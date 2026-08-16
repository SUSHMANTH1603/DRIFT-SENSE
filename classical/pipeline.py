"""
Classical CV registration pipeline.

Orchestrates the full classical path:
  Preprocessing → Phase Correlation → DT-NCC → Periodicity → Refinement → Validation

This is the main entry point for the classical registration engine.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import numpy as np

from classical.candidates import Candidate, CandidateManager


@dataclass
class RegistrationResult:
    """Output of the classical registration pipeline."""

    x: float = 0.0
    y: float = 0.0
    confidence: float = 0.0
    path_taken: str = "classical"   # "classical" or "dl_fallback"
    top_candidates: list = None
    pitch: Tuple[float, float] = (0.0, 0.0)
    alias_detected: bool = False
    reprojection_error: float = 0.0
    latency_ms: float = 0.0
    failure_code: str = "F0"        # From failure taxonomy

    def __post_init__(self):
        if self.top_candidates is None:
            self.top_candidates = []


class ClassicalPipeline:
    """
    Full classical CV registration pipeline.

    Implements the coarse-to-fine multi-scale strategy:
      L0: Phase correlation (256×256) → top-20 candidates
      L1: DT-NCC (512×512) → top-5 candidates
      L2: DT-NCC + ECC (1000×1000) → subpixel result
    """

    def __init__(self, config: dict):
        """
        Args:
            config: Classical pipeline configuration (from classical.yaml).
        """
        self.config = config

    def register(
        self,
        reference: np.ndarray,
        search: np.ndarray,
    ) -> RegistrationResult:
        """
        Run the full classical registration pipeline.

        Args:
            reference: Reference SEM image (1000×1000, grayscale).
            search: Search SEM image (1000×1000, grayscale).

        Returns:
            RegistrationResult with (x, y), confidence, and metadata.
        """
        # TODO: Implement full pipeline
        # 1. Preprocess both images
        # 2. Coarse localization (phase correlation at L0)
        # 3. Medium refinement (DT-NCC at L1)
        # 4. Periodicity analysis
        # 5. Fine refinement (DT-NCC + ECC at L2)
        # 6. Subpixel fitting
        # 7. Validation
        raise NotImplementedError

    def _compute_confidence(
        self,
        candidates: list,
        scores: list,
        pitch: Tuple[float, float],
        siamese_score: Optional[float] = None,
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute multi-component confidence score.

        Components:
          - Score margin (top-1 vs top-2): w=0.35
          - Periodicity consistency: w=0.20
          - Geometric consistency (ECC residual): w=0.20
          - Center prior alignment: w=0.10
          - Siamese score (if used): w=0.15

        Returns:
            (confidence, component_scores).
        """
        # TODO: Implement
        raise NotImplementedError

    def needs_dl_fallback(
        self, confidence: float, alias_detected: bool
    ) -> bool:
        """
        Decide whether to trigger the DL fallback.

        Triggers if:
          - Score margin < 5% AND alias cluster detected
          - Confidence < routing threshold (0.3)

        Returns:
            True if DL fallback should be used.
        """
        # TODO: Implement
        raise NotImplementedError
