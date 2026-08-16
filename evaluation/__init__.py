"""
DRIFT-SENSE: Evaluation Framework
====================================

Metrics, benchmarking, failure taxonomy, and visualization
for registration accuracy assessment.
"""

from evaluation.metrics import evaluate
from evaluation.failures import classify_failure, FAILURE_TYPES

__all__ = ["evaluate", "classify_failure", "FAILURE_TYPES"]
