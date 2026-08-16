"""
Base semiconductor structure generator.

Abstract base class for generating continuous physical layouts
and reference/search image pairs with independent SEM degradations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import numpy as np


@dataclass
class PairMetadata:
    """Metadata for a generated reference-search image pair."""

    pair_id: str = ""
    style: str = ""
    ground_truth_x: float = 0.0
    ground_truth_y: float = 0.0
    scale: float = 0.1
    rotation_deg: float = 0.0
    noise_params_ref: Dict = field(default_factory=dict)
    noise_params_search: Dict = field(default_factory=dict)
    structure_params: Dict = field(default_factory=dict)
    seed: int = 0


import uuid
import cv2
from generator.noise import NoiseModel, NoiseParams, REFERENCE_NOISE, SEARCH_NOISE
from generator.sem_model import SEMDegradationModel, SEMParams
from generator.utils import extract_fov, downsample

class SemiconductorGenerator(ABC):
    """
    Abstract base class for semiconductor structure generators.

    Subclasses implement specific layout patterns (DRAM, FinFET).
    The base class handles FOV extraction, SEM degradation, and pair generation.
    """

    def __init__(self, config: dict, seed: int = 42):
        """
        Args:
            config: Generator configuration dict (from generator.yaml).
            seed: Random seed for reproducibility.
        """
        self.config = config
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.style = "Base"

    @abstractmethod
    def generate_continuous_layout(self, size_um: float = 12.0) -> np.ndarray:
        """
        Generate a large continuous physical structure.

        Args:
            size_um: Physical size in micrometers.

        Returns:
            High-resolution binary/float array at 1 nm/px.
        """
        ...

    def generate_pair(self) -> Tuple[np.ndarray, np.ndarray, PairMetadata]:
        """
        Generate a reference-search image pair with independent noise.

        Returns:
            Tuple of (reference_image, search_image, metadata).
        """
        # 1. Generate large continuous layout (12 um x 12 um = 12000 x 12000 pixels at 1 nm/px)
        continuous_um = self.config.get("fov", {}).get("continuous_layout_um", 12.0)
        layout = self.generate_continuous_layout(size_um=continuous_um)
        
        layout_size_px = layout.shape[0]
        center_layout = layout_size_px // 2
        
        # 2. Extract reference center with random stage error (translation)
        # Search area covers 10 µm = 10000 nm (at 1 nm/px).
        # Reference area covers 1 µm = 1000 nm (at 1 nm/px).
        # Reference center can be offset from search center.
        # Max offset is clamped so reference is fully inside search FOV with margin.
        max_offset_nm = 3500.0  # 3.5 µm to keep reference crop safely inside search crop
        offset_x = self.rng.normal(0.0, 1000.0)
        offset_y = self.rng.normal(0.0, 1000.0)
        offset_x = np.clip(offset_x, -max_offset_nm, max_offset_nm)
        offset_y = np.clip(offset_y, -max_offset_nm, max_offset_nm)
        
        # Coordinates in continuous layout (1 nm/px)
        search_center_r = center_layout
        search_center_c = center_layout
        
        ref_center_r = int(search_center_r + offset_y)
        ref_center_c = int(search_center_c + offset_x)
        
        # 3. Extract raw reference FOV (1000 x 1000 px at 1 nm/px)
        ref_fov_size = int(self.config.get("fov", {}).get("reference_um", 1.0) * 1000)
        ref_clean = extract_fov(layout, (ref_center_r, ref_center_c), ref_fov_size)
        
        # 4. Extract raw search FOV (10000 x 10000 px at 1 nm/px)
        search_fov_size = int(self.config.get("fov", {}).get("search_um", 10.0) * 1000)
        search_clean_large = extract_fov(layout, (search_center_r, search_center_c), search_fov_size)
        
        # 5. Downsample search FOV to 1000 x 1000 (10 nm/px)
        search_clean = downsample(search_clean_large, factor=10)
        
        # 6. Apply rotation and scale geometric transformation to the search image
        # (This simulates stage rotation/scale error relative to reference)
        rotation_deg = self.rng.uniform(-2.0, 2.0)
        scale_factor = self.rng.uniform(0.95, 1.05)
        
        # Compute ground truth translation in un-rotated/scaled search coordinates
        # Reference center relative to search top-left: (ref_center - search_top_left) / 10
        search_top_left_r = search_center_r - search_fov_size // 2
        search_top_left_c = search_center_c - search_fov_size // 2
        
        raw_gt_y = (ref_center_r - search_top_left_r) / 10.0
        raw_gt_x = (ref_center_c - search_top_left_c) / 10.0
        
        # Get warp matrix around search center (500, 500)
        warp_center = (500.0, 500.0)
        M = cv2.getRotationMatrix2D(warp_center, rotation_deg, scale_factor)
        
        # Warp search clean image
        search_clean_warped = cv2.warpAffine(
            search_clean,
            M,
            (1000, 1000),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101
        )
        
        # Map the ground truth center coordinate through the warp transformation
        gt_pt = np.array([raw_gt_x, raw_gt_y, 1.0])
        gt_x, gt_y = M.dot(gt_pt)
        
        # 7. Apply SEM degradations independently
        # Instantiate independent parameters and rngs to ensure independent noise realizations
        ref_seed = int(self.rng.integers(0, 2**31))
        search_seed = int(self.rng.integers(0, 2**31))
        
        # Reference SEM and noise models
        ref_sem_params = SEMParams(
            blur_sigma_px=1.5,
            edge_brightening_alpha=0.2,
            charging_amplitude=0.05,
            contrast_gain=1.0,
            brightness_offset=0.0
        )
        ref_sem_model = SEMDegradationModel(ref_sem_params, np.random.default_rng(ref_seed))
        ref_noise_model = NoiseModel(REFERENCE_NOISE, np.random.default_rng(ref_seed + 1))
        
        # Search SEM and noise models
        search_sem_params = SEMParams(
            blur_sigma_px=1.0,
            edge_brightening_alpha=0.15,
            charging_amplitude=0.10,
            contrast_gain=1.0,
            brightness_offset=0.0
        )
        search_sem_model = SEMDegradationModel(search_sem_params, np.random.default_rng(search_seed))
        search_noise_model = NoiseModel(SEARCH_NOISE, np.random.default_rng(search_seed + 1))
        
        # Apply degradations
        ref_degraded = ref_sem_model.apply(ref_clean)
        reference_image = ref_noise_model.apply(ref_degraded)
        
        search_degraded = search_sem_model.apply(search_clean_warped)
        search_image = search_noise_model.apply(search_degraded)
        
        # 8. Construct Metadata
        pair_id = str(uuid.uuid4())
        metadata = PairMetadata(
            pair_id=pair_id,
            style=self.style,
            ground_truth_x=float(gt_x),
            ground_truth_y=float(gt_y),
            scale=float(scale_factor),
            rotation_deg=float(rotation_deg),
            noise_params_ref={
                "shot_scale": REFERENCE_NOISE.shot_scale,
                "read_noise": REFERENCE_NOISE.read_noise_electrons,
            },
            noise_params_search={
                "shot_scale": SEARCH_NOISE.shot_scale,
                "read_noise": SEARCH_NOISE.read_noise_electrons,
            },
            structure_params={
                "offset_x_nm": float(offset_x),
                "offset_y_nm": float(offset_y),
            },
            seed=self.seed
        )
        
        return reference_image, search_image, metadata

    def _extract_fov(
        self, layout: np.ndarray, bbox: Tuple[int, int, int, int], target_size: int
    ) -> np.ndarray:
        """Extract and resize a field-of-view from the continuous layout."""
        # bbox is (r_center, c_center, fov_size)
        r_c, c_c, size = bbox
        extracted = extract_fov(layout, (r_c, c_c), size)
        if extracted.shape[0] != target_size:
            extracted = cv2.resize(extracted, (target_size, target_size), interpolation=cv2.INTER_AREA)
        return extracted
