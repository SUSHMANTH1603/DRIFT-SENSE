"""
Loss functions for Siamese training.

Implements Supervised Contrastive Loss (Khosla et al., ICML 2020)
with temperature scaling, and Triplet Loss as fallback.
"""

# TODO: Implement in Phase 4


class SupervisedContrastiveLoss:
    """
    Supervised Contrastive Loss.

    Ref: Khosla et al., "Supervised Contrastive Learning", ICML 2020

    Args:
        temperature: Softmax temperature (default: 0.1).
    """

    def __init__(self, temperature: float = 0.1):
        self.temperature = temperature

    def __call__(self, embeddings, labels):
        """
        Compute supervised contrastive loss.

        Args:
            embeddings: [2*N, D] normalized embeddings.
            labels: [2*N] labels (each pair shares a label).

        Returns:
            Scalar loss.
        """
        # TODO: Implement
        raise NotImplementedError


class TripletLoss:
    """Triplet loss with configurable margin."""

    def __init__(self, margin: float = 0.5):
        self.margin = margin

    def __call__(self, anchor, positive, negative):
        # TODO: Implement
        raise NotImplementedError
