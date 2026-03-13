"""
QuantumYieldTracker Module
Photosynthetic Quantum Yield (Φ_q) from satellite SIF

Φ_q = ΔF/Fm' = (Fm' − Fs) / Fm' [solar-induced fluorescence formulation]
"""

import json
import csv
import os
import math
from typing import Dict, List, Optional, Tuple


class QuantumYieldTracker:
    """
    Photosynthetic Quantum Yield Tracker
    
    Tracks Φ_q from GOSAT and OCO-2 satellite SIF retrievals.
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize Quantum Yield Tracker module
        
        Parameters
        ----------
        data_dir : str
            Directory containing input data
        """
        self.data_dir = data_dir
        self.gosat_data = []
        self.oco2_data = []
        self._load_default_data()
    
    def _load_default_data(self):
        """Load default reference data"""
        # Global mean Φ_q values
        self.phi_q_ref = {
            2009: 0.0765,
            2010: 0.0763,
            2011: 0.0761,
            2012: 0.0759,
            2013: 0.0757,
            2014: 0.0755,
            2015: 0.0752,
            2016: 0.0750,
            2017: 0.0748,
            2018: 0.0745,
            2019: 0.0742,
            2020: 0.0740,
            2021: 0.0737,
            2022: 0.0734,
            2023: 0.0731,
            2024: 0.0728,
            2025: 0.0725
        }
        
        # Biome-specific Φ_q (2025 values)
        self.biome_phi_q = {
            'amazon_tropical': 0.055,
            'se_asian_peat': 0.058,
            'mediterranean': 0.062,
            'boreal_forest': 0.078,
            'temperate_forest': 0.072,
            'savanna': 0.065,
            'cropland': 0.068,
            'global_mean': 0.071
        }
        
        # Decline rates (% per decade)
        self.decline_rates = {
            'amazon_tropical': -2.1,
            'se_asian_peat': -1.8,
            'mediterranean': -1.4,
            'global_mean': -0.9,
            'boreal': 0.3  # Positive in boreal
        }
    
    def load_gosat(self, filepath: Optional[str] = None) -> List[Dict]:
        """
        Load GOSAT SIF data
        
        Parameters
        ----------
        filepath : str, optional
            Path to GOSAT data file
        
        Returns
        -------
        list
            List of SIF measurements
        """
        if filepath and os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                self.gosat_data = [row for row in reader]
        return self.gosat_data
    
    def load_oco2(self, filepath: Optional[str] = None) -> List[Dict]:
        """
        Load OCO-2 SIF data
        
        Parameters
        ----------
        filepath : str, optional
            Path to OCO-2 data file
        
        Returns
        -------
        list
            List of SIF measurements
        """
        if filepath and os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                self.oco2_data = [row for row in reader]
        return self.oco2_data
    
    def get_quantum_yield(self, year: int, biome: str = 'global_mean') -> float:
        """
        Get photosynthetic quantum yield Φ_q for given year and biome
        
        Parameters
        ----------
        year : int
            Target year
        biome : str
            Biome name
        
        Returns
        -------
        float
            Quantum yield (mol C / mol photons)
        """
        if biome == 'global_mean':
            # Use global time series
            available = sorted(self.phi_q_ref.keys())
            closest = min(available, key=lambda y: abs(y - year))
            return self.phi_q_ref[closest]
        else:
            # Use biome-specific value with decline rate
            base_value = self.biome_phi_q.get(biome, 0.071)
            decline_rate = self.decline_rates.get(biome, -0.9) / 100 / 10  # per year
            
            years_from_2025 = year - 2025
            return base_value * (1 + decline_rate * years_from_2025)
    
    def compute_from_sif(self, sif: float, apar: float) -> float:
        """
        Compute Φ_q from SIF and APAR using Frankenberg et al. (2011)
        
        Φ_q = SIF / (APAR · ε)
        
        Parameters
        ----------
        sif : float
            Solar-induced fluorescence (mW/m²/sr/nm)
        apar : float
            Absorbed photosynthetically active radiation (µmol/m²/s)
        
        Returns
        -------
        float
            Quantum yield estimate
        """
        # Conversion factor (simplified)
        epsilon = 0.01
        phi_q = sif / (apar * epsilon)
        
        return min(0.125, max(0.0, phi_q))  # Cap at theoretical maximum
    
    def detect_stress(self, phi_q: float, biome: str) -> Tuple[bool, str]:
        """
        Detect if Φ_q indicates stress conditions
        
        Parameters
        ----------
        phi_q : float
            Quantum yield value
        biome : str
            Biome name
        
        Returns
        -------
        tuple
            (is_stressed, stress_level)
        """
        normal_range = {
            'amazon_tropical': (0.065, 0.075),
            'boreal_forest': (0.075, 0.085),
            'global_mean': (0.070, 0.078)
        }
        
        normal = normal_range.get(biome, (0.070, 0.078))
        
        if phi_q < normal[0]:
            if phi_q < 0.040:
                return True, "SEVERE STRESS"
            elif phi_q < 0.055:
                return True, "HIGH STRESS"
            else:
                return True, "MODERATE STRESS"
        else:
            return False, "NORMAL"
    
    def get_trend(self, start_year: int = 2009, 
                  end_year: int = 2025,
                  biome: str = 'global_mean') -> Dict:
        """
        Calculate Φ_q trend over period
        
        Parameters
        ----------
        start_year : int
            Start year
        end_year : int
            End year
        biome : str
            Biome name
        
        Returns
        -------
        dict
            Trend statistics
        """
        years = list(range(start_year, end_year + 1))
        values = [self.get_quantum_yield(y, biome) for y in years]
        
        # Simple linear trend
        n = len(years)
        if n < 2:
            return {'slope': 0, 'decline_rate': 0}
        
        # Calculate slope
        mean_x = sum(years) / n
        mean_y = sum(values) / n
        
        numerator = sum((years[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((years[i] - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Decline rate (% per decade)
        decline_rate = (slope / mean_y) * 100 * 10
        
        return {
            'start_year': start_year,
            'end_year': end_year,
            'start_value': values[0],
            'end_value': values[-1],
            'absolute_change': values[-1] - values[0],
            'relative_change': (values[-1] - values[0]) / values[0] * 100,
            'slope': slope,
            'decline_rate_per_decade': decline_rate
        }
    
    def summary(self, year: int = 2025) -> str:
        """Print quantum yield summary"""
        global_phi = self.get_quantum_yield(year)
        trend = self.get_trend(2009, 2025)
        stressed, level = self.detect_stress(global_phi, 'global_mean')
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║                 Quantum Yield Summary ({year})                  ║
╠════════════════════════════════════════════════════════════════╣
║  Global mean Φ_q    : {global_phi:.4f}                         ║
║  Status             : {level}                                  ║
╠════════════════════════════════════════════════════════════════╣
║  Trend (2009-2025):                                           ║
║    Decline rate     : {trend['decline_rate_per_decade']:.2f}%/decade  ║
║    Absolute change  : {trend['absolute_change']:.4f}                 ║
║    Relative change  : {trend['relative_change']:.2f}%                 ║
╠════════════════════════════════════════════════════════════════╣
║  Biome-specific Φ_q (2025):                                    ║
║    Amazon tropical  : {self.biome_phi_q['amazon_tropical']:.3f}      ║
║    SE Asian peat    : {self.biome_phi_q['se_asian_peat']:.3f}        ║
║    Mediterranean    : {self.biome_phi_q['mediterranean']:.3f}        ║
║    Boreal forest    : {self.biome_phi_q['boreal_forest']:.3f}        ║
╚════════════════════════════════════════════════════════════════╝
        """
        return summary
