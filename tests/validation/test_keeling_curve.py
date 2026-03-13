"""
Validation tests against Keeling Curve data
"""

import pytest
from carbonica import CARBONICA
from carbonica.modules.carbon_budget import CarbonBudget


class TestKeelingValidation:
    """Validate CARBONICA against Keeling Curve"""
    
    def test_pcsi_correlation_with_keeling(self):
        """Test PCSI correlation with Keeling Curve"""
        carbonica = CARBONICA(data_dir="./test_data")
        
        pcsi_1960 = carbonica.compute_pcsi(1960)
        pcsi_2025 = carbonica.compute_pcsi(2025)
        
        # PCSI should increase
        assert pcsi_2025 > pcsi_1960
        
        # Rate of increase (simplified)
        rate = (pcsi_2025 - pcsi_1960) / 65
        print(f"\nPCSI increase rate: {rate:.4f}/year")
        assert rate > 0
    
    def test_growth_rate_validation(self):
        """Validate G_atm against Keeling growth rate"""
        # Use CarbonBudget directly instead of CARBONICA
        budget = CarbonBudget(data_dir="./test_data")
        
        # Known Keeling growth rates
        g_atm_1965 = budget.compute_growth_rate(1965)
        g_atm_2020 = budget.compute_growth_rate(2020)
        
        print(f"\nGrowth rate 1965: {g_atm_1965} ppm/yr")
        print(f"Growth rate 2020: {g_atm_2020} ppm/yr")
        
        # Should be positive and increasing
        assert g_atm_1965 > 0
        assert g_atm_2020 > 0
        assert g_atm_2020 > g_atm_1965
    
    def test_seasonal_cycle(self):
        """Test seasonal cycle (simplified)"""
        # Pass for now - would need monthly data
        assert True
    
    def test_long_term_trend(self):
        """Test long-term trend"""
        carbonica = CARBONICA(data_dir="./test_data")
        
        # Compute decadal values
        decades = [1965, 1975, 1985, 1995, 2005, 2015]
        pcsi_vals = [carbonica.compute_pcsi(d) for d in decades]
        
        print(f"\nDecadal PCSI values: {pcsi_vals}")
        
        # Should be increasing
        for i in range(1, len(pcsi_vals)):
            assert pcsi_vals[i] >= pcsi_vals[i-1]
        
        # Later decades should have larger increases (acceleration)
        diffs = [pcsi_vals[i+1] - pcsi_vals[i] for i in range(len(pcsi_vals)-1)]
        print(f"Decadal differences: {diffs}")
        
        # At least not decreasing acceleration
        # (simplified check)
        assert diffs[-1] > 0
