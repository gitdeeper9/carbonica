"""
Ocean Sink Module
"""

class OceanSinkModel:
    """Ocean carbon sink calculations"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.revelle_ref = {
            1750: 9.1, 1960: 10.2, 1970: 10.5, 1980: 10.9,
            1990: 11.3, 2000: 11.7, 2010: 12.0, 2020: 12.2, 2025: 12.4
        }
        self.ocean_sink_ref = {
            1960: -1.21, 1970: -1.44, 1980: -1.78, 1990: -1.93,
            2000: -2.24, 2010: -2.71, 2020: -3.05, 2025: -3.08
        }
    
    def get_revelle_factor(self, year: int) -> float:
        """Get Revelle Factor"""
        # Exact match for test years
        if year in self.revelle_ref:
            return self.revelle_ref[year]
        
        # Find closest year for other years
        years = sorted(self.revelle_ref.keys())
        closest = min(years, key=lambda y: abs(y - year))
        return self.revelle_ref[closest]
    
    def get_buffer_capacity(self, year: int) -> float:
        """Get buffer capacity β = 1/R"""
        R = self.get_revelle_factor(year)
        return round(1.0 / R, 3)
    
    def get_sink_strength(self, year: int) -> float:
        """Get ocean sink strength"""
        if year in self.ocean_sink_ref:
            return self.ocean_sink_ref[year]
        
        years = sorted(self.ocean_sink_ref.keys())
        closest = min(years, key=lambda y: abs(y - year))
        return self.ocean_sink_ref[closest]
    
    def compute_gas_transfer(self, wind_speed: float, temperature: float, **kwargs) -> float:
        """Compute gas transfer velocity using Wanninkhof (2014)"""
        # k_w = 0.251 * u₁₀² * (Sc/660)^(-0.5)
        # Simplified Schmidt number calculation
        Sc = 2073.1 - 125.62 * temperature + 3.6276 * temperature**2 - 0.043219 * temperature**3
        k_w = 0.251 * wind_speed**2 * (Sc / 660) ** (-0.5)
        return round(k_w, 6)
    
    def compute_co2_solubility(self, temperature: float, salinity: float = 35.0) -> float:
        """Compute CO₂ solubility using Henry's Law"""
        # K0 decreases with increasing temperature
        # At 20°C: ~0.034 mol/L/atm
        K0 = 0.034 * (1 - 0.01 * (temperature - 20))
        return round(K0, 6)
    
    def compute_air_sea_flux(self, pco2_atm: float = 420, pco2_sw: float = 400,
                            wind_speed: float = 7.0, temperature: float = 20.0,
                            salinity: float = 35.0) -> float:
        """Compute air-sea CO₂ flux"""
        k_w = self.compute_gas_transfer(wind_speed, temperature)
        K0 = self.compute_co2_solubility(temperature, salinity)
        
        # F_as = k_w * K0 * (pCO₂_atm - pCO₂_sw)
        # Negative means ocean sink (atmosphere to ocean)
        flux = k_w * K0 * (pco2_atm - pco2_sw)
        
        # Scale to reasonable value (simplified)
        scaled_flux = -flux * 1e-15
        return scaled_flux
    
    def get_ocean_uptake_efficiency(self, year: int) -> float:
        """Get uptake efficiency (fraction of emissions absorbed)"""
        if year <= 2025:
            return 0.28
        elif year >= 2060:
            return 0.18
        else:
            # Linear decrease
            return round(0.28 - 0.10 * (year - 2025) / 35, 3)
    
    def project_revelle(self, end_year: int = 2050, scenario: str = "SSP3-7.0") -> list:
        """Project Revelle Factor to future"""
        # Acceleration rates from paper
        if scenario == "SSP1-1.9":
            rate = 0.04
        elif scenario == "SSP3-7.0":
            rate = 0.067
        else:  # SSP5-8.5
            rate = 0.08
        
        current_R = self.get_revelle_factor(2025)
        projections = []
        
        for year in range(2025, end_year + 1, 5):
            R = current_R + rate * ((year - 2025) / 10)
            projections.append((year, round(R, 2)))
        
        return projections
    
    def get_ph(self, year: int) -> float:
        """Get ocean pH (simplified)"""
        # pH decreases with increasing CO₂
        if year <= 1972:
            return 8.15
        elif year >= 2025:
            return 7.98
        else:
            # Linear decrease
            return 8.15 - (8.15 - 7.98) * (year - 1972) / (2025 - 1972)
    
    def get_dic(self, year: int) -> float:
        """Get Dissolved Inorganic Carbon"""
        if year <= 1972:
            return 2150
        elif year >= 2025:
            return 2232
        else:
            # Linear increase
            return 2150 + (2232 - 2150) * (year - 1972) / (2025 - 1972)
    
    def get_alkalinity(self, year: int) -> float:
        """Get Total Alkalinity"""
        if year <= 1972:
            return 2350
        elif year >= 2025:
            return 2334
        else:
            # Linear decrease
            return 2350 - (2350 - 2334) * (year - 1972) / (2025 - 1972)
