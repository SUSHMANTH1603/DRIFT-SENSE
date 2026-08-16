"""
DRAM structure generator.

Generates synthetic DRAM array patterns with word lines, bit lines,
contacts, and realistic line edge roughness (LER).

Physical parameters sourced from:
  - IRDS 2022 (pitch ranges)
  - Kim et al. ISSCC 2020 (DRAM geometry)
  - IMEC J. Micro/Nanolith. 2017 (LER statistics)
  - SPIE 2018 (CD variation)
"""

import numpy as np

from generator.base import SemiconductorGenerator


from generator.utils import generate_ler

class DRAMGenerator(SemiconductorGenerator):
    """
    DRAM array pattern generator.

    Layout: horizontal word lines + vertical bit lines + contacts at intersections.
    """

    def __init__(self, config: dict, seed: int = 42):
        super().__init__(config, seed)
        self.style = "DRAM"

    def generate_continuous_layout(self, size_um: float = 12.0) -> np.ndarray:
        """
        Generate a continuous DRAM array layout.

        Creates a grid of word lines and bit lines with:
        - Configurable pitch (45-75 nm range)
        - Contact dots at intersections
        - Line edge roughness (LER)
        - Critical dimension (CD) variation

        Args:
            size_um: Physical extent in micrometers.

        Returns:
            Float array of shape (12000, 12000) at 1 nm/px resolution.
        """
        # Continuous size in pixels (1 nm/px)
        size_px = int(size_um * 1000)
        
        # Load parameters
        params = self.config.get("styles", {}).get("DRAM", {})
        pitch_range = params.get("pitch_range_nm", [45, 75])
        contact_range = params.get("contact_ratio", [0.4, 0.6])
        width_range = params.get("line_width_ratio", [0.3, 0.5])
        ler_sigma_range = params.get("ler_sigma_nm", [1.0, 2.5])
        ler_corr_range = params.get("ler_corr_nm", [10, 30])
        cd_var_3sigma = params.get("cd_variation_3sigma", 0.05)
        
        # Draw randomized process parameters (process variation)
        pitch_wl = self.rng.uniform(pitch_range[0], pitch_range[1])
        pitch_bl = self.rng.uniform(pitch_range[0], pitch_range[1])
        
        contact_ratio = self.rng.uniform(contact_range[0], contact_range[1])
        line_width_ratio = self.rng.uniform(width_range[0], width_range[1])
        
        ler_sigma_nm = self.rng.uniform(ler_sigma_range[0], ler_sigma_range[1])
        ler_corr_nm = self.rng.uniform(ler_corr_range[0], ler_corr_range[1])
        
        # Apply global CD variation (3-sigma)
        cd_scale = self.rng.normal(1.0, cd_var_3sigma / 3.0)
        
        wl_width = pitch_wl * line_width_ratio * cd_scale
        bl_width = pitch_bl * line_width_ratio * cd_scale
        contact_dia = ((pitch_wl + pitch_bl) / 2.0) * contact_ratio * cd_scale
        
        # 1. Word Lines (horizontal) LER profile along x
        ler_wl = generate_ler(size_px, ler_sigma_nm, ler_corr_nm, 1.0, self.rng)
        ler_wl_2d = ler_wl.reshape(1, -1)  # (1, size_px)
        
        y_idx = np.arange(size_px, dtype=np.float32).reshape(-1, 1)  # (size_px, 1)
        wl_dist = (y_idx - ler_wl_2d) % pitch_wl
        wl_mask = (wl_dist < wl_width / 2.0) | (wl_dist > pitch_wl - wl_width / 2.0)
        
        # 2. Bit Lines (vertical) LER profile along y
        ler_bl = generate_ler(size_px, ler_sigma_nm, ler_corr_nm, 1.0, self.rng)
        ler_bl_2d = ler_bl.reshape(-1, 1)  # (size_px, 1)
        
        x_idx = np.arange(size_px, dtype=np.float32).reshape(1, -1)  # (1, size_px)
        bl_dist = (x_idx - ler_bl_2d) % pitch_bl
        bl_mask = (bl_dist < bl_width / 2.0) | (bl_dist > pitch_bl - bl_width / 2.0)
        
        # 3. Contact Dots at intersections
        # Compute centered distances to get distance to closest intersection
        wl_dist_c = wl_dist.copy()
        wl_dist_c[wl_dist_c > pitch_wl / 2.0] -= pitch_wl
        
        bl_dist_c = bl_dist.copy()
        bl_dist_c[bl_dist_c > pitch_bl / 2.0] -= pitch_bl
        
        contact_radius = contact_dia / 2.0
        contact_mask = (wl_dist_c**2 + bl_dist_c**2) < contact_radius**2
        
        # 4. Construct height map (topography)
        layout = np.ones((size_px, size_px), dtype=np.float32) * 0.1  # Substrate height
        layout[wl_mask] = 0.4                                         # Word lines height
        layout[bl_mask] = 0.7                                         # Bit lines height
        layout[contact_mask] = 1.0                                    # Contacts height
        
        return layout
