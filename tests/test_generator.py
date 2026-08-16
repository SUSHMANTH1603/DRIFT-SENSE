import yaml
import pytest
import numpy as np
from generator.dram import DRAMGenerator
from generator.finfet import FinFETGenerator
from generator.sem_model import SEMDegradationModel, SEMParams
from generator.noise import NoiseModel, REFERENCE_NOISE, SEARCH_NOISE

# Mock/Default generator config
CONFIG_DATA = """
fov:
  reference_um: 1.0
  search_um: 10.0
  image_size_px: 1000
  continuous_layout_um: 12.0
styles:
  DRAM:
    pitch_range_nm: [45, 75]
    contact_ratio: [0.4, 0.6]
    line_width_ratio: [0.3, 0.5]
    ler_sigma_nm: [1.0, 2.5]
    ler_corr_nm: [10, 30]
    cd_variation_3sigma: 0.05
  FinFET:
    fin_pitch_nm: [24, 48]
    fin_width_nm: [6, 10]
    gate_pitch_nm: [48, 96]
    gate_length_nm: [12, 18]
    ler_fin_sigma_nm: [0.8, 2.0]
    ler_gate_sigma_nm: [1.0, 2.5]
"""
DEFAULT_CONFIG = yaml.safe_load(CONFIG_DATA)


class TestDRAMGenerator:
    """Tests for DRAM structure generation."""

    def test_generator_creates_valid_pair(self):
        """Generated pair should have correct shapes and types."""
        gen = DRAMGenerator(DEFAULT_CONFIG, seed=42)
        ref_img, search_img, meta = gen.generate_pair()
        
        assert ref_img.shape == (1000, 1000)
        assert search_img.shape == (1000, 1000)
        assert ref_img.dtype == np.float32
        assert search_img.dtype == np.float32
        assert meta.style == "DRAM"
        assert len(meta.pair_id) > 0

    def test_independent_noise_realizations(self):
        """Reference and search must have independent noise."""
        gen = DRAMGenerator(DEFAULT_CONFIG, seed=42)
        ref_img, search_img, _ = gen.generate_pair()
        
        # Even if reference and search regions were identical (which they are not),
        # noise must be independent
        assert not np.array_equal(ref_img, search_img)

    def test_ground_truth_within_search(self):
        """Ground truth center must be within search image bounds."""
        gen = DRAMGenerator(DEFAULT_CONFIG, seed=42)
        _, _, meta = gen.generate_pair()
        
        # Search image coords are 1000x1000 px
        assert 0.0 <= meta.ground_truth_x <= 1000.0
        assert 0.0 <= meta.ground_truth_y <= 1000.0

    def test_reproducibility_with_seed(self):
        """Same seed should produce identical pairs."""
        gen1 = DRAMGenerator(DEFAULT_CONFIG, seed=42)
        gen2 = DRAMGenerator(DEFAULT_CONFIG, seed=42)
        
        ref1, srch1, meta1 = gen1.generate_pair()
        ref2, srch2, meta2 = gen2.generate_pair()
        
        assert np.array_equal(ref1, ref2)
        assert np.array_equal(srch1, srch2)
        assert meta1.ground_truth_x == meta2.ground_truth_x
        assert meta1.ground_truth_y == meta2.ground_truth_y


class TestFinFETGenerator:
    """Tests for FinFET structure generation."""

    def test_generator_creates_valid_pair(self):
        gen = FinFETGenerator(DEFAULT_CONFIG, seed=100)
        ref_img, search_img, meta = gen.generate_pair()
        
        assert ref_img.shape == (1000, 1000)
        assert search_img.shape == (1000, 1000)
        assert meta.style == "FinFET"


class TestSEMDegradation:
    """Tests for SEM physics degradation model."""

    def test_edge_brightening_increases_edge_intensity(self):
        # Create a simple step edge image
        img = np.zeros((100, 100), dtype=np.float32)
        img[:, 50:] = 0.5
        
        params = SEMParams(
            blur_sigma_px=0.0,
            edge_brightening_alpha=0.5,
            charging_amplitude=0.0,
            scan_distortion_amplitude_px=0.0
        )
        model = SEMDegradationModel(params, np.random.default_rng(42))
        degraded = model.apply(img)
        
        # Edge pixels around col 50 should show intensity increase due to gradient
        assert np.max(degraded) > 0.5

    def test_noise_increases_variance(self):
        # A perfectly flat image
        img = np.ones((100, 100), dtype=np.float32) * 0.5
        
        noise_model = NoiseModel(REFERENCE_NOISE, np.random.default_rng(42))
        noisy = noise_model.apply(img)
        
        assert np.var(noisy) > 0.0
        assert np.mean(noisy) == pytest.approx(0.5, abs=0.05)

    def test_search_noisier_than_reference(self):
        """Search image must have higher noise variance than reference on a flat target."""
        img = np.ones((200, 200), dtype=np.float32) * 0.5
        
        ref_noise = NoiseModel(REFERENCE_NOISE, np.random.default_rng(42))
        search_noise = NoiseModel(SEARCH_NOISE, np.random.default_rng(42))
        
        ref_noisy = ref_noise.apply(img)
        search_noisy = search_noise.apply(img)
        
        # Search noise params has larger shot_scale (3.0 vs 1.0)
        assert np.var(search_noisy) > np.var(ref_noisy)

