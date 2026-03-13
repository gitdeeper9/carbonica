"""
Projection Plot Module
Visualize SSP scenario projections for PCSI
"""

from typing import Dict, List, Optional, Tuple


class ProjectionPlot:
    """
    SSP scenario projection plots for PCSI
    
    Visualizes PCSI projections under different emissions scenarios:
    - SSP1-1.9 (aggressive mitigation)
    - SSP3-7.0 (current trajectory)
    - SSP5-8.5 (high emissions)
    """
    
    def __init__(self, width: int = 70):
        """
        Initialize projection plot
        
        Parameters
        ----------
        width : int
            Plot width in characters
        """
        self.width = width
        
        # Projection data from paper
        self.projections = {
            'SSP1-1.9': [
                (2025, 0.78), (2030, 0.81), (2035, 0.83), (2040, 0.85),
                (2045, 0.87), (2050, 0.88), (2055, 0.89), (2060, 0.90),
                (2065, 0.91), (2070, 0.92)
            ],
            'SSP3-7.0': [
                (2025, 0.78), (2030, 0.82), (2035, 0.86), (2040, 0.89),
                (2045, 0.92), (2050, 0.94), (2055, 0.96), (2060, 0.97),
                (2065, 0.98), (2070, 0.99)
            ],
            'SSP5-8.5': [
                (2025, 0.78), (2030, 0.83), (2035, 0.88), (2040, 0.92),
                (2045, 0.95), (2050, 0.97), (2055, 0.98), (2060, 0.99),
                (2065, 1.00), (2070, 1.00)
            ]
        }
        
        # Thresholds
        self.thresholds = {
            'critical': 0.80,
            'saturation': 1.00
        }
    
    def set_projections(self, projections: Dict[str, List[Tuple[int, float]]]):
        """Set custom projection data"""
        self.projections = projections
    
    def _scale_value(self, value: float, min_val: float, max_val: float) -> int:
        """Scale value to plot width"""
        if max_val - min_val == 0:
            return self.width // 2
        return int((value - min_val) / (max_val - min_val) * (self.width - 1))
    
    def render_projection(self, years: List[int], values: List[float],
                         scenario: str, color: str = '█') -> str:
        """Render single projection line"""
        if not years or not values:
            return ""
        
        min_val = min(values + [0.5])
        max_val = max(values + [1.0])
        
        plot = f"  {scenario:10s} "
        
        # Create line
        line = [' '] * self.width
        for i, (year, val) in enumerate(zip(years, values)):
            pos = self._scale_value(val, min_val, max_val)
            if 0 <= pos < self.width:
                if i == 0:
                    line[pos] = '●'
                elif i == len(years) - 1:
                    line[pos] = '○'
                else:
                    line[pos] = '•'
        
        plot += ''.join(line)
        plot += f" {values[-1]:.2f}\n"
        
        return plot
    
    def render_all_projections(self) -> str:
        """Render all SSP projections"""
        # Find global min/max
        all_values = []
        for scenario, data in self.projections.items():
            all_values.extend([v for _, v in data])
        min_val = min(all_values + [0.5])
        max_val = max(all_values + [1.0])
        
        # Create scale
        scale = "  Year      "
        for i in range(0, self.width, 10):
            val = min_val + (max_val - min_val) * i / self.width
            scale += f"{val:.1f}" + " " * (10 - 4)
        
        plot = f"\n📈 PCSI Projections under SSP Scenarios\n"
        plot += "═" * (self.width + 20) + "\n\n"
        plot += scale + "\n"
        plot += "  " + "─" * self.width + "\n"
        
        # Plot each scenario
        colors = {'SSP1-1.9': '🟢', 'SSP3-7.0': '🟡', 'SSP5-8.5': '🔴'}
        
        for scenario, data in self.projections.items():
            years = [y for y, _ in data]
            values = [v for _, v in data]
            plot += self.render_projection(years, values, scenario, colors.get(scenario, '█'))
        
        plot += "  " + "─" * self.width + "\n"
        
        # Add threshold lines
        plot += "  Critical  "
        crit_pos = self._scale_value(self.thresholds['critical'], min_val, max_val)
        plot += ' ' * crit_pos + '│' + ' ' * (self.width - crit_pos - 1) + f" {self.thresholds['critical']:.2f}\n"
        
        plot += "  Saturation"
        sat_pos = self._scale_value(self.thresholds['saturation'], min_val, max_val)
        plot += ' ' * sat_pos + '║' + ' ' * (self.width - sat_pos - 1) + f" {self.thresholds['saturation']:.2f}\n"
        
        # Year labels
        plot += "\n  Years:    "
        all_years = sorted(set([y for data in self.projections.values() for y, _ in data]))
        for year in all_years[::2]:
            pos = self._scale_value(year, min(all_years), max(all_years))
            plot += ' ' * (pos - len(plot) + 20) + f"{year}"
        
        plot += "\n\n" + "═" * (self.width + 20) + "\n"
        
        return plot
    
    def get_threshold_crossing(self) -> Dict[str, int]:
        """Get year when each scenario crosses critical threshold"""
        crossings = {}
        
        for scenario, data in self.projections.items():
            for year, pcsi in data:
                if pcsi >= self.thresholds['critical']:
                    crossings[scenario] = year
                    break
            else:
                crossings[scenario] = None
        
        return crossings
    
    def get_uncertainty_range(self, scenario: str = "SSP3-7.0") -> List[Tuple[int, float, float]]:
        """Get uncertainty range for projection (simulated)"""
        data = self.projections.get(scenario, [])
        ranges = []
        
        for year, pcsi in data:
            # Simulate ±0.03 uncertainty
            ranges.append((year, pcsi - 0.03, pcsi + 0.03))
        
        return ranges
    
    def render_uncertainty_fan(self, scenario: str = "SSP3-7.0") -> str:
        """Render projection with uncertainty fan"""
        data = self.projections.get(scenario, [])
        if not data:
            return ""
        
        years = [y for y, _ in data]
        values = [v for _, v in data]
        ranges = self.get_uncertainty_range(scenario)
        
        min_val = min(values + [0.5])
        max_val = max(values + [1.0])
        
        plot = f"\n📊 {scenario} Projection with Uncertainty\n"
        plot += "─" * (self.width + 20) + "\n\n"
        
        for i, (year, pcsi) in enumerate(data):
            low, high = ranges[i][1], ranges[i][2]
            
            pos = self._scale_value(pcsi, min_val, max_val)
            low_pos = self._scale_value(low, min_val, max_val)
            high_pos = self._scale_value(high, min_val, max_val)
            
            line = [' '] * self.width
            for j in range(low_pos, high_pos + 1):
                if 0 <= j < self.width:
                    line[j] = '░'
            
            if 0 <= pos < self.width:
                line[pos] = '●'
            
            plot += f"  {year:4d}  {''.join(line)}  {pcsi:.2f} [{low:.2f}-{high:.2f}]\n"
        
        plot += "─" * (self.width + 20) + "\n"
        
        return plot
    
    def summary(self) -> str:
        """Print projection summary"""
        crossings = self.get_threshold_crossing()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║              PCSI Projection Summary                           ║
╠════════════════════════════════════════════════════════════════╣
║  Critical Threshold: {self.thresholds['critical']:.2f}                         ║
║  Saturation Threshold: {self.thresholds['saturation']:.2f}                      ║
╠════════════════════════════════════════════════════════════════╣
║  Year when PCSI ≥ {self.thresholds['critical']:.2f}:                              ║
║    SSP1-1.9 (mitigation) : {crossings.get('SSP1-1.9', 'N/A')}                          ║
║    SSP3-7.0 (current)    : {crossings.get('SSP3-7.0', 'N/A')}                          ║
║    SSP5-8.5 (high)       : {crossings.get('SSP5-8.5', 'N/A')}                          ║
╠════════════════════════════════════════════════════════════════╣
║  PCSI in 2050:                                               ║
║    SSP1-1.9 : {self.projections['SSP1-1.9'][5][1]:.2f}                               ║
║    SSP3-7.0 : {self.projections['SSP3-7.0'][5][1]:.2f}                               ║
║    SSP5-8.5 : {self.projections['SSP5-8.5'][5][1]:.2f}                               ║
╚════════════════════════════════════════════════════════════════╝
        """
        return summary
