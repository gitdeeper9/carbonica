"""
Unit tests for Quantum Yield Tracker module
"""

import pytest
from carbonica.modules.quantum_yield_tracker import QuantumYieldTracker


class TestQuantumYield:
    """Test Quantum Yield Tracker module"""
    
    def test_initialization(self):
        """Test initialization"""
        qyt = QuantumYieldTracker()
        assert qyt is not None
        assert hasattr(qyt, 'phi_q_ref')
        assert hasattr(qyt, 'biome_phi_q')
    
    def test_get_quantum_yield(self):
        """Test quantum yield retrieval"""
        qyt = QuantumYieldTracker()
        
        phi_2009 = qyt.get_quantum_yield(2009)
        assert 0.076 <= phi_2009 <= 0.077
        
        phi_2025 = qyt.get_quantum_yield(2025)
        assert 0.071 <= phi_2025 <= 0.073
        
        # Should decrease over time
        assert phi_2009 > phi_2025
    
    def test_biome_specific(self):
        """Test biome-specific quantum yield"""
        qyt = QuantumYieldTracker()
        
        phi_amazon = qyt.get_quantum_yield(2025, 'amazon_tropical')
        phi_boreal = qyt.get_quantum_yield(2025, 'boreal_forest')
        
        assert phi_amazon < phi_boreal  # Amazon more stressed
    
    def test_compute_from_sif(self):
        """Test Φ_q computation from SIF"""
        qyt = QuantumYieldTracker()
        
        phi = qyt.compute_from_sif(sif=1.0, apar=1000)
        assert 0.0 <= phi <= 0.125  # Within theoretical range
    
    def test_detect_stress(self):
        """Test stress detection"""
        qyt = QuantumYieldTracker()
        
        # Normal conditions
        stressed, level = qyt.detect_stress(0.075, 'global_mean')
        assert not stressed
        assert 'NORMAL' in level
        
        # Stressed conditions
        stressed, level = qyt.detect_stress(0.050, 'amazon_tropical')
        assert stressed
        assert 'STRESS' in level
    
    def test_get_trend(self):
        """Test trend calculation"""
        qyt = QuantumYieldTracker()
        
        trend = qyt.get_trend(2009, 2025)
        
        assert trend['start_year'] == 2009
        assert trend['end_year'] == 2025
        assert trend['absolute_change'] < 0  # Decreasing
        assert trend['decline_rate_per_decade'] < 0
    
    def test_decline_rates(self):
        """Test biome decline rates"""
        qyt = QuantumYieldTracker()
        
        assert qyt.decline_rates['amazon_tropical'] == -2.1
        assert qyt.decline_rates['global_mean'] == -0.9
        assert qyt.decline_rates['boreal'] == 0.3  # Positive in boreal
    
    def test_summary(self):
        """Test summary generation"""
        qyt = QuantumYieldTracker()
        
        summary = qyt.summary()
        assert 'Quantum Yield' in summary
        assert 'Φ_q' in summary
        assert 'Amazon' in summary
