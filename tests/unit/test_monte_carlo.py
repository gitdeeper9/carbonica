"""
Unit tests for Monte Carlo uncertainty propagation
"""

import pytest
from carbonica.statistics.monte_carlo import MonteCarloPropagator


class TestMonteCarlo:
    """Test Monte Carlo propagator"""
    
    def test_initialization(self):
        """Test initialization"""
        mc = MonteCarloPropagator(n_ensemble=1000, seed=42)
        assert mc.n_ensemble == 1000
        assert mc.seed == 42
    
    def test_propagate(self):
        """Test uncertainty propagation"""
        mc = MonteCarloPropagator(n_ensemble=100)
        
        # Simple test function
        def test_func(params):
            return params['a'] + params['b']
        
        parameters = {
            'a': (10.0, 1.0),
            'b': (20.0, 2.0)
        }
        
        result = mc.propagate(parameters, test_func)
        
        assert 'mean' in result
        assert 'std' in result
        assert 'p5' in result
        assert 'p95' in result
        assert result['n_ensemble'] > 0
    
    def test_propagate_with_bounds(self):
        """Test propagation with bounds"""
        mc = MonteCarloPropagator(n_ensemble=100)
        
        def test_func(params):
            return params['a']
        
        parameters = {
            'a': (5.0, 10.0, 15.0)  # min, mean, max
        }
        
        result = mc.propagate_with_bounds(parameters, test_func)
        
        assert 5.0 <= result['min'] <= 15.0
        assert 5.0 <= result['max'] <= 15.0
    
    def test_ensemble_stats(self):
        """Test ensemble statistics calculation"""
        mc = MonteCarloPropagator()
        
        ensemble = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        stats = mc._ensemble_stats(ensemble)
        
        assert stats['mean'] == 5.5
        assert stats['median'] == 5.5
        assert stats['min'] == 1
        assert stats['max'] == 10
        assert stats['p5'] <= stats['p95']
    
    def test_threshold_year(self):
        """Test threshold year finding"""
        mc = MonteCarloPropagator()
        
        ensemble_by_year = {
            2025: [0.75, 0.76, 0.77],
            2030: [0.82, 0.83, 0.84],
            2035: [0.88, 0.89, 0.90],
            2040: [0.92, 0.93, 0.94]
        }
        
        result = mc.threshold_year(ensemble_by_year, threshold=0.85)
        
        assert result['threshold'] == 0.85
        assert result['median_year'] is not None
    
    def test_get_scenario_params(self):
        """Test scenario parameters"""
        mc = MonteCarloPropagator()
        
        ssp1 = mc._get_scenario_params('SSP1-1.9')
        assert 'E_anth' in ssp1
        assert 'F_perma' in ssp1
        
        ssp3 = mc._get_scenario_params('SSP3-7.0')
        assert ssp3['F_perma'] > ssp1['F_perma']
        
        ssp5 = mc._get_scenario_params('SSP5-8.5')
        assert ssp5['F_perma'] > ssp3['F_perma']
