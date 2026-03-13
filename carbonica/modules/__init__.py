"""
CARBONICA Modules Package

Contains the four core processing modules:
- CarbonBudget: Master dC_atm/dt integrator
- OceanSinkModel: Air-sea CO₂ exchange & Revelle Factor
- PermafrostEngine: Permafrost thaw flux
- QuantumYieldTracker: Φ_q from satellite SIF
"""

from carbonica.modules.carbon_budget import CarbonBudget
from carbonica.modules.ocean_sink import OceanSinkModel
from carbonica.modules.permafrost_engine import PermafrostEngine
from carbonica.modules.quantum_yield_tracker import QuantumYieldTracker

__all__ = [
    "CarbonBudget",
    "OceanSinkModel", 
    "PermafrostEngine",
    "QuantumYieldTracker"
]
