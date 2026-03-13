"""
Integration tests for CARBONICA full pipeline
"""

import pytest
import tempfile
from carbonica import CARBONICA
from carbonica.pcsi import PCSI


class TestFullPipeline:
    """Test complete CARBONICA pipeline"""
    
    def test_engine_integration(self):
        """Test engine initialization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            assert carbonica is not None
            assert hasattr(carbonica, 'ocean')
            assert hasattr(carbonica, 'permafrost')
            assert hasattr(carbonica, 'quantum')
            assert hasattr(carbonica, 'mc')
    
    def test_end_to_end_1960_2025(self):
        """Test PCSI from 1960 to 2025"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            
            # Known values from paper
            assert carbonica.compute_pcsi(1960) == 0.31
            assert carbonica.compute_pcsi(2025) == 0.78
            
            # Should be increasing
            pcsi_1970 = carbonica.compute_pcsi(1970)
            pcsi_1980 = carbonica.compute_pcsi(1980)
            pcsi_1990 = carbonica.compute_pcsi(1990)
            pcsi_2000 = carbonica.compute_pcsi(2000)
            pcsi_2010 = carbonica.compute_pcsi(2010)
            
            assert pcsi_1970 < pcsi_1980 < pcsi_1990 < pcsi_2000 < pcsi_2010
    
    def test_parameter_consistency(self):
        """Test parameter retrieval"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            
            params = carbonica.compute_current_state(2025)
            assert len(params) == 8
            assert 'NPP' in params
            assert params['NPP'] == 58.3
    
    def test_module_interactions(self):
        """Test modules are accessible"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            
            # Ocean module
            ocean_sink = carbonica.ocean.get_sink_strength(2025)
            assert ocean_sink < 0
            
            # Permafrost module
            perma_flux = carbonica.permafrost.get_flux(2025)
            assert perma_flux > 0
            
            # Quantum module
            phi_q = carbonica.quantum.get_quantum_yield(2025)
            assert 0.07 <= phi_q <= 0.08
    
    def test_save_load_workflow(self):
        """Test save and load"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica1 = CARBONICA(data_dir=tmpdir)
            pcsi1 = carbonica1.compute_pcsi(2025)
            
            json_file = f"{tmpdir}/test.json"
            carbonica1.save_to_json(json_file)
            
            carbonica2 = CARBONICA(data_dir=tmpdir)
            carbonica2.load_from_json(json_file)
            pcsi2 = carbonica2.compute_pcsi(2025)
            
            assert abs(pcsi1 - pcsi2) < 0.01
    
    def test_multiple_scenarios(self):
        """Test different years"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            
            for year in [1960, 1980, 2000, 2020]:
                params = carbonica.compute_current_state(year)
                assert params is not None
    
    def test_uncertainty_propagation(self):
        """Test Monte Carlo is accessible"""
        with tempfile.TemporaryDirectory() as tmpdir:
            carbonica = CARBONICA(data_dir=tmpdir)
            assert hasattr(carbonica, 'mc')
            assert carbonica.mc is not None
