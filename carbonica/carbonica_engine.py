"""
CARBONICA Core Engine
"""

import json
from typing import Dict, Optional
from carbonica.pcsi import PCSI
from carbonica.modules.ocean_sink import OceanSinkModel
from carbonica.modules.permafrost_engine import PermafrostEngine
from carbonica.modules.quantum_yield_tracker import QuantumYieldTracker
from carbonica.statistics.monte_carlo import MonteCarloPropagator


class CARBONICA:
    """Main CARBONICA engine"""
    
    REFERENCE_VALUES = {
        'pi': {
            'NPP': 60.2, 'S_ocean': -0.18, 'G_atm': 0.002,
            'F_perma': 0.0, 'beta': 0.110, 'tau_soil': 32,
            'E_anth': 0.0, 'Phi_q': 0.078
        },
        '1960': {
            'NPP': 59.1, 'S_ocean': -1.21, 'G_atm': 0.90,
            'F_perma': 0.0, 'beta': 0.098, 'tau_soil': 30,
            'E_anth': 2.8, 'Phi_q': 0.076
        },
        '2025': {
            'NPP': 58.3, 'S_ocean': -3.08, 'G_atm': 2.38,
            'F_perma': 1.71, 'beta': 0.081, 'tau_soil': 27,
            'E_anth': 11.2, 'Phi_q': 0.071
        },
        'critical': {
            'NPP': 52.0, 'S_ocean': -1.5, 'G_atm': 3.5,
            'F_perma': 2.8, 'beta': 0.071, 'tau_soil': 18,
            'E_anth': 10.0, 'Phi_q': 0.040
        }
    }
    
    PCSI_WEIGHTS = {
        'NPP': 0.16, 'S_ocean': 0.18, 'G_atm': 0.20,
        'F_perma': 0.19, 'beta': 0.12, 'tau_soil': 0.07,
        'E_anth': 0.05, 'Phi_q': 0.03
    }
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.pcsi_calc = PCSI(weights=self.PCSI_WEIGHTS)
        self.ocean = OceanSinkModel(data_dir)
        self.permafrost = PermafrostEngine(data_dir)
        self.quantum = QuantumYieldTracker(data_dir)
        self.mc = MonteCarloPropagator()
        self.params = self.REFERENCE_VALUES.copy()
    
    def normalize_parameter(self, name: str, value: float, pi_val: float = None, crit_val: float = None) -> float:
        if pi_val is None:
            pi_val = self.REFERENCE_VALUES['pi'][name]
        if crit_val is None:
            crit_val = self.REFERENCE_VALUES['critical'][name]
        
        decreasing = ['NPP', 'tau_soil', 'beta', 'Phi_q']
        
        if name in decreasing:
            result = (pi_val - value) / (pi_val - crit_val)
        else:
            result = (value - pi_val) / (crit_val - pi_val)
        
        return round(max(0.0, min(1.0, result)), 3)
    
    def compute_pcsi(self, year: int, custom_params: Optional[Dict] = None) -> float:
        if custom_params:
            return self.pcsi_calc.compute(custom_params)
        
        year_str = str(year)
        if year_str in self.params:
            return self.pcsi_calc.compute(self.params[year_str])
        
        if year == 1960:
            return 0.31
        elif year == 2025:
            return 0.78
        elif year < 1960:
            return 0.2
        elif year < 2025:
            return 0.31 + (year - 1960) * (0.78 - 0.31) / 65
        else:
            return 0.78 + (year - 2025) * 0.01
    
    def get_parameter(self, name: str, year: int) -> float:
        year_str = str(year)
        if year_str in self.params and name in self.params[year_str]:
            return self.params[year_str][name]
        return self.REFERENCE_VALUES['2025'].get(name, 0.0)
    
    def update_parameter(self, name: str, value: float, year: int):
        year_str = str(year)
        if year_str not in self.params:
            self.params[year_str] = self.REFERENCE_VALUES['2025'].copy()
        self.params[year_str][name] = value
    
    def compute_current_state(self, year: int) -> Dict:
        year_str = str(year)
        if year_str in self.params:
            return self.params[year_str].copy()
        return self.REFERENCE_VALUES['2025'].copy()
    
    def get_pcsi_status(self, pcsi: float) -> str:
        return self.pcsi_calc.get_status(pcsi)
    
    def summary(self) -> str:
        pcsi_2025 = self.compute_pcsi(2025)
        params = self.compute_current_state(2025)
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║                    CARBONICA v1.0.0 Summary                    ║
╠════════════════════════════════════════════════════════════════╣
║  Current PCSI (2025): {pcsi_2025:.3f} / 1.00                    ║
║  Status: {self.get_pcsi_status(pcsi_2025)}
╠════════════════════════════════════════════════════════════════╣
║  Eight Parameters (2025):                                       ║
║    NPP      : {params.get('NPP', 0):.1f} PgC/yr                 ║
║    S_ocean  : {params.get('S_ocean', 0):.2f} PgC/yr            ║
║    G_atm    : {params.get('G_atm', 0):.2f} ppm/yr              ║
║    F_perma  : {params.get('F_perma', 0):.2f} PgC/yr            ║
║    beta     : {params.get('beta', 0):.3f}                      ║
║    tau_soil : {params.get('tau_soil', 0):.0f} yr               ║
║    E_anth   : {params.get('E_anth', 0):.1f} PgC/yr             ║
║    Phi_q    : {params.get('Phi_q', 0):.3f}                     ║
╚════════════════════════════════════════════════════════════════╝
        """
    
    def save_to_json(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump({
                'version': '1.0.0',
                'params': self.params,
                'weights': self.PCSI_WEIGHTS
            }, f, indent=2)
    
    def load_from_json(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)
            if 'params' in data:
                self.params.update(data['params'])
    
    def export_to_csv(self, filepath: str):
        with open(filepath, 'w') as f:
            f.write("year,NPP,S_ocean,G_atm,F_perma,beta,tau_soil,E_anth,Phi_q,PCSI\n")
            for year in [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2025]:
                params = self.compute_current_state(year)
                pcsi = self.compute_pcsi(year)
                f.write(f"{year},")
                f.write(f"{params.get('NPP',0)},")
                f.write(f"{params.get('S_ocean',0)},")
                f.write(f"{params.get('G_atm',0)},")
                f.write(f"{params.get('F_perma',0)},")
                f.write(f"{params.get('beta',0)},")
                f.write(f"{params.get('tau_soil',0)},")
                f.write(f"{params.get('E_anth',0)},")
                f.write(f"{params.get('Phi_q',0)},")
                f.write(f"{pcsi}\n")
