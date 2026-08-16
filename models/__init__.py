"""
DRIFT-SENSE: Deep Learning Models
===================================

Siamese verification network for ambiguous candidate disambiguation.
Only triggered when the classical pipeline cannot resolve periodic aliases.
"""

from models.siamese import SiameseVerifier

__all__ = ["SiameseVerifier"]
