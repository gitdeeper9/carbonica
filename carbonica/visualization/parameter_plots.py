"""
Parameter Plots Module
Time series visualization for all eight parameters
"""

import math
from typing import Dict, List, Optional, Tuple


class ParameterPlots:
    """
    Generate time series plots for CARBONICA parameters
    
    Note: This is a text-based representation for terminal/console.
    For actual plots, use matplotlib/plotly in notebooks.
    """
    
    def __init__(self, width: int = 60):
        """
        Initialize parameter plots
        
        Parameters
        ----------
        width : int
            Plot width in characters
        """
        self.width = width
    
    def _scale_value(self, value: float, min_val: float, max_val: float) -> int:
        """Scale value to plot width"""
        if max_val - min_val == 0:
            return self.width // 2
        return int((value - min_val) / (max_val - min_val) * (self.width - 1))
    
    def _create_bar(self, value: float, min_val: float, max_val: float,
                   char: str = '█', label: str = '') -> str:
        """Create a text bar chart"""
        pos = self._scale_value(value, min_val, max_val)
        bar = char * pos + ' ' * (self.width - pos)
        return f"{label:10s} |{bar}| {value:.2f}"
    
    def plot_timeseries(self, years: List[int], values: List[float],
                       title: str, ylabel: str) -> str:
        """Create text-based time series plot"""
        if not years or not values:
            return "No data"
        
        min_val = min(values)
        max_val = max(values)
        
        plot = f"\n{title}\n"
        plot += "─" * self.width + "\n"
        
        # Find max and min for y-axis labels
        y_max = max_val
        y_min = min_val
        
        # Plot each point
        for i, (year, val) in enumerate(zip(years, values)):
            pos = self._scale_value(val, y_min, y_max)
            
            # Year label every 5 points
            if i % 5 == 0 or i == len(years) - 1:
                plot += f"{year:4d} |{'·' * pos}{'●'}{' ' * (self.width - pos - 1)}| {val:.2f}\n"
            else:
                plot += f"     |{'·' * pos}{'●'}{' ' * (self.width - pos - 1)}| {val:.2f}\n"
        
        plot += "─" * self.width + "\n"
        plot += f"     0{'' :>{self.width-5}} {max_val:.1f}\n"
        plot += f"     {ylabel}\n"
        
        return plot
    
    def plot_parameter_bars(self, parameters: Dict[str, float],
                           title: str = "Current Parameter Values") -> str:
        """Create bar chart of all eight parameters"""
        plot = f"\n{title}\n"
        plot += "═" * (self.width + 20) + "\n"
        
        # Define ranges for each parameter
        ranges = {
            'NPP': (50, 62),
            'S_ocean': (-3.5, 0),
            'G_atm': (0, 4),
            'F_perma': (0, 3),
            'beta': (0.07, 0.12),
            'tau_soil': (15, 35),
            'E_anth': (0, 15),
            'Phi_q': (0.04, 0.08)
        }
        
        for param, value in parameters.items():
            if param in ranges:
                min_val, max_val = ranges[param]
                plot += self._create_bar(value, min_val, max_val, '█', param) + "\n"
        
        plot += "═" * (self.width + 20) + "\n"
        
        return plot
    
    def plot_pcsi_gauge(self, pcsi: float) -> str:
        """Create a gauge chart for PCSI"""
        gauge_width = 50
        
        # Determine color zones
        stable = int(0.55 * gauge_width)
        transitional = int(0.25 * gauge_width)
        critical = gauge_width - stable - transitional
        
        gauge = "PCSI: ["
        
        # Stable zone (green)
        gauge += "🟢" * stable
        
        # Transitional zone (yellow)
        gauge += "🟡" * transitional
        
        # Critical zone (red)
        gauge += "🔴" * critical
        
        gauge += "]\n"
        gauge += "       " + " " * stable + "↑" + " " * (transitional - 1) + "\n"
        gauge += f"       {pcsi:.2f} ("
        
        if pcsi < 0.55:
            gauge += "STABLE)"
        elif pcsi < 0.80:
            gauge += "TRANSITIONAL)"
        else:
            gauge += "CRITICAL)"
        
        gauge += f"\n       0{'.' :>{int(pcsi*50)}}1"
        
        return gauge
    
    def plot_comparison(self, year1: int, params1: Dict[str, float],
                       year2: int, params2: Dict[str, float]) -> str:
        """Compare parameters between two years"""
        plot = f"\nParameter Comparison: {year1} vs {year2}\n"
        plot += "─" * 60 + "\n"
        plot += f"{'Parameter':12s} {year1:10s} {year2:10s} {'Change':10s} {'Status':10s}\n"
        plot += "─" * 60 + "\n"
        
        for param in ['NPP', 'S_ocean', 'G_atm', 'F_perma', 
                     'beta', 'tau_soil', 'E_anth', 'Phi_q']:
            v1 = params1.get(param, 0)
            v2 = params2.get(param, 0)
            change = v2 - v1
            pct_change = (change / v1 * 100) if v1 != 0 else 0
            
            # Determine status
            if param in ['NPP', 'tau_soil', 'beta', 'Phi_q']:
                # Decreasing is bad
                status = "🔴" if change < 0 else "🟢"
            else:
                # Increasing is bad
                status = "🔴" if change > 0 else "🟢"
            
            plot += f"{param:12s} {v1:10.2f} {v2:10.2f} {change:+8.2f} ({pct_change:+5.1f}%) {status:10s}\n"
        
        plot += "─" * 60 + "\n"
        
        return plot
    
    def plot_correlation_heatmap(self, corr_matrix: Dict[Tuple[str, str], float],
                                parameters: List[str]) -> str:
        """Create text-based correlation heatmap"""
        plot = "\nParameter Correlation Matrix\n"
        plot += "─" * (len(parameters) * 8 + 12) + "\n"
        
        # Header
        plot += " " * 12
        for p in parameters:
            plot += f"{p:8s}"
        plot += "\n"
        
        # Rows
        for p1 in parameters:
            plot += f"{p1:12s}"
            for p2 in parameters:
                corr = corr_matrix.get((p1, p2), 0)
                
                # Color coding
                if corr > 0.7:
                    color = "🔴"  # Strong positive
                elif corr > 0.3:
                    color = "🟡"  # Moderate positive
                elif corr < -0.7:
                    color = "🔵"  # Strong negative
                elif corr < -0.3:
                    color = "🟢"  # Moderate negative
                else:
                    color = "⚪"  # Weak
                
                plot += f" {color}{corr:6.2f} "
            plot += "\n"
        
        plot += "─" * (len(parameters) * 8 + 12) + "\n"
        plot += "🔴 Strong +  🟡 Moderate +  ⚪ Weak  🟢 Moderate -  🔵 Strong -\n"
        
        return plot
    
    def plot_ssp_projections(self, projections: Dict[str, List[Tuple[int, float]]],
                            title: str = "SSP Scenario Projections") -> str:
        """Plot SSP scenario projections"""
        plot = f"\n{title}\n"
        plot += "─" * self.width + "\n"
        
        # Collect all years
        all_years = set()
        for scenario, data in projections.items():
            for year, _ in data:
                all_years.add(year)
        years = sorted(all_years)
        
        if not years:
            return plot
        
        # Find min/max for scaling
        all_values = []
        for scenario, data in projections.items():
            all_values.extend([v for _, v in data])
        min_val = min(all_values)
        max_val = max(all_values)
        
        # Plot each scenario
        colors = {'SSP1-1.9': '🟢', 'SSP3-7.0': '🟡', 'SSP5-8.5': '🔴'}
        
        for scenario, data in projections.items():
            plot += f"\n{colors.get(scenario, '⚪')} {scenario}:\n"
            
            # Create dict for easy lookup
            val_dict = dict(data)
            
            # Plot line
            line = "     "
            for year in years:
                if year in val_dict:
                    pos = self._scale_value(val_dict[year], min_val, max_val)
                    line += "●" + "·" * max(0, pos - len(line) + 5)
            
            plot += line + "\n"
            
            # Print values
            for year in years:
                if year in val_dict:
                    plot += f"     {year}: {val_dict[year]:.2f}\n"
        
        return plot
