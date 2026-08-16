"""
PyTorch dataset for Siamese training.

Generates reference-candidate pairs on-the-fly using the synthetic generator.
Implements hard negative mining strategy:
  - Positive: reference ↔ true match crop (same physical site)
  - Hard Negative: reference ↔ periodic alias crop (±1 pitch offset)
  - Random Negative: reference ↔ distant region
"""

# TODO: Implement in Phase 4


class SiameseDataset:
    """
    On-the-fly dataset for Siamese training with hard negative mining.

    Generates positive, hard-negative, and random-negative pairs
    using the synthetic SEM generator.
    """

    def __init__(self, generator, config: dict):
        self.generator = generator
        self.config = config

    def __len__(self):
        return self.config.get("num_train_pairs", 50000)

    def __getitem__(self, idx):
        """
        Generate a training sample.

        Returns:
            Dict with 'reference', 'positive', 'hard_negative', 'random_negative'.
        """
        # TODO: Implement
        raise NotImplementedError
