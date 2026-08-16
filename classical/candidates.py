"""
Candidate generation and scoring.

Manages the top-K candidate pipeline across multi-scale levels:
  L0 (coarse): Phase correlation → top-20
  L1 (medium): DT-NCC refinement → top-5
  L2 (fine): DT-NCC + ECC → top-1
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np


@dataclass
class Candidate:
    """A registration candidate with score and metadata."""

    row: int = 0
    col: int = 0
    score: float = 0.0
    level: str = ""           # Which pyramid level produced this
    alias_cluster_id: int = -1  # Alias cluster assignment
    refined: bool = False       # Whether subpixel refinement was applied
    subpixel_row: float = 0.0
    subpixel_col: float = 0.0


class CandidateManager:
    """
    Manages candidate generation, scoring, and filtering across scales.
    """

    def __init__(self, config: dict):
        self.config = config
        self.candidates: List[Candidate] = []

    def add_candidates(
        self, locations: List[Tuple[int, int, float]], level: str
    ) -> None:
        """Add candidates from a pyramid level."""
        # TODO: Implement
        raise NotImplementedError

    def filter_top_k(self, k: int) -> List[Candidate]:
        """Return top-K candidates by score."""
        # TODO: Implement
        raise NotImplementedError

    def apply_alias_clustering(
        self, pitch: Tuple[float, float], tolerance_px: float = 2.0
    ) -> None:
        """Assign alias cluster IDs to candidates."""
        # TODO: Implement
        raise NotImplementedError

    def get_best_candidate(self) -> Candidate:
        """Return the highest-scoring candidate after all filtering."""
        # TODO: Implement
        raise NotImplementedError
