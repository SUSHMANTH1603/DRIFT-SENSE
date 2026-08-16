"""
Noise model for independent SEM image captures.

Implements the Poisson-Gaussian noise model for SEM imaging:
  y ~ N(lambda, lambda + sigma_read^2)

Reference and search images receive independent noise realizations
with different parameter scales (search is noisier due to lower magnification).

References:
  [3] Foi et al., TPAMI 2008
  [4] SEMI E1661
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class NoiseParams:
    """Noise parameters for a single SEM capture."""

    shot_scale: float = 1.0           # Poisson noise multiplier
    read_noise_electrons: float = 8.0  # Gaussian read noise sigma
    gain: float = 1.0                  # Detector gain


# Default noise parameter sets (from Section 13.2 of the spec)
REFERENCE_NOISE = NoiseParams(shot_scale=1.0, read_noise_electrons=8.0, gain=1.0)
SEARCH_NOISE = NoiseParams(shot_scale=3.0, read_noise_electrons=12.0, gain=1.0)


class NoiseModel:
    """
    Poisson-Gaussian noise model for SEM imaging.

    Generates independent noise realizations for reference and search images.
    Search images are physically noisier (lower magnification = fewer electrons/pixel).
    """

    def __init__(self, params: Optional[NoiseParams] = None, rng: Optional[np.random.Generator] = None):
        self.params = params or REFERENCE_NOISE
        self.rng = rng or np.random.default_rng()

    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Poisson-Gaussian noise to an image.

        Args:
            image: Clean image (float, [0, 1]).

        Returns:
            Noisy image in range [0, 1].
        """
        # Base electron dose at shot_scale = 1.0 is 300 electrons/pixel
        dose = 300.0 / self.params.shot_scale
        
        # Ensure image is non-negative
        lam = np.clip(image * dose, 1e-6, None)
        
        # Poisson shot noise (electron counting)
        electrons = self.rng.poisson(lam).astype(np.float32)
        
        # Gaussian read noise
        read_noise = self.rng.normal(
            0.0,
            self.params.read_noise_electrons,
            size=image.shape
        ).astype(np.float32)
        
        # Total noisy signal in electron counts
        noisy_electrons = electrons + read_noise
        
        # Normalize back to [0, 1] intensity range
        noisy_image = noisy_electrons / dose
        return np.clip(noisy_image, 0.0, 1.0)

    @staticmethod
    def create_independent_pair(
        ref_params: Optional[NoiseParams] = None,
        search_params: Optional[NoiseParams] = None,
        seed: int = 42,
    ) -> tuple:
        """
        Create two independent noise models for reference and search images.

        Returns:
            Tuple of (ref_noise_model, search_noise_model).
        """
        rng1 = np.random.default_rng(seed)
        rng2 = np.random.default_rng(seed + 1)  # Different seed = independent
        return (
            NoiseModel(ref_params or REFERENCE_NOISE, rng1),
            NoiseModel(search_params or SEARCH_NOISE, rng2),
        )
