"""
Deep learning fallback engine.

Wraps the Siamese ONNX inference with candidate re-ranking logic.
Only activated when classical pipeline detects ambiguity.
"""

from typing import List, Optional

import numpy as np


class DLEngine:
    """
    Deep learning fallback engine for ambiguous candidate resolution.

    Uses the Siamese verifier to re-rank top-K candidates when
    the classical pipeline detects periodic alias ambiguity.
    """

    def __init__(self, config: dict):
        self.config = config
        self.model = None  # Lazy-loaded ONNX session

    def load_model(self):
        """Load the Siamese ONNX model."""
        # TODO: Implement
        raise NotImplementedError

    def rerank_candidates(
        self,
        reference: np.ndarray,
        search: np.ndarray,
        candidates: list,
        context_size: int = 128,
    ) -> list:
        """
        Re-rank candidates using Siamese verification.

        Args:
            reference: Reference image.
            search: Search image.
            candidates: List of candidate locations from classical pipeline.
            context_size: Size of context crops for Siamese input.

        Returns:
            Re-ranked candidate list with updated scores.
        """
        # TODO: Implement
        raise NotImplementedError
