"""
Subpixel refinement and validation.

Provides multiple refinement methods:
  - Parabolic peak fitting (fast, ~0.2 px RMSE)
  - Gaussian peak fitting (accurate, ~0.15 px RMSE)
  - ECC (Enhanced Correlation Coefficient, ~0.1 px RMSE)
  - Lucas-Kanade optical flow (~0.15 px RMSE)

Includes validation via reprojection error and fit quality checks.

References:
  [24] Evangelidis & Psarakis (2008) — ECC
"""

from typing import Optional, Tuple

import numpy as np


def parabolic_peak_fit(
    correlation_map: np.ndarray,
    peak_loc: Tuple[int, int],
    window: int = 5,
) -> Tuple[float, float]:
    """
    Parabolic subpixel peak fitting.

    Fits a 2D parabola around the peak for subpixel localization.
    Fast but less accurate than Gaussian fit.

    Args:
        correlation_map: NCC correlation map.
        peak_loc: Integer peak location (row, col).
        window: Half-window size for fitting.

    Returns:
        Subpixel (row, col) location.
    """
    # TODO: Implement
    raise NotImplementedError


def gaussian_peak_fit(
    correlation_map: np.ndarray,
    peak_loc: Tuple[int, int],
    window: int = 5,
    min_r_squared: float = 0.9,
) -> Tuple[float, float, float]:
    """
    2D Gaussian subpixel peak fitting.

    Fits A*exp(-((x-x0)^2/(2*sx^2) + (y-y0)^2/(2*sy^2))) + C.

    Args:
        correlation_map: NCC correlation map.
        peak_loc: Integer peak location.
        window: Half-window size.
        min_r_squared: Quality gate — if R^2 < this, returns NaN.

    Returns:
        (subpixel_row, subpixel_col, r_squared).
    """
    # TODO: Implement with scipy.optimize.curve_fit
    raise NotImplementedError


def ecc_refinement(
    reference: np.ndarray,
    search_roi: np.ndarray,
    max_iterations: int = 50,
    epsilon: float = 1e-5,
    motion_model: str = "euclidean",
) -> Tuple[np.ndarray, float]:
    """
    ECC (Enhanced Correlation Coefficient) refinement.

    Iteratively refines the transformation between reference and
    search ROI for subpixel accuracy.

    Args:
        reference: Reference image (resized to match).
        search_roi: ROI from search image around candidate.
        max_iterations: Maximum ECC iterations.
        epsilon: Convergence threshold.
        motion_model: 'translation', 'euclidean', or 'affine'.

    Returns:
        (warp_matrix, residual).
    """
    # TODO: Implement with cv2.findTransformECC
    raise NotImplementedError


def compute_reprojection_error(
    reference: np.ndarray,
    search: np.ndarray,
    warp_matrix: np.ndarray,
) -> float:
    """
    Compute reprojection error for validation.

    Warps reference into search space and measures pixel-wise error.

    Returns:
        Mean absolute reprojection error.
    """
    # TODO: Implement
    raise NotImplementedError
