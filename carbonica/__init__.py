"""
CARBONICA - Advanced Planetary Carbon Accounting & Feedback Dynamics
Version: 1.0.0
DOI: 10.5281/zenodo.18995446

A physically rigorous eight-parameter framework for real-time quantification
of global carbon cycle dynamics, natural sink capacity, and the critical
threshold at which Earth's self-regulating biogeochemical systems approach
saturation.
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__doi__ = "10.5281/zenodo.18995446"

from carbonica.carbonica_engine import CARBONICA
from carbonica.pcsi import PCSI

__all__ = ["CARBONICA", "PCSI"]
