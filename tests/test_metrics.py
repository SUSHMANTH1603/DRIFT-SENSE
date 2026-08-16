"""Tests for evaluation metrics."""

import pytest
import numpy as np


class TestMetrics:
    """Tests for the evaluation metrics suite."""

    def test_perfect_predictions_give_zero_error(self):
        # TODO: Implement
        pass

    def test_accuracy_at_threshold(self):
        """Accuracy@K should count predictions within K pixels."""
        # TODO: Implement
        pass

    def test_alias_error_detection(self):
        """Predictions offset by exactly 1 pitch should be flagged."""
        # TODO: Implement
        pass

    def test_false_confidence_rate(self):
        """High confidence + large error should be flagged."""
        # TODO: Implement
        pass


class TestFailureTaxonomy:
    """Tests for failure classification."""

    def test_periodic_alias_classified_as_f1(self):
        # TODO: Implement
        pass

    def test_unknown_failure_returns_f0(self):
        # TODO: Implement
        pass
