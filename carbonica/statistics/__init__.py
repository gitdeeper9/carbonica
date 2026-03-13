"""
CARBONICA Statistics Package

Statistical methods for carbon cycle analysis:
- Monte Carlo uncertainty propagation
- Structural Equation Modeling (SEM)
- PCA-regularized regression
- CUSUM change point detection
"""

from carbonica.statistics.monte_carlo import MonteCarloPropagator
from carbonica.statistics.sem import StructuralEquationModel
from carbonica.statistics.pca_regression import PCARegression
from carbonica.statistics.cusum import CUSUMDetector
from carbonica.statistics.simple_stats import SimpleStats

__all__ = [
    "MonteCarloPropagator",
    "StructuralEquationModel",
    "PCARegression", 
    "CUSUMDetector",
    "SimpleStats"
]
