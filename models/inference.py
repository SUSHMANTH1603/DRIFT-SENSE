"""
ONNX Runtime inference wrapper for the Siamese model.

Loads an exported ONNX model and provides a clean inference API
for integration with the hybrid pipeline.
"""

from typing import List, Optional

import numpy as np


class SiameseInference:
    """
    ONNX Runtime inference wrapper for the Siamese verifier.

    Supports both CPU and CUDA execution providers.
    """

    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Args:
            model_path: Path to the ONNX model file.
            device: 'cpu' or 'cuda'.
        """
        self.model_path = model_path
        self.device = device
        self.session = None
        # TODO: Initialize ONNX Runtime session

    def load(self):
        """Load the ONNX model."""
        # TODO: Implement
        raise NotImplementedError

    def embed(self, crops: np.ndarray) -> np.ndarray:
        """
        Compute embeddings for a batch of crops.

        Args:
            crops: [N, 1, 128, 128] grayscale crops.

        Returns:
            [N, 128] L2-normalized embeddings.
        """
        # TODO: Implement
        raise NotImplementedError

    def score_candidates(
        self, reference_crop: np.ndarray, candidate_crops: List[np.ndarray]
    ) -> List[float]:
        """
        Score candidates against a reference crop.

        Returns:
            List of cosine similarity scores.
        """
        # TODO: Implement
        raise NotImplementedError
