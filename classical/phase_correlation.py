"""
Phase correlation for coarse localization.

FFT-based translation estimation using cross-power spectrum.
Used at pyramid L0 for fast candidate generation (top-20).

Limitation: Periodic structures create multiple peaks at pitch intervals.
This module generates candidates only; disambiguation is done by periodicity.py.
"""

from typing import List, Optional, Tuple

import numpy as np


def phase_correlate(
    template: np.ndarray,
    search: np.ndarray,
    window: str = "hann",
) -> np.ndarray:
    """
    Compute phase correlation between template and search.

    Args:
        template: Template image (resized to search scale).
        search: Search image.
        window: Window function ('hann', 'hamming', 'none').

    Returns:
        Phase correlation map.
    """
    # TODO: Implement
    raise NotImplementedError


def multiscale_phase_correlation(
    template: np.ndarray,
    search: np.ndarray,
    levels: int = 3,
    level_sizes: Optional[List[int]] = None,
    top_k: int = 20,
) -> List[Tuple[int, int, float]]:
    """
    Multi-scale phase correlation using image pyramid.

    Args:
        template: Reference template.
        search: Search image.
        levels: Number of pyramid levels.
        level_sizes: Resolution at each level (default: [256, 512, 1000]).
        top_k: Number of candidates to return from coarsest level.

    Returns:
        List of (row, col, score) candidate locations.
    """
    # TODO: Implement
    raise NotImplementedError
