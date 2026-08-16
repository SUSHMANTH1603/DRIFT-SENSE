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
        # TODO: Implement in Phase 0
        # 1. Generate continuous layout (12µm × 12µm at 1 nm/px)
        # 2. Extract reference FOV (1000×1000 at 1 nm/px)
        # 3. Extract search FOV (10000×10000 at 1 nm/px)
        # 4. Apply independent SEM degradations
        # 5. Downsample search to 1000×1000 (10 nm/px)
        # 6. Record ground truth center in search coordinates
        raise NotImplementedError

    def _extract_fov(
        self, layout: np.ndarray, bbox: Tuple[int, int, int, int], target_size: int
    ) -> np.ndarray:
        """Extract and resize a field-of-view from the continuous layout."""
        # TODO: Implement
        raise NotImplementedError
