"""
Common utilities for the generator module.

Provides shared functions for coordinate transforms, FOV extraction,
downsampling, and metadata handling used across DRAM and FinFET generators.
"""

from typing import Tuple

import numpy as np


def nm_to_px(value_nm: float, resolution_nm_per_px: float) -> float:
    """Convert physical nanometers to pixel coordinates."""
    return value_nm / resolution_nm_per_px


def px_to_nm(value_px: float, resolution_nm_per_px: float) -> float:
    """Convert pixel coordinates to physical nanometers."""
    return value_px * resolution_nm_per_px


def extract_fov(
    layout: np.ndarray,
    center: Tuple[int, int],
    fov_size_px: int,
) -> np.ndarray:
    """
    Extract a field-of-view centered at `center` from a continuous layout.

    Args:
        layout: Full continuous layout array.
        center: (row, col) center of the FOV.
        fov_size_px: Size of the square FOV in pixels.

    Returns:
        Cropped FOV array.
    """
    # TODO: Implement with boundary handling
    raise NotImplementedError


def downsample(image: np.ndarray, factor: int) -> np.ndarray:
    """
    Downsample an image by an integer factor using area averaging.

    Args:
        image: Input image.
        factor: Downsampling factor (e.g., 10 for 10× magnification change).

    Returns:
        Downsampled image.
    """
    # TODO: Implement with proper anti-aliasing
    raise NotImplementedError


def generate_ler(
    length_px: int,
    sigma_nm: float,
    correlation_length_nm: float,
    resolution_nm_per_px: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Generate line edge roughness (LER) profile.

    Uses correlated Gaussian noise with specified sigma and correlation length.

    Args:
        length_px: Length of the line in pixels.
        sigma_nm: RMS roughness in nanometers.
        correlation_length_nm: Spatial correlation length in nanometers.
        resolution_nm_per_px: Resolution of the layout.
        rng: Random number generator.

    Returns:
        1D array of edge deviations in pixels.
    """
    # TODO: Implement using convolution with Gaussian kernel
    raise NotImplementedError
