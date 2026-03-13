"""
Unit tests for Ocean Sink module
"""

import pytest
from carbonica.modules.ocean_sink import OceanSinkModel


class TestOceanSink:
    """Test Ocean Sink module"""
    
    def test_initialization(self):
        """Test initialization"""
        ocean = OceanSinkModel()
        assert ocean is not None
        assert hasattr(ocean, 'revelle_ref')
        assert hasattr(ocean, 'ocean_sink_ref')
    
    def test_get_revelle_factor(self):
        """Test Revelle Factor retrieval"""
        ocean = OceanSinkModel()
        
        R_1960 = ocean.get_revelle_factor(1960)
        assert 10.1 <= R_1960 <= 10.3  # Paper: 10.2
        
        R_2025 = ocean.get_revelle_factor(2025)
        assert 12.3 <= R_2025 <= 12.5  # Paper: 12.4
    
    def test_get_buffer_capacity(self):
        """Test buffer capacity calculation"""
        ocean = OceanSinkModel()
        
        beta_2025 = ocean.get_buffer_capacity(2025)
        assert 0.080 <= beta_2025 <= 0.082  # 1/12.4 ≈ 0.081
    
    def test_get_sink_strength(self):
        """Test ocean sink strength"""
        ocean = OceanSinkModel()
        
        S_2025 = ocean.get_sink_strength(2025)
        assert -3.10 <= S_2025 <= -3.06  # Paper: -3.08
    
    def test_gas_transfer(self):
        """Test gas transfer velocity"""
        ocean = OceanSinkModel()
        
        # Wanninkhof (2014) formula
        k_w = ocean.compute_gas_transfer(wind_speed=7.0, temperature=20.0)
        assert k_w > 0
    
    def test_co2_solubility(self):
        """Test CO₂ solubility"""
        ocean = OceanSinkModel()
        
        K0 = ocean.compute_co2_solubility(temperature=20.0)
        assert K0 > 0
        
        # Solubility decreases with temperature
        K0_warm = ocean.compute_co2_solubility(temperature=25.0)
        K0_cold = ocean.compute_co2_solubility(temperature=15.0)
        assert K0_cold > K0_warm
    
    def test_air_sea_flux(self):
        """Test air-sea flux calculation"""
        ocean = OceanSinkModel()
        
        flux = ocean.compute_air_sea_flux(
            pco2_atm=420,
            pco2_sw=400,
            wind_speed=7.0,
            temperature=20.0
        )
        
        # Should be negative (ocean sink) when atm > ocean
        assert flux < 0
    
    def test_project_revelle(self):
        """Test Revelle Factor projection"""
        ocean = OceanSinkModel()
        
        proj = ocean.project_revelle(end_year=2050)
        assert len(proj) > 0
        
        # Should increase
        assert proj[0][1] < proj[-1][1]
    
    def test_ocean_uptake_efficiency(self):
        """Test ocean uptake efficiency"""
        ocean = OceanSinkModel()
        
        eff_2025 = ocean.get_ocean_uptake_efficiency(2025)
        assert 0.27 <= eff_2025 <= 0.29  # 28%
        
        eff_2060 = ocean.get_ocean_uptake_efficiency(2060)
        assert 0.17 <= eff_2060 <= 0.19  # 18%
