"""
Visualization utilities for generated data.

Functions for visualizing:
  - Generated structure layouts
  - Reference/search image pairs with ground truth overlay
  - Noise comparison panels
  - SEM degradation pipeline stages
"""

from typing import Optional, Tuple

import numpy as np


def visualize_pair(
    reference: np.ndarray,
    search: np.ndarray,
    gt_center: Optional[Tuple[float, float]] = None,
    pred_center: Optional[Tuple[float, float]] = None,
    title: str = "",
    save_path: Optional[str] = None,
) -> None:
    """
    Visualize a reference-search pair with optional ground truth and prediction overlay.

    Args:
        reference: Reference image (1000×1000).
        search: Search image (1000×1000).
        gt_center: Ground truth center (x, y) in search coordinates.
        pred_center: Predicted center (x, y) in search coordinates.
        title: Plot title.
        save_path: If provided, save figure to this path.
    """
    # TODO: Implement with matplotlib
    raise NotImplementedError


def visualize_degradation_pipeline(
    clean: np.ndarray,
    stages: dict,
    save_path: Optional[str] = None,
) -> None:
    """Show each SEM degradation stage side by side."""
    # TODO: Implement
    raise NotImplementedError


def visualize_noise_comparison(
    clean: np.ndarray,
    ref_noisy: np.ndarray,
    search_noisy: np.ndarray,
    save_path: Optional[str] = None,
) -> None:
    """Compare clean vs. reference noise vs. search noise."""
    # TODO: Implement
    raise NotImplementedError
