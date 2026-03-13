"""
Unit tests for PCSI calculator
"""

import pytest
import tempfile
import json
from carbonica.pcsi import PCSI


class TestPCSI:
    """Test PCSI calculator"""
    
    def test_initialization(self):
        """Test PCSI initialization"""
        pcsi = PCSI()
        assert pcsi.weights is not None
        assert len(pcsi.weights) == 8
    
    def test_default_weights(self):
        """Test default weights"""
        pcsi = PCSI()
        assert pcsi.weights['NPP'] == 0.16
        assert pcsi.weights['S_ocean'] == 0.18
        assert pcsi.weights['G_atm'] == 0.20
        assert pcsi.weights['F_perma'] == 0.19
        assert pcsi.weights['beta'] == 0.12
        assert pcsi.weights['tau_soil'] == 0.07
        assert pcsi.weights['E_anth'] == 0.05
        assert pcsi.weights['Phi_q'] == 0.03
    
    def test_custom_weights(self):
        """Test custom weights"""
        custom = {'NPP': 0.2, 'G_atm': 0.8}
        pcsi = PCSI(weights=custom)
        assert abs(sum(pcsi.weights.values()) - 1.0) < 0.01
    
    def test_normalize_decreasing(self):
        """Test normalization of decreasing parameters"""
        pcsi = PCSI()
        
        # NPP: pre-industrial 60.2, critical 52.0
        assert pcsi.normalize('NPP', 60.2) == 0.0  # PI
        assert pcsi.normalize('NPP', 56.1) == 0.5  # Midpoint
        assert pcsi.normalize('NPP', 52.0) == 1.0  # Critical
        assert pcsi.normalize('NPP', 50.0) == 1.0  # Capped
    
    def test_normalize_increasing(self):
        """Test normalization of increasing parameters"""
        pcsi = PCSI()
        
        # G_atm: pre-industrial 0.002, critical 3.5
        assert pcsi.normalize('G_atm', 0.002) == 0.0  # PI
        assert pcsi.normalize('G_atm', 1.751) == 0.5  # Midpoint
        assert pcsi.normalize('G_atm', 3.5) == 1.0  # Critical
        assert pcsi.normalize('G_atm', 4.0) == 1.0  # Capped
    
    def test_compute_2025(self, sample_parameters_2025):
        """Test compute for 2025 values"""
        pcsi = PCSI()
        result = pcsi.compute(sample_parameters_2025)
        assert 0.77 <= result <= 0.79
    
    def test_compute_1960(self, sample_parameters_1960):
        """Test compute for 1960 values"""
        pcsi = PCSI()
        result = pcsi.compute(sample_parameters_1960)
        assert 0.30 <= result <= 0.32
    
    def test_compute_all(self, sample_parameters_2025, sample_parameters_1960):
        """Test compute multiple"""
        pcsi = PCSI()
        results = pcsi.compute_all([sample_parameters_1960, sample_parameters_2025])
        assert len(results) == 2
        assert results[0] < results[1]
    
    def test_status(self):
        """Test status strings"""
        pcsi = PCSI()
        assert 'STABLE' in pcsi.get_status(0.5)
        assert 'TRANSITIONAL' in pcsi.get_status(0.7)
        assert 'CRITICAL' in pcsi.get_status(0.9)
    
    def test_colors(self):
        """Test color codes"""
        pcsi = PCSI()
        assert pcsi.get_color(0.5) == 'green'
        assert pcsi.get_color(0.7) == 'yellow'
        assert pcsi.get_color(0.9) == 'red'
    
    def test_emoji(self):
        """Test emoji codes"""
        pcsi = PCSI()
        assert pcsi.get_emoji(0.5) == '🟢'
        assert pcsi.get_emoji(0.7) == '🟡'
        assert pcsi.get_emoji(0.9) == '🔴'
    
    def test_to_dict(self):
        """Test dictionary export"""
        pcsi = PCSI()
        data = pcsi.to_dict()
        assert 'pre_industrial' in data
        assert 'critical_thresholds' in data
        assert 'weights' in data
    
    def test_save_load_json(self):
        """Test JSON save/load"""
        pcsi = PCSI()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as f:
            pcsi.save_to_json(f.name)
            
            # Load into new instance
            pcsi2 = PCSI.from_json(f.name)
            
            # Compare
            assert pcsi2.weights == pcsi.weights
    
    def test_pre_industrial_values(self):
        """Test pre-industrial values from paper"""
        pcsi = PCSI()
        assert pcsi.PRE_INDUSTRIAL['NPP'] == 60.2
        assert pcsi.PRE_INDUSTRIAL['S_ocean'] == -0.18
        assert pcsi.PRE_INDUSTRIAL['G_atm'] == 0.002
        assert pcsi.PRE_INDUSTRIAL['beta'] == 0.110
    
    def test_critical_thresholds(self):
        """Test critical thresholds from paper"""
        pcsi = PCSI()
        assert pcsi.CRITICAL_THRESHOLDS['NPP'] == 52.0
        assert pcsi.CRITICAL_THRESHOLDS['S_ocean'] == -1.5
        assert pcsi.CRITICAL_THRESHOLDS['G_atm'] == 3.5
        assert pcsi.CRITICAL_THRESHOLDS['F_perma'] == 2.8
