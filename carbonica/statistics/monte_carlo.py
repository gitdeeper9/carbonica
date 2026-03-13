"""
Monte Carlo Uncertainty Propagation
10,000-member ensemble for PCSI uncertainty
"""

import random
import math
from typing import Dict, List, Optional, Tuple, Callable


class MonteCarloPropagator:
    """
    Monte Carlo uncertainty propagation for CARBONICA parameters
    """
    
    def __init__(self, n_ensemble: int = 10000, seed: int = 42):
        """
        Initialize Monte Carlo propagator
        
        Parameters
        ----------
        n_ensemble : int
            Number of ensemble members
        seed : int
            Random seed for reproducibility
        """
        self.n_ensemble = n_ensemble
        self.seed = seed
        random.seed(seed)
    
    def _normal_random(self, mean: float, std: float) -> float:
        """Generate normal random number (Box-Muller transform)"""
        # Box-Muller transform for normal distribution
        u1 = random.random()
        u2 = random.random()
        
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mean + std * z
    
    def _uniform_random(self, low: float, high: float) -> float:
        """Generate uniform random number"""
        return low + random.random() * (high - low)
    
    def propagate(self, parameters: Dict[str, Tuple[float, float]],
                 pcsi_func: Callable) -> Dict:
        """
        Propagate uncertainties through PCSI
        
        Parameters
        ----------
        parameters : dict
            Dictionary with parameter names as keys and
            (mean, std) tuples as values
        pcsi_func : callable
            Function that computes PCSI from parameters
        
        Returns
        -------
        dict
            Ensemble statistics
        """
        ensemble = []
        
        for _ in range(self.n_ensemble):
            # Sample each parameter
            sample = {}
            for name, (mean, std) in parameters.items():
                sample[name] = self._normal_random(mean, std)
            
            # Compute PCSI for this sample
            try:
                pcsi = pcsi_func(sample)
                ensemble.append(pcsi)
            except:
                pass
        
        return self._ensemble_stats(ensemble)
    
    def propagate_with_bounds(self, parameters: Dict[str, Tuple[float, float, float]],
                             pcsi_func: Callable) -> Dict:
        """
        Propagate with (min, mean, max) bounds
        
        Parameters
        ----------
        parameters : dict
            (min, mean, max) for each parameter
        pcsi_func : callable
            PCSI function
        """
        ensemble = []
        
        for _ in range(self.n_ensemble):
            sample = {}
            for name, (min_val, mean_val, max_val) in parameters.items():
                # Uniform between min and max
                sample[name] = self._uniform_random(min_val, max_val)
            
            try:
                pcsi = pcsi_func(sample)
                ensemble.append(pcsi)
            except:
                pass
        
        return self._ensemble_stats(ensemble)
    
    def _ensemble_stats(self, ensemble: List[float]) -> Dict:
        """Calculate ensemble statistics"""
        if not ensemble:
            return {
                'mean': 0,
                'median': 0,
                'std': 0,
                'p5': 0,
                'p95': 0,
                'min': 0,
                'max': 0,
                'n_ensemble': 0
            }
        
        sorted_ens = sorted(ensemble)
        n = len(sorted_ens)
        
        # Basic statistics
        mean_val = sum(ensemble) / n
        
        # Median
        if n % 2 == 0:
            median_val = (sorted_ens[n//2 - 1] + sorted_ens[n//2]) / 2
        else:
            median_val = sorted_ens[n//2]
        
        # Standard deviation
        variance = sum((x - mean_val) ** 2 for x in ensemble) / (n - 1) if n > 1 else 0
        std_val = math.sqrt(variance)
        
        # Percentiles
        p5_idx = max(0, min(n-1, int(n * 0.05)))
        p95_idx = max(0, min(n-1, int(n * 0.95)))
        
        return {
            'mean': mean_val,
            'median': median_val,
            'std': std_val,
            'p5': sorted_ens[p5_idx],
            'p95': sorted_ens[p95_idx],
            'min': sorted_ens[0],
            'max': sorted_ens[-1],
            'n_ensemble': n
        }
    
    def project_scenario(self, current: Dict[str, float],
                        uncertainties: Dict[str, float],
                        scenario: str, end_year: int = 2070) -> Dict:
        """
        Project PCSI under scenario
        
        Parameters
        ----------
        current : dict
            Current parameter values (2025)
        uncertainties : dict
            Parameter uncertainties
        scenario : str
            Scenario name
        end_year : int
            Projection end year
        
        Returns
        -------
        dict
            Projection ensemble by year
        """
        years = list(range(2025, end_year + 1, 5))
        
        # Scenario parameters
        scenario_params = self._get_scenario_params(scenario)
        
        # Project for each year
        projection = {}
        
        for year in years:
            year_ensemble = []
            years_from_now = year - 2025
            
            for _ in range(self.n_ensemble // len(years)):
                # Sample current uncertainties
                sample = {}
                for param, mean in current.items():
                    if param in uncertainties:
                        sample[param] = self._normal_random(mean, uncertainties[param])
                    else:
                        sample[param] = mean
                
                # Apply scenario trends
                for param, trend in scenario_params.items():
                    if param in sample:
                        sample[param] += trend * years_from_now
                
                year_ensemble.append(sample)
            
            projection[year] = year_ensemble
        
        return projection
    
    def _get_scenario_params(self, scenario: str) -> Dict[str, float]:
        """Get scenario parameters"""
        scenarios = {
            'SSP1-1.9': {
                'E_anth': -0.3,  # Decreasing emissions
                'F_perma': 0.05,
                'G_atm': -0.02
            },
            'SSP3-7.0': {
                'E_anth': 0.1,   # Increasing emissions
                'F_perma': 0.12,
                'G_atm': 0.05
            },
            'SSP5-8.5': {
                'E_anth': 0.2,
                'F_perma': 0.15,
                'G_atm': 0.08
            }
        }
        
        return scenarios.get(scenario, scenarios['SSP3-7.0'])
    
    def threshold_year(self, ensemble_by_year: Dict[int, List[float]],
                      threshold: float = 0.90) -> Dict:
        """
        Find year when threshold is crossed
        
        Parameters
        ----------
        ensemble_by_year : dict
            Ensemble values by year
        threshold : float
            PCSI threshold
        
        Returns
        -------
        dict
            Threshold crossing statistics
        """
        crossing_years = []
        
        for year, ensemble in ensemble_by_year.items():
            # Count members above threshold
            n_above = sum(1 for v in ensemble if v >= threshold)
            fraction = n_above / len(ensemble)
            
            crossing_years.append({
                'year': year,
                'fraction_above': fraction,
                'n_above': n_above
            })
        
        # Find median crossing year
        for cy in crossing_years:
            if cy['fraction_above'] >= 0.5:
                median_year = cy['year']
                break
        else:
            median_year = None
        
        return {
            'by_year': crossing_years,
            'median_year': median_year,
            'threshold': threshold
        }
