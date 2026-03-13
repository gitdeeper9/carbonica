"""
PermafrostEngine Module
Permafrost thaw flux calculations

F_perma = C_perma · k_decomp(T) · A_thaw(t) / τ_frozen
k_decomp(T) = k₀ · Q₁₀^((T−T_ref)/10)
"""

import json
import csv
import os
import math
from typing import Dict, List, Optional, Tuple


class PermafrostEngine:
    """
    Permafrost Thaw Flux Calculator
    
    Computes permafrost carbon release including abrupt thaw mechanisms.
    """
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize Permafrost Engine module
        
        Parameters
        ----------
        data_dir : str
            Directory containing input data
        """
        self.data_dir = data_dir
        self.gtnp_data = []
        self._load_default_data()
    
    def _load_default_data(self):
        """Load default reference data"""
        # Permafrost flux reference values (PgC/yr)
        self.permaflux_ref = {
            1960: 0.0,
            1970: 0.0,
            1980: 0.01,
            1990: 0.05,
            2000: 0.31,
            2010: 0.98,
            2020: 1.65,
            2025: 1.71
        }
        
        # Q10 values by soil type
        self.q10_values = {
            'mineral': 2.1,
            'organic': 2.8,
            'yedoma': 3.5
        }
        
        # Carbon density (kgC/m²)
        self.carbon_density = {
            'continuous': 28.1,
            'discontinuous': 18.5,
            'sporadic': 10.2
        }
    
    def load_gtnp(self, filepath: Optional[str] = None) -> List[Dict]:
        """
        Load GTN-P (Global Terrestrial Network for Permafrost) data
        
        Parameters
        ----------
        filepath : str, optional
            Path to GTN-P data file
        
        Returns
        -------
        list
            List of borehole measurements
        """
        if filepath and os.path.exists(filepath):
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                self.gtnp_data = [row for row in reader]
        return self.gtnp_data
    
    def get_flux(self, year: int) -> float:
        """
        Get permafrost thaw flux F_perma for given year
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            Permafrost flux in PgC/yr
        """
        available = sorted(self.permaflux_ref.keys())
        closest = min(available, key=lambda y: abs(y - year))
        return self.permaflux_ref[closest]
    
    def compute_decomposition_rate(self, temperature_anomaly: float,
                                  q10: float = 2.5) -> float:
        """
        Compute temperature-dependent decomposition rate
        
        k_decomp(T) = Q₁₀^((T−T_ref)/10)
        
        Parameters
        ----------
        temperature_anomaly : float
            Temperature anomaly above baseline (°C)
        q10 : float
            Q₁₀ temperature sensitivity coefficient
        
        Returns
        -------
        float
            Decomposition rate multiplier
        """
        return q10 ** (temperature_anomaly / 10.0)
    
    def compute_flux(self, carbon_density: float, area: float,
                    temperature_anomaly: float, q10: float = 2.5,
                    tau_frozen: float = 10000) -> float:
        """
        Compute permafrost thaw flux
        
        F_perma = C_perma · k_decomp(T) · A / τ_frozen
        
        Parameters
        ----------
        carbon_density : float
            Carbon density (kgC/m²)
        area : float
            Thawing area (m²)
        temperature_anomaly : float
            Temperature anomaly (°C)
        q10 : float
            Q₁₀ sensitivity coefficient
        tau_frozen : float
            Mean age of frozen carbon (years)
        
        Returns
        -------
        float
            Permafrost flux in PgC (1 Pg = 10¹⁵ g)
        """
        k_decomp = self.compute_decomposition_rate(temperature_anomaly, q10)
        
        # Convert kg to Pg: 1 kg = 10⁻¹² Pg
        flux_pg = (carbon_density * k_decomp * area) / (tau_frozen * 1e12)
        
        return flux_pg
    
    def get_abrupt_thaw_fraction(self, year: int) -> float:
        """
        Get fraction of flux from abrupt thaw (thermokarst)
        
        Parameters
        ----------
        year : int
            Target year
        
        Returns
        -------
        float
            Fraction (0-1)
        """
        # From paper: 31% in 2025, increasing
        if year <= 2025:
            return 0.31
        else:
            # Projected increase
            return min(0.45, 0.31 + 0.01 * (year - 2025))
    
    def separate_thaw_types(self, total_flux: float, year: int) -> Dict:
        """
        Separate total flux into gradual and abrupt components
        
        Parameters
        ----------
        total_flux : float
            Total permafrost flux (PgC/yr)
        year : int
            Target year
        
        Returns
        -------
        dict
            Dictionary with 'gradual' and 'abrupt' components
        """
        abrupt_fraction = self.get_abrupt_thaw_fraction(year)
        abrupt = total_flux * abrupt_fraction
        gradual = total_flux * (1 - abrupt_fraction)
        
        return {
            'total': total_flux,
            'gradual': gradual,
            'abrupt': abrupt,
            'abrupt_fraction': abrupt_fraction
        }
    
    def project_flux(self, end_year: int = 2100,
                    scenario: str = "SSP3-7.0") -> List[Tuple[int, float]]:
        """
        Project permafrost flux to future
        
        Parameters
        ----------
        end_year : int
            Projection end year
        scenario : str
            Emissions scenario
        
        Returns
        -------
        list
            List of (year, flux) tuples
        """
        projections = []
        current_flux = self.get_flux(2025)
        
        # Acceleration rates from paper
        if scenario == "SSP1-1.9":
            rate = 0.08  # Slower increase
        elif scenario == "SSP3-7.0":
            rate = 0.12  # Current acceleration (PgC/yr²)
        else:  # SSP5-8.5
            rate = 0.15  # Faster increase
        
        for year in range(2025, end_year + 1, 5):
            years_from_now = year - 2025
            flux = current_flux + rate * years_from_now
            
            # Apply self-sustaining threshold
            if flux > 2.8:
                # After crossing threshold, acceleration increases
                flux = 2.8 + (flux - 2.8) * 1.5
            
            projections.append((year, round(flux, 2)))
        
        return projections
    
    def get_critical_year(self, scenario: str = "SSP3-7.0") -> int:
        """
        Get year when permafrost reaches self-sustaining threshold (2.8 PgC/yr)
        
        Parameters
        ----------
        scenario : str
            Emissions scenario
        
        Returns
        -------
        int
            Critical year
        """
        if scenario == "SSP1-1.9":
            return 2065
        elif scenario == "SSP3-7.0":
            return 2042  # From paper: 2038-2046
        else:  # SSP5-8.5
            return 2035
    
    def get_esas_risk_year(self) -> Tuple[int, int]:
        """
        Get East Siberian Arctic Shelf (ESAS) risk window
        
        Returns
        -------
        tuple
            (start_year, end_year) for ESAS activation
        """
        # From paper: 2031-2044
        return (2031, 2044)
    
    def summary(self, year: int = 2025) -> str:
        """Print permafrost summary for given year"""
        flux = self.get_flux(year)
        components = self.separate_thaw_types(flux, year)
        critical_year = self.get_critical_year()
        esas_range = self.get_esas_risk_year()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║                    Permafrost Summary ({year})                   ║
╠════════════════════════════════════════════════════════════════╣
║  Total flux      : {flux:.2f} ± 0.40 PgC/yr                     ║
║  Gradual thaw    : {components['gradual']:.2f} PgC/yr          ║
║  Abrupt thaw     : {components['abrupt']:.2f} PgC/yr           ║
║  Abrupt fraction : {components['abrupt_fraction']*100:.1f}%      ║
║  % of global     : {(flux/11.2*100):.1f}% (of 11.2 PgC)        ║
╠════════════════════════════════════════════════════════════════╣
║  Self-sustaining threshold : 2.8 PgC/yr                        ║
║  Critical year (SSP3-7.0)   : {critical_year}                    ║
║  ESAS submarine risk window : {esas_range[0]}-{esas_range[1]}        ║
╚════════════════════════════════════════════════════════════════╝
        """
        return summary
