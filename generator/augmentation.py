"""
Data augmentation pipeline for training.

Augmentations are physically motivated by SEM imaging and stage error sources.
See Section 14 of the technical specification for full table.

References:
  [3] Foi et al., TPAMI 2008 (noise)
  [6] Applied Materials US20190122688 (charging)
  [7] ASML US20150364221 (scan distortion)
  [8] KLA US20180018765 (thermal drift)
  [9] ASML US20170098602 (stage hysteresis)
"""

from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np


@dataclass
class AugmentationConfig:
    """Configuration for training augmentations."""

    rotation_range_deg: Tuple[float, float] = (-2.0, 2.0)
    scale_range: Tuple[float, float] = (0.95, 1.05)
    translation_range_px: int = 200
    noise_probability: float = 1.0
    blur_sigma_range: Tuple[float, float] = (0.5, 3.0)
    blur_probability: float = 0.8
    contrast_range: Tuple[float, float] = (0.7, 1.3)
    brightness_range: Tuple[float, float] = (-30.0, 30.0)
    photometric_probability: float = 0.8
    charging_probability: float = 0.5
    scan_distortion_probability: float = 0.3
    scan_distortion_amplitude_px: float = 2.0


class Augmentor:
    """Applies physically-motivated augmentations to SEM image pairs."""

    def __init__(self, config: Optional[AugmentationConfig] = None, rng: Optional[np.random.Generator] = None):
        self.config = config or AugmentationConfig()
        self.rng = rng or np.random.default_rng()

    def augment_pair(
        self, reference: np.ndarray, search: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply augmentations to a reference-search pair.

        Geometric augmentations are applied jointly (consistent transform),
        photometric augmentations are applied independently.

        Returns:
            Augmented (reference, search) tuple.
        """
        # TODO: Implement
        raise NotImplementedError
