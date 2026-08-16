"""
SEM imaging physics degradation model.

Models the physical effects of scanning electron microscopy:
  - Edge brightening (secondary electron yield at topography edges)
  - PSF/beam blur
  - Charging artifacts
  - Scan distortion

References:
  [1] Joy, SEM Physics (1995)
  [2] Goldstein et al., SEM and X-ray Microanalysis (2018)
  [5] KLA-Tencor US7230658, US8120645
  [6] Applied Materials US20190122688
  [7] ASML US20150364221
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np


import cv2

@dataclass
class SEMParams:
    """Parameters for the SEM degradation model."""

    blur_sigma_px: float = 1.5
    edge_brightening_alpha: float = 0.2
    charging_amplitude: float = 0.05
    charging_poly_order: int = 3
    scan_distortion_amplitude_px: float = 1.5
    contrast_gain: float = 1.0
    brightness_offset: float = 0.0


class SEMDegradationModel:
    """
    Applies physically-motivated SEM imaging degradations.

    Each degradation corresponds to a known SEM imaging artifact
    with citations to semiconductor imaging literature.
    """

    def __init__(self, params: Optional[SEMParams] = None, rng: Optional[np.random.Generator] = None):
        self.params = params or SEMParams()
        self.rng = rng or np.random.default_rng()

    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the full SEM degradation pipeline to a clean image.

        Pipeline order:
        1. Edge brightening (secondary electron yield)
        2. PSF blur (Gaussian beam profile)
        3. Contrast/brightness variation
        4. Charging artifact (surface potential variation)
        5. Scan distortion (thin-plate spline/displacement warp)

        Args:
            image: Clean structure image (float, [0, 1]).

        Returns:
            Degraded image with SEM artifacts.
        """
        img = image.copy()
        img = self.apply_edge_brightening(img)
        img = self.apply_psf_blur(img)
        img = img * self.params.contrast_gain + self.params.brightness_offset
        img = self.apply_charging(img)
        img = self.apply_scan_distortion(img)
        return np.clip(img, 0.0, 1.0)

    def apply_edge_brightening(self, image: np.ndarray) -> np.ndarray:
        """I_edge = I * (1 + alpha * |grad(h)|)"""
        dx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        dy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        grad_mag = np.sqrt(dx**2 + dy**2)
        
        max_grad = np.max(grad_mag)
        if max_grad > 0:
            grad_mag = grad_mag / max_grad
            
        edge_brightened = image * (1.0 + self.params.edge_brightening_alpha * grad_mag)
        return edge_brightened

    def apply_psf_blur(self, image: np.ndarray) -> np.ndarray:
        """Gaussian beam profile + box scan integration."""
        if self.params.blur_sigma_px <= 0.0:
            return image
        # Gaussian blur approximates the beam profile PSF
        blurred = cv2.GaussianBlur(image, (0, 0), self.params.blur_sigma_px)
        return blurred

    def apply_charging(self, image: np.ndarray) -> np.ndarray:
        """Low-frequency 2D polynomial/sinusoidal multiplicative field."""
        if self.params.charging_amplitude <= 0.0:
            return image
        h, w = image.shape
        y = np.linspace(-1, 1, h)
        x = np.linspace(-1, 1, w)
        X, Y = np.meshgrid(x, y)
        
        # Generate low-frequency charging variation using random coefficients
        coeffs = self.rng.normal(0.0, 1.0, 4)
        charging_field = (
            coeffs[0] * np.sin(np.pi * X) +
            coeffs[1] * np.cos(np.pi * Y) +
            coeffs[2] * np.sin(np.pi * X * Y) +
            coeffs[3] * X**2
        )
        
        # Normalize to [-1, 1] range
        c_min, c_max = np.min(charging_field), np.max(charging_field)
        if c_max > c_min:
            charging_field = (charging_field - c_min) / (c_max - c_min)
            charging_field = 2.0 * charging_field - 1.0
        else:
            charging_field = np.zeros_like(charging_field)
            
        # Multiplicative field: [1 - amp, 1 + amp]
        mult_field = 1.0 + self.params.charging_amplitude * charging_field
        return image * mult_field

    def apply_scan_distortion(self, image: np.ndarray) -> np.ndarray:
        """Warp mapping for nonlinear scan coil response."""
        if self.params.scan_distortion_amplitude_px <= 0.0:
            return image
        h, w = image.shape
        y = np.linspace(-1, 1, h)
        x = np.linspace(-1, 1, w)
        X, Y = np.meshgrid(x, y)
        
        # Low frequency displacement field
        coeffs_x = self.rng.normal(0.0, 1.0, 2)
        coeffs_y = self.rng.normal(0.0, 1.0, 2)
        
        dx_field = self.params.scan_distortion_amplitude_px * (
            coeffs_x[0] * np.sin(np.pi * Y) + coeffs_x[1] * Y
        )
        dy_field = self.params.scan_distortion_amplitude_px * (
            coeffs_y[0] * np.cos(np.pi * X) + coeffs_y[1] * X
        )
        
        # Map original pixel grid to distorted coordinates
        map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
        map_x = (map_x + dx_field).astype(np.float32)
        map_y = (map_y + dy_field).astype(np.float32)
        
        # Remap image with linear interpolation
        distorted = cv2.remap(
            image,
            map_x,
            map_y,
            cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101
        )
        return distorted
