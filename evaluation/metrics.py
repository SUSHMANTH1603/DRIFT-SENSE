"""
Evaluation metrics for registration accuracy.

Implements the full metrics suite from Section 18 of the specification:
  - Localization error (mean, median, p95, max)
  - Accuracy at thresholds (0.5px, 1px, 2px, 5px, 10px)
  - Alias error rate
  - False confidence rate
  - Failure rate
  - Latency statistics
"""

from typing import Dict, List, Optional

import numpy as np


def evaluate(
    predictions: np.ndarray,
    ground_truths: np.ndarray,
    confidences: Optional[np.ndarray] = None,
    latencies: Optional[np.ndarray] = None,
    pitch: Optional[float] = None,
) -> Dict[str, float]:
    """
    Compute full evaluation metrics suite.

    Args:
        predictions: [N, 2] predicted (x, y) locations.
        ground_truths: [N, 2] ground truth (x, y) locations.
        confidences: [N] confidence scores (optional).
        latencies: [N] per-sample latencies in ms (optional).
        pitch: Structural pitch in pixels (for alias error computation).

    Returns:
        Dictionary of metric name → value.
    """
    # TODO: Implement
    raise NotImplementedError


def compute_alias_errors(
    predictions: np.ndarray,
    ground_truths: np.ndarray,
    pitch: float,
    tolerance_px: float = 2.0,
) -> float:
    """
    Compute alias error rate.

    An alias error occurs when the prediction differs from GT
    by approximately n × pitch (n ≠ 0).

    Returns:
        Fraction of samples with alias errors.
    """
    # TODO: Implement
    raise NotImplementedError


def compute_false_confidence(
    confidences: np.ndarray,
    errors: np.ndarray,
    error_threshold: float = 5.0,
    confidence_threshold: float = 0.8,
) -> float:
    """
    Compute false confidence rate.

    Fraction of samples with high confidence but large error.
    """
    # TODO: Implement
    raise NotImplementedError
