"""
DRIFT-SENSE: Classical Computer Vision Pipeline
=================================================

Multi-scale coarse-to-fine registration using:
  - Phase correlation (coarse localization)
  - Distance Transform + Normalized Cross-Correlation (DT-NCC)
  - Periodicity-aware alias clustering
  - ECC refinement with subpixel fitting
"""

from classical.pipeline import ClassicalPipeline

__all__ = ["ClassicalPipeline"]
