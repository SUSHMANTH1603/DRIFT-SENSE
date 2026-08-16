"""
Normalized Cross-Correlation (NCC) with FFT acceleration.

Provides DT-NCC (Distance Transform NCC) as the primary matching
metric, with FFT-based acceleration for large images.

Formulation:
    C(u,v) = sum[(D_R - mu_R)(D_S(u,v) - mu_S)] / sqrt(sum(D_R - mu_R)^2 * sum(D_S - mu_S)^2)
"""

from typing import Optional, Tuple

import numpy as np


def ncc_fft(
    template: np.ndarray,
    search: np.ndarray,
) -> np.ndarray:
    """
    Compute NCC using FFT acceleration.

    Args:
        template: Template image (e.g., 100×100 DT of reference).
        search: Search image (e.g., 1000×1000 DT of search).

    Returns:
        NCC correlation map.
    """
    # TODO: Implement FFT-based NCC
    raise NotImplementedError


def dt_ncc(
    dt_reference: np.ndarray,
    dt_search: np.ndarray,
) -> np.ndarray:
    """
    Distance Transform NCC — the primary matching metric.

    Computes NCC between DT representations for robustness
    to SEM intensity variations.

    Args:
        dt_reference: DT of reference edges (resized to search scale).
        dt_search: DT of search image edges.

    Returns:
        Correlation map.
    """
    # TODO: Implement
    raise NotImplementedError


def find_peaks(
    correlation_map: np.ndarray,
    top_k: int = 20,
    min_distance: int = 10,
) -> list:
    """
    Find top-K peaks in a correlation map.

    Args:
        correlation_map: 2D NCC output.
        top_k: Number of peaks to return.
        min_distance: Minimum distance between peaks.

    Returns:
        List of (row, col, score) tuples, sorted by score descending.
    """
    # TODO: Implement with non-maximum suppression
    raise NotImplementedError
