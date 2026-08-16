"""
Siamese model training script.

Usage:
    python -m training.train --config configs/siamese.yaml

Only execute if classical pipeline accuracy < 95% on hard test set (Phase 4).
"""

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Train Siamese fallback model")
    parser.add_argument("--config", type=str, default="configs/siamese.yaml")
    parser.add_argument("--resume", type=str, default=None, help="Checkpoint to resume from")
    parser.add_argument("--gpus", type=int, default=1)
    return parser.parse_args()


def main():
    """Main training entry point."""
    args = parse_args()
    # TODO: Implement in Phase 4
    # 1. Load config
    # 2. Create generator + dataset
    # 3. Build model
    # 4. Train with PyTorch Lightning
    # 5. Export to ONNX
    raise NotImplementedError("Training not yet implemented (Phase 4)")


if __name__ == "__main__":
    main()
