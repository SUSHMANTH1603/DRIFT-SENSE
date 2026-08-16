"""
DRIFT-SENSE: Main inference CLI.

Usage:
    python -m inference.infer reference.png search.png
    python -m inference.infer reference.png search.png --output result.json
    python -m inference.infer reference.png search.png --config configs/inference.yaml

Output (JSON):
    {"x": 512.34, "y": 487.21, "confidence": 0.92}
"""

import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="DRIFT-SENSE: Locate reference image within search image"
    )
    parser.add_argument("reference", type=str, help="Path to reference SEM image")
    parser.add_argument("search", type=str, help="Path to search SEM image")
    parser.add_argument(
        "--output",
        type=str,
        default="stdout",
        help="Output path (default: stdout)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/inference.yaml",
        help="Inference configuration file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include full metadata in output",
    )
    return parser.parse_args()


def main():
    """Main inference entry point."""
    args = parse_args()

    # TODO: Implement
    # 1. Load images (grayscale)
    # 2. Load config
    # 3. Create RegistrationEngine
    # 4. Run registration
    # 5. Output result as JSON

    result = {"x": 0.0, "y": 0.0, "confidence": 0.0}

    if args.output == "stdout":
        print(json.dumps(result, indent=2))
    else:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result saved to {args.output}")


if __name__ == "__main__":
    main()
