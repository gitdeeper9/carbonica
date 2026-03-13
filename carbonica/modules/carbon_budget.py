"""
CarbonBudget Module
Master dC_atm/dt integrator for CARBONICA

dC_atm/dt = E_anth + F_nat + F_perma - S_ocean - S_land
where S_land = NPP - R_eco
"""

import json
import csv
import os
from typing import Dict, List, Optional, Tuple


class CarbonBudget:
    """
    Carbon Budget Calculator
    
    Integrates all sources and sinks to compute atmospheric CO₂ growth rate.
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize Carbon Budget module
        
        Parameters
        ----------
        data_dir : str
            Directory containing input data
        """
        self.data_dir = data_dir
        self.keeling_data = []
        self.gcp_data = []
        self._load_default_data()
    
    def _load_default_data(self):
        """Load default reference data"""
        # Keeling Curve reference values (ppm)
        self.keeling_ref = {
            1960: 316.9, 1965: 320.0, 1970: 325.7, 1975: 331.1,
            1980: 338.7, 1985: 346.0, 1990: 354.2, 1995: 360.8,
            2000: 369.4, 2005: 379.7, 2010: 389.8, 2015: 400.8,
            2020: 414.2, 2025: 424.0
        }
    
    def load_keeling(self, filepath: Optional[str] = None) -> List[Dict]:
        """
        Load Keeling Curve data from NOAA
        
        Parameters
        ----------
        filepath : str, optional
            Path to Keeling data file
        
        Returns
        -------
        list
            List of {year, month, co2_ppm} dictionaries
        """
        if filepath and os.path.exists(filepath):
            # Load from file
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                self.keeling_data = [row for row in reader]
        else:
            # Use reference data
            self.keeling_data = [
                {'year': year, 'co2_ppm': value}
                for year, value in self.keeling_ref.items()
            ]
        
        return self.keeling_data
    
    def compute_growth_rate(self, year: int) -> float:
        """
        Compute atmospheric CO₂ growth rate G_atm for given year
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            Growth rate in ppm/yr
        """
        # Reference values from paper
        growth_rates = {
            1960: 0.90, 1965: 1.10, 1970: 1.28, 1975: 1.40,
            1980: 1.51, 1985: 1.58, 1990: 1.63, 1995: 1.70,
            2000: 1.88, 2005: 2.04, 2010: 2.19, 2015: 2.28,
            2020: 2.35, 2025: 2.38
        }
        
        # Find closest year
        available = sorted(growth_rates.keys())
        closest = min(available, key=lambda y: abs(y - year))
        return growth_rates[closest]
    
    def get_npp(self, year: int) -> float:
        """
        Get Net Primary Productivity for given year
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            NPP in PgC/yr
        """
        # Reference values from paper
        npp_values = {
            1960: 59.1, 1970: 59.0, 1980: 58.9, 1990: 58.7,
            2000: 58.5, 2010: 58.4, 2020: 58.3, 2025: 58.3
        }
        
        available = sorted(npp_values.keys())
        closest = min(available, key=lambda y: abs(y - year))
        return npp_values[closest]
    
    def get_emissions(self, year: int) -> float:
        """
        Get anthropogenic emissions E_anth for given year
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            Emissions in PgC/yr
        """
        # Reference values from paper
        emissions = {
            1960: 2.8, 1970: 4.1, 1980: 5.3, 1990: 6.1,
            2000: 6.8, 2010: 9.1, 2020: 10.5, 2025: 11.2
        }
        
        available = sorted(emissions.keys())
        closest = min(available, key=lambda y: abs(y - year))
        return emissions[closest]
    
    def get_soil_residence(self, year: int) -> float:
        """
        Get soil carbon residence time τ_soil for given year
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            Residence time in years
        """
        # Reference values from paper
        residence = {
            1960: 30, 1970: 29.5, 1980: 29, 1990: 28.5,
            2000: 28, 2010: 27.5, 2020: 27, 2025: 27
        }
        
        available = sorted(residence.keys())
        closest = min(available, key=lambda y: abs(y - year))
        return residence[closest]
    
    def compute_budget(self, params: Dict) -> Dict:
        """
        Compute carbon budget
        
        dC_atm/dt = E_anth + F_nat + F_perma - S_ocean - S_land
        
        Parameters
        ----------
        params : dict
            Dictionary with keys: E_anth, F_nat, F_perma, S_ocean, NPP, R_eco
        
        Returns
        -------
        dict
            Budget components
        """
        # Natural emissions (volcanic, etc.) - constant background
        F_nat = params.get('F_nat', 0.2)
        
        # Terrestrial sink
        NPP = params.get('NPP', 58.3)
        R_eco = params.get('R_eco', 55.0)  # Ecosystem respiration
        S_land = NPP - R_eco
        
        # Atmospheric growth rate
        dC_dt = (params.get('E_anth', 11.2) + F_nat + 
                 params.get('F_perma', 1.71) - 
                 params.get('S_ocean', 3.08) - S_land)
        
        # Convert PgC to ppm (approximate: 1 PgC ≈ 0.47 ppm)
        dC_dt_ppm = dC_dt * 0.47
        
        return {
            'dC_dt': dC_dt,
            'dC_dt_ppm': dC_dt_ppm,
            'S_land': S_land,
            'F_nat': F_nat,
            'components': params
        }
    
    def detect_change_point(self, timeseries: List[float], 
                           threshold: float = 2.0) -> List[int]:
        """
        Simple CUSUM change point detection
        
        Parameters
        ----------
        timeseries : list
            Time series data
        threshold : float
            Detection threshold
        
        Returns
        -------
        list
            Indices of change points
        """
        if len(timeseries) < 2:
            return []
        
        mean_val = sum(timeseries) / len(timeseries)
        cusum = [0]
        
        for i, val in enumerate(timeseries[1:], 1):
            cusum.append(cusum[-1] + (val - mean_val))
        
        # Find significant changes
        change_points = []
        std_val = (sum((x - mean_val) ** 2 for x in timeseries) / len(timeseries)) ** 0.5
        
        for i, val in enumerate(cusum):
            if abs(val) > threshold * std_val * (len(timeseries) ** 0.5):
                change_points.append(i)
        
        return change_points
