"""
Dataset generation CLI.

Usage:
    python -m generator.generate_dataset --style DRAM --count 1000 --output data/generated/train
    python -m generator.generate_dataset --style FinFET --count 200 --output data/generated/test
"""

import argparse
import json
import os
from pathlib import Path

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate synthetic SEM image pairs for DRIFT-SENSE"
    )
    parser.add_argument(
        "--style",
        type=str,
        required=True,
        choices=["DRAM", "FinFET"],
        help="Semiconductor structure style",
    )
    parser.add_argument(
        "--count",
        type=int,
        required=True,
        help="Number of image pairs to generate",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory for generated pairs",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/generator.yaml",
        help="Path to generator configuration file",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="png",
        choices=["png", "npy", "h5"],
        help="Output image format",
    )
    return parser.parse_args()


import yaml
import cv2
from generator.dram import DRAMGenerator
from generator.finfet import FinFETGenerator

def main():
    """Main entry point for dataset generation."""
    args = parse_args()
    
    # 1. Load generator config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        
    print(f"[DRIFT-SENSE] Starting generation of {args.count} {args.style} pairs → {args.output}")
    os.makedirs(args.output, exist_ok=True)
    
    # 2. Loop to generate pairs
    for i in range(args.count):
        # Derive a unique seed for this pair to guarantee variety
        pair_seed = args.seed + i
        
        # Instantiate generator for this seed
        if args.style == "DRAM":
            gen = DRAMGenerator(config, seed=pair_seed)
        else:
            gen = FinFETGenerator(config, seed=pair_seed)
            
        try:
            ref_img, search_img, meta = gen.generate_pair()
            
            # Save files
            base_name = f"pair_{i:04d}"
            
            if args.format == "png":
                # Convert float32 [0.0, 1.0] to uint8 [0, 255]
                ref_u8 = (ref_img * 255.0).astype(np.uint8)
                search_u8 = (search_img * 255.0).astype(np.uint8)
                
                ref_path = os.path.join(args.output, f"{base_name}_ref.png")
                search_path = os.path.join(args.output, f"{base_name}_search.png")
                
                cv2.imwrite(ref_path, ref_u8)
                cv2.imwrite(search_path, search_u8)
            else:
                # Save as numpy arrays
                np.save(os.path.join(args.output, f"{base_name}_ref.npy"), ref_img)
                np.save(os.path.join(args.output, f"{base_name}_search.npy"), search_img)
                
            # Construct and save metadata dict matching configs/metadata_schema.json
            meta_dict = {
                "pair_id": meta.pair_id,
                "style": meta.style,
                "ground_truth": {
                    "x": float(meta.ground_truth_x),
                    "y": float(meta.ground_truth_y),
                    "scale": float(meta.scale),
                    "rotation_deg": float(meta.rotation_deg),
                },
                "noise_params": {
                    "reference": meta.noise_params_ref,
                    "search": meta.noise_params_search,
                },
                "structure_params": meta.structure_params,
                "seed": int(meta.seed),
            }
            
            meta_path = os.path.join(args.output, f"{base_name}_meta.json")
            with open(meta_path, "w") as f_meta:
                json.dump(meta_dict, f_meta, indent=2)
                
            if (i + 1) % max(1, args.count // 10) == 0 or i == args.count - 1:
                print(f"  Generated {i + 1}/{args.count} pairs...")
                
        except Exception as e:
            print(f"Error generating pair {i} (seed {pair_seed}): {str(e)}")
            raise e
            
    print(f"[DRIFT-SENSE] Completed generation of {args.count} pairs.")


if __name__ == "__main__":
    main()
