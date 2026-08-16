"""
Distance transform computation and normalization.

Converts binary edge maps to smooth distance fields for robust
template matching. DT-NCC is the core matching representation
in the classical pipeline.

Key insight: DT converts binary edges → smooth distance field,
enabling subpixel NCC and robustness to edge detection variations.
"""

from typing import Tuple

import numpy as np


def compute_distance_transform(
    edge_map: np.ndarray,
    dist_type: str = "L2",
    mask_size: int = 5,
    normalize: bool = True,
    normalize_range: Tuple[float, float] = (0.0, 1.0),
) -> np.ndarray:
    """
    Compute distance transform from a binary edge map.

    Args:
        edge_map: Binary edge image (0 or 255).
        dist_type: Distance type ('L1', 'L2', 'C').
        mask_size: Mask size for DT computation (3, 5, or 0 for exact).
        normalize: Whether to normalize the output.
        normalize_range: Output range after normalization.

    Returns:
        Distance transform image (float32).
    """
    # TODO: Implement with cv2.distanceTransform
    raise NotImplementedError


def ler_aware_distance_transform(
    edge_map: np.ndarray, opening_kernel: int = 3
) -> np.ndarray:
    """
    LER-aware distance transform.

    Applies morphological opening before DT to suppress
    high-frequency noise from line edge roughness.
    Mitigation for failure mode F7.
    """
    # TODO: Implement
    raise NotImplementedError
