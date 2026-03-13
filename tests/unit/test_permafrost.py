"""
Unit tests for Permafrost Engine module
"""

import pytest
from carbonica.modules.permafrost_engine import PermafrostEngine


class TestPermafrost:
    """Test Permafrost Engine module"""
    
    def test_initialization(self):
        """Test initialization"""
        perma = PermafrostEngine()
        assert perma is not None
        assert hasattr(perma, 'permaflux_ref')
        assert hasattr(perma, 'q10_values')
    
    def test_get_flux(self):
        """Test permafrost flux retrieval"""
        perma = PermafrostEngine()
        
        F_1990 = perma.get_flux(1990)
        assert F_1990 <= 0.1  # Near zero in 1990
        
        F_2025 = perma.get_flux(2025)
        assert 1.6 <= F_2025 <= 1.8  # Paper: 1.71
    
    def test_compute_decomposition_rate(self):
        """Test decomposition rate calculation"""
        perma = PermafrostEngine()
        
        # Q10 = 2, 10°C warming → 2x rate
        rate = perma.compute_decomposition_rate(temperature_anomaly=10, q10=2)
        assert abs(rate - 2.0) < 0.1
        
        # Q10 = 3, 10°C warming → 3x rate
        rate = perma.compute_decomposition_rate(temperature_anomaly=10, q10=3)
        assert abs(rate - 3.0) < 0.1
    
    def test_compute_flux(self):
        """Test flux calculation"""
        perma = PermafrostEngine()
        
        flux = perma.compute_flux(
            carbon_density=28.1,
            area=1e12,  # 1 million km²
            temperature_anomaly=2.0,
            q10=2.5
        )
        
        assert flux > 0
    
    def test_get_abrupt_thaw_fraction(self):
        """Test abrupt thaw fraction"""
        perma = PermafrostEngine()
        
        frac_2025 = perma.get_abrupt_thaw_fraction(2025)
        assert 0.30 <= frac_2025 <= 0.32  # Paper: 31%
        
        # Should increase over time
        frac_2040 = perma.get_abrupt_thaw_fraction(2040)
        assert frac_2040 > frac_2025
    
    def test_separate_thaw_types(self):
        """Test separation of thaw types"""
        perma = PermafrostEngine()
        
        components = perma.separate_thaw_types(total_flux=1.71, year=2025)
        
        assert abs(components['total'] - 1.71) < 0.01
        assert components['gradual'] + components['abrupt'] == components['total']
        assert 0.30 <= components['abrupt_fraction'] <= 0.32
    
    def test_project_flux(self):
        """Test flux projection"""
        perma = PermafrostEngine()
        
        proj = perma.project_flux(end_year=2050)
        assert len(proj) > 0
        assert proj[0][1] < proj[-1][1]  # Increasing
    
    def test_get_critical_year(self):
        """Test critical year retrieval"""
        perma = PermafrostEngine()
        
        year = perma.get_critical_year('SSP3-7.0')
        assert 2038 <= year <= 2046  # Paper range
    
    def test_get_esas_risk_year(self):
        """Test ESAS risk window"""
        perma = PermafrostEngine()
        
        start, end = perma.get_esas_risk_year()
        assert start == 2031
        assert end == 2044
    
    def test_summary(self):
        """Test summary generation"""
        perma = PermafrostEngine()
        
        summary = perma.summary()
        assert 'Permafrost' in summary
        assert 'flux' in summary
        assert 'PgC/yr' in summary
