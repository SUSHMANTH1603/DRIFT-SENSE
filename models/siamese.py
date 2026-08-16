"""
Siamese verification network.

Architecture: MobileNetV3-Small (0.35M params) with metric learning head.
Used ONLY as a fallback when classical pipeline cannot resolve periodic aliases.

Input: 128×128 context crops (reference + candidate)
Output: 128-d L2-normalized embedding
Similarity: Cosine similarity between embeddings

References:
  [29] Zagoruyko & Komodakis, CVPR 2015 (Siamese networks)
  MobileNetV3: Howard et al., ICCV 2019
"""

# TODO: Implement in Phase 4
# Skeleton only — implementation gated on classical accuracy results


class SiameseVerifier:
    """
    Siamese verification network for periodic alias disambiguation.

    Architecture:
        Reference Context (128×128) → MobileNetV3-Small → L2-normalize → 128-d
        Candidate Context (128×128) → MobileNetV3-Small (shared) → L2-normalize → 128-d
                                                                       ↓
                                                                Cosine Similarity
    """

    def __init__(self, backbone: str = "mobilenetv3_small", embed_dim: int = 128):
        self.backbone_name = backbone
        self.embed_dim = embed_dim
        # TODO: Build PyTorch module

    def forward(self, x):
        """Compute L2-normalized embedding."""
        # TODO: Implement
        raise NotImplementedError

    def verify_candidates(self, reference_crop, candidate_crops):
        """
        Score multiple candidates against a reference crop.

        Args:
            reference_crop: 128×128 reference context.
            candidate_crops: List of 128×128 candidate contexts.

        Returns:
            List of cosine similarity scores.
        """
        # TODO: Implement
        raise NotImplementedError
