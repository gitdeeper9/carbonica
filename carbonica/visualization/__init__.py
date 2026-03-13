"""
CARBONICA Visualization Package

Plotting and dashboard components for carbon cycle analysis
"""

from carbonica.visualization.pcsi_dashboard import PCSIDashboard
from carbonica.visualization.parameter_plots import ParameterPlots
from carbonica.visualization.correlation_matrix import CorrelationMatrix
from carbonica.visualization.projection_plot import ProjectionPlot

__all__ = [
    "PCSIDashboard",
    "ParameterPlots",
    "CorrelationMatrix",
    "ProjectionPlot"
]
