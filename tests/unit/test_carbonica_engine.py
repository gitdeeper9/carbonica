"""
Unit tests for CARBONICA main engine
"""

import pytest
import os
import json
from carbonica import CARBONICA


class TestCARBONICA:
    """Test CARBONICA main engine"""
    
    def test_initialization(self, carbonica_instance):
        """Test engine initialization"""
        assert carbonica_instance is not None
        assert carbonica_instance.data_dir is not None
        assert hasattr(carbonica_instance, 'REFERENCE_VALUES')
        assert hasattr(carbonica_instance, 'PCSI_WEIGHTS')
    
    def test_reference_values(self, carbonica_instance):
        """Test reference values"""
        ref = carbonica_instance.REFERENCE_VALUES
        
        assert 'pi' in ref
        assert '1960' in ref
        assert '2025' in ref
        assert 'critical' in ref
        
        # Check 2025 values from paper
        assert ref['2025']['NPP'] == 58.3
        assert ref['2025']['S_ocean'] == -3.08
        assert ref['2025']['G_atm'] == 2.38
        assert ref['2025']['F_perma'] == 1.71
        assert ref['2025']['beta'] == 0.081
        assert ref['2025']['tau_soil'] == 27
        assert ref['2025']['E_anth'] == 11.2
        assert ref['2025']['Phi_q'] == 0.071
    
    def test_pcsi_weights(self, carbonica_instance):
        """Test PCSI weights"""
        weights = carbonica_instance.PCSI_WEIGHTS
        
        assert abs(sum(weights.values()) - 1.0) < 0.01
        assert weights['NPP'] == 0.16
        assert weights['S_ocean'] == 0.18
        assert weights['G_atm'] == 0.20
        assert weights['F_perma'] == 0.19
        assert weights['beta'] == 0.12
        assert weights['tau_soil'] == 0.07
        assert weights['E_anth'] == 0.05
        assert weights['Phi_q'] == 0.03
    
    def test_normalize_parameter(self, carbonica_instance):
        """Test parameter normalization"""
        # Test NPP (decreasing)
        npp_norm = carbonica_instance.normalize_parameter('NPP', 58.3)
        assert 0.22 <= npp_norm <= 0.24  # Should be ~0.23
        
        # Test G_atm (increasing)
        gatm_norm = carbonica_instance.normalize_parameter('G_atm', 2.38)
        assert 0.67 <= gatm_norm <= 0.69  # Should be ~0.68
        
        # Test boundary conditions
        assert carbonica_instance.normalize_parameter('NPP', 60.2) == 0.0  # PI
        assert carbonica_instance.normalize_parameter('NPP', 52.0) == 1.0  # Critical
    
    def test_compute_pcsi_2025(self, carbonica_instance, sample_parameters_2025):
        """Test PCSI calculation for 2025"""
        pcsi = carbonica_instance.compute_pcsi(2025, sample_parameters_2025)
        assert 0.77 <= pcsi <= 0.79  # Paper says 0.78
    
    def test_compute_pcsi_1960(self, carbonica_instance, sample_parameters_1960):
        """Test PCSI calculation for 1960"""
        pcsi = carbonica_instance.compute_pcsi(1960, sample_parameters_1960)
        assert 0.30 <= pcsi <= 0.32  # Paper says 0.31
    
    def test_get_parameter(self, carbonica_instance):
        """Test parameter retrieval"""
        npp = carbonica_instance.get_parameter('NPP', 2025)
        assert npp == 58.3
        
        gatm = carbonica_instance.get_parameter('G_atm', 1960)
        assert gatm == 0.90
    
    def test_update_parameter(self, carbonica_instance):
        """Test parameter update"""
        carbonica_instance.update_parameter('NPP', 60.0, 2025)
        assert carbonica_instance.get_parameter('NPP', 2025) == 60.0
    
    def test_pcsi_status(self, carbonica_instance):
        """Test PCSI status strings"""
        assert 'STABLE' in carbonica_instance.get_pcsi_status(0.5)
        assert 'TRANSITIONAL' in carbonica_instance.get_pcsi_status(0.7)
        assert 'CRITICAL' in carbonica_instance.get_pcsi_status(0.9)
    
    def test_save_load_json(self, carbonica_instance, temp_data_dir):
        """Test JSON save/load"""
        # Save
        json_file = f"{temp_data_dir}/test.json"
        carbonica_instance.save_to_json(json_file)
        
        # Check file exists
        assert os.path.exists(json_file)
        
        # Load into new instance
        new_instance = CARBONICA(data_dir=temp_data_dir)
        new_instance.load_from_json(json_file)
        
        # Compare
        assert new_instance.compute_pcsi(2025) == carbonica_instance.compute_pcsi(2025)
    
    def test_summary(self, carbonica_instance):
        """Test summary generation"""
        summary = carbonica_instance.summary()
        assert 'CARBONICA v1.0.0' in summary
        assert 'PCSI' in summary
        assert 'NPP' in summary
