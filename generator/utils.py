"""
Common utilities for the generator module.

Provides shared functions for coordinate transforms, FOV extraction,
downsampling, and metadata handling used across DRAM and FinFET generators.
"""

from typing import Tuple

import numpy as np


import cv2

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
    Uses zero-padding if the window goes out of bounds.

    Args:
        layout: Full continuous layout array.
        center: (row, col) center of the FOV.
        fov_size_px: Size of the square FOV in pixels.

    Returns:
        Cropped FOV array of shape (fov_size_px, fov_size_px).
    """
    r, c = center
    half = fov_size_px // 2
    
    # Calculate crop coordinates
    r_start, r_end = r - half, r + half
    c_start, c_end = c - half, c + half
    
    # Bounds of layout
    max_r, max_c = layout.shape
    
    # Handle out of bounds with padding
    pad_top = max(0, -r_start)
    pad_bottom = max(0, r_end - max_r)
    pad_left = max(0, -c_start)
    pad_right = max(0, c_end - max_c)
    
    # Crop bounds clamped to layout
    crop_r_start = max(0, r_start)
    crop_r_end = min(max_r, r_end)
    crop_c_start = max(0, c_start)
    crop_c_end = min(max_c, c_end)
    
    cropped = layout[crop_r_start:crop_r_end, crop_c_start:crop_c_end]
    
    # Apply padding if necessary
    if pad_top > 0 or pad_bottom > 0 or pad_left > 0 or pad_right > 0:
        cropped = np.pad(
            cropped,
            ((pad_top, pad_bottom), (pad_left, pad_right)),
            mode='constant',
            constant_values=0.0
        )
        
    return cropped


def downsample(image: np.ndarray, factor: int) -> np.ndarray:
    """
    Downsample an image by an integer factor using area averaging.

    Args:
        image: Input image.
        factor: Downsampling factor (e.g., 10 for 10× magnification change).

    Returns:
        Downsampled image.
    """
    if factor == 1:
        return image.copy()
    h, w = image.shape
    new_h, new_w = h // factor, w // factor
    # OpenCV INTER_AREA is ideal for decimation to avoid aliasing artifacts
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)


def generate_ler(
    length_px: int,
    sigma_nm: float,
    correlation_length_nm: float,
    resolution_nm_per_px: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Generate line edge roughness (LER) profile.

    Uses uncorrelated Gaussian noise convolved with a Gaussian correlation kernel
    to produce correlated spatial noise matching specified LER parameters.

    Args:
        length_px: Length of the line in pixels.
        sigma_nm: RMS roughness in nanometers.
        correlation_length_nm: Spatial correlation length in nanometers.
        resolution_nm_per_px: Resolution of the layout.
        rng: Random number generator.

    Returns:
        1D array of edge deviations in pixels.
    """
    if sigma_nm <= 0.0:
        return np.zeros(length_px, dtype=np.float32)
        
    # Convert physical params to pixel domain
    sigma_px = sigma_nm / resolution_nm_per_px
    lc_px = correlation_length_nm / resolution_nm_per_px
    
    # Generate white Gaussian noise (with extra padding to avoid edge effects)
    pad = int(np.ceil(3 * lc_px)) if lc_px > 0 else 0
    total_len = length_px + 2 * pad
    white_noise = rng.normal(0.0, 1.0, total_len)
    
    if lc_px <= 0.0:
        # Uncorrelated noise
        raw_ler = white_noise[pad : pad + length_px]
    else:
        # Create Gaussian filter kernel matching Lc
        # Normal distribution kernel: exp(-x^2 / (2 * lc_px^2))
        kernel_size = 2 * pad + 1
        x = np.arange(kernel_size) - pad
        kernel = np.exp(-0.5 * (x / lc_px) ** 2)
        kernel /= np.sum(kernel)
        
        # Convolve white noise with Gaussian kernel
        raw_ler = np.convolve(white_noise, kernel, mode='same')[pad : pad + length_px]
        
    # Scale raw LER to exact target standard deviation in pixels
    std_raw = np.std(raw_ler)
    if std_raw > 0:
        raw_ler = (raw_ler / std_raw) * sigma_px
    else:
        raw_ler = raw_ler * sigma_px
        
    return raw_ler

