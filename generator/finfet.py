"""
FinFET structure generator.

Generates synthetic FinFET patterns with fins, gates, gate-fin crossings,
and source/drain regions.

Physical parameters sourced from:
  - IRDS 2022 (pitch ranges)
  - Chen et al. IEDM 2019 (fin geometry)
  - Intel US20200258841 (gate dimensions)
  - SPIE 2020 (LER statistics)
"""

import numpy as np

from generator.base import SemiconductorGenerator


from generator.utils import generate_ler

class FinFETGenerator(SemiconductorGenerator):
    """
    FinFET pattern generator.

    Layout: vertical fins + horizontal gates + distinctive gate-fin crossings.
    """

    def __init__(self, config: dict, seed: int = 42):
        super().__init__(config, seed)
        self.style = "FinFET"

    def generate_continuous_layout(self, size_um: float = 12.0) -> np.ndarray:
        """
        Generate a continuous FinFET layout.

        Creates a pattern of fins and gates with:
        - Configurable fin pitch (24-48 nm) and width (6-10 nm)
        - Gate pitch (48-96 nm) and length (12-18 nm)
        - Fin-LER and gate-LER
        - Source/drain regions

        Args:
            size_um: Physical extent in micrometers.

        Returns:
            Float array of shape (12000, 12000) at 1 nm/px resolution.
        """
        # Continuous size in pixels (1 nm/px)
        size_px = int(size_um * 1000)
        
        # Load parameters
        params = self.config.get("styles", {}).get("FinFET", {})
        fin_pitch_range = params.get("fin_pitch_nm", [24, 48])
        fin_width_range = params.get("fin_width_nm", [6, 10])
        gate_pitch_range = params.get("gate_pitch_nm", [48, 96])
        gate_len_range = params.get("gate_length_nm", [12, 18])
        ler_fin_range = params.get("ler_fin_sigma_nm", [0.8, 2.0])
        ler_gate_range = params.get("ler_gate_sigma_nm", [1.0, 2.5])
        ler_corr_range = self.config.get("styles", {}).get("DRAM", {}).get("ler_corr_nm", [10, 30])  # Use correlation length range
        
        # Draw randomized process parameters
        pitch_fin = self.rng.uniform(fin_pitch_range[0], fin_pitch_range[1])
        pitch_gate = self.rng.uniform(gate_pitch_range[0], gate_pitch_range[1])
        
        fin_width = self.rng.uniform(fin_width_range[0], fin_width_range[1])
        gate_length = self.rng.uniform(gate_len_range[0], gate_len_range[1])
        
        ler_fin_sigma_nm = self.rng.uniform(ler_fin_range[0], ler_fin_range[1])
        ler_gate_sigma_nm = self.rng.uniform(ler_gate_range[0], ler_gate_range[1])
        ler_corr_nm = self.rng.uniform(ler_corr_range[0], ler_corr_range[1])
        
        # Apply global CD variation (3-sigma = 5%)
        cd_scale = self.rng.normal(1.0, 0.05 / 3.0)
        fin_width *= cd_scale
        gate_length *= cd_scale
        
        # 1. Fins (vertical) LER profile along y
        ler_fin = generate_ler(size_px, ler_fin_sigma_nm, ler_corr_nm, 1.0, self.rng)
        ler_fin_2d = ler_fin.reshape(-1, 1)  # (size_px, 1)
        
        x_idx = np.arange(size_px, dtype=np.float32).reshape(1, -1)  # (1, size_px)
        fin_dist = (x_idx - ler_fin_2d) % pitch_fin
        fin_mask = (fin_dist < fin_width / 2.0) | (fin_dist > pitch_fin - fin_width / 2.0)
        
        # 2. Gates (horizontal) LER profile along x
        ler_gate = generate_ler(size_px, ler_gate_sigma_nm, ler_corr_nm, 1.0, self.rng)
        ler_gate_2d = ler_gate.reshape(1, -1)  # (1, size_px)
        
        y_idx = np.arange(size_px, dtype=np.float32).reshape(-1, 1)  # (size_px, 1)
        gate_dist = (y_idx - ler_gate_2d) % pitch_gate
        gate_mask = (gate_dist < gate_length / 2.0) | (gate_dist > pitch_gate - gate_length / 2.0)
        
        # 3. Intersections (Gate-Fin crossings)
        crossing_mask = fin_mask & gate_mask
        
        # 4. Construct height map
        layout = np.ones((size_px, size_px), dtype=np.float32) * 0.1  # Substrate height
        layout[fin_mask] = 0.5                                         # Fins (source/drain) height
        layout[gate_mask] = 0.7                                        # Gates height
        layout[crossing_mask] = 1.0                                    # Crossings height
        
        return layout
