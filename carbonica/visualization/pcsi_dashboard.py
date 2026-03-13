"""
PCSI Dashboard Module
Real-time monitoring dashboard for Planetary Carbon Saturation Index
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from carbonica.visualization.parameter_plots import ParameterPlots


class PCSIDashboard:
    """
    Real-time PCSI monitoring dashboard
    
    Provides text-based dashboard for terminal/console monitoring.
    For web-based dashboard, see the separate `dashboard/` directory.
    """
    
    def __init__(self, carbonica_instance=None, width: int = 80):
        """
        Initialize PCSI dashboard
        
        Parameters
        ----------
        carbonica_instance : CARBONICA, optional
            CARBONICA engine instance
        width : int
            Dashboard width in characters
        """
        self.carbonica = carbonica_instance
        self.width = width
        self.plots = ParameterPlots(width=width - 20)
        self.history = []
        self.update_interval = 60  # seconds
        self.last_update = None
    
    def set_carbonica(self, carbonica_instance):
        """Set CARBONICA instance"""
        self.carbonica = carbonica_instance
    
    def update(self) -> Dict:
        """Update dashboard data"""
        if not self.carbonica:
            return {'error': 'No CARBONICA instance'}
        
        # Get current PCSI
        pcsi_2025 = self.carbonica.compute_pcsi(2025)
        
        # Get current parameters
        params = self.carbonica.params.get('2025', self.carbonica.REFERENCE_VALUES['2025'])
        
        # Store in history
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'pcsi': pcsi_2025,
            'parameters': params.copy()
        })
        
        # Keep last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.last_update = datetime.now()
        
        return {
            'pcsi': pcsi_2025,
            'parameters': params,
            'status': self.carbonica.get_pcsi_status(pcsi_2025),
            'timestamp': self.last_update
        }
    
    def render_header(self) -> str:
        """Render dashboard header"""
        header = f"""
╔{'═' * (self.width-2)}╗
║{' ' * ((self.width - 40) // 2)}🌍 CARBONICA Planetary Carbon Dashboard{' ' * ((self.width - 41) // 2)}║
╠{'═' * (self.width-2)}╣
║  Version: 1.0.0 | DOI: 10.5281/zenodo.18995446{' ' * (self.width - 57)}║
║  Last Update: {self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else 'Never'}{' ' * (self.width - 54)}║
╚{'═' * (self.width-2)}╝
"""
        return header
    
    def render_pcsi_gauge(self, pcsi: float) -> str:
        """Render PCSI gauge"""
        gauge_width = self.width - 10
        
        # Determine thresholds
        stable = int(0.55 * gauge_width)
        transitional = int(0.25 * gauge_width)
        critical = gauge_width - stable - transitional
        
        gauge = f"║  PCSI: ["
        
        # Stable zone (green)
        gauge += "🟢" * stable
        
        # Transitional zone (yellow)
        gauge += "🟡" * transitional
        
        # Critical zone (red)
        gauge += "🔴" * critical
        
        gauge += f"]  ║\n"
        
        # Pointer
        pos = int(pcsi * gauge_width)
        gauge += f"║{' ' * 8}{' ' * pos}▲{' ' * (gauge_width - pos - 1)}  ║\n"
        
        # Value and status
        status = self.carbonica.get_pcsi_status(pcsi) if self.carbonica else "Unknown"
        gauge += f"║  Value: {pcsi:.3f} / 1.00{' ' * (gauge_width - 25)}  ║\n"
        gauge += f"║  Status: {status}{' ' * (gauge_width - len(status) - 14)}  ║\n"
        
        return gauge
    
    def render_parameters(self, params: Dict[str, float]) -> str:
        """Render eight parameters"""
        output = f"╠{'═' * (self.width-2)}╣\n"
        output += f"║  {'Eight Parameters (2025)':^{self.width-6}}  ║\n"
        output += f"╠{'═' * (self.width-2)}╣\n"
        
        # Define parameter info
        param_info = [
            ('NPP', 'PgC/yr', 50, 62, 'Terrestrial uptake'),
            ('S_ocean', 'PgC/yr', -3.5, 0, 'Ocean sink'),
            ('G_atm', 'ppm/yr', 0, 4, 'CO₂ growth'),
            ('F_perma', 'PgC/yr', 0, 3, 'Permafrost thaw'),
            ('beta', '', 0.07, 0.12, 'Buffer capacity'),
            ('tau_soil', 'yr', 15, 35, 'Soil residence'),
            ('E_anth', 'PgC/yr', 0, 15, 'Anthropogenic'),
            ('Phi_q', '', 0.04, 0.08, 'Quantum yield')
        ]
        
        for param, unit, min_val, max_val, desc in param_info:
            value = params.get(param, 0)
            
            # Normalize to bar length
            bar_width = self.width - 40
            if max_val - min_val != 0:
                if param in ['NPP', 'tau_soil', 'beta', 'Phi_q']:
                    # Decreasing parameters (lower is worse)
                    pos = int((max_val - value) / (max_val - min_val) * bar_width)
                else:
                    # Increasing parameters (higher is worse)
                    pos = int((value - min_val) / (max_val - min_val) * bar_width)
            else:
                pos = 0
            
            pos = max(0, min(bar_width, pos))
            
            bar = '█' * pos + '░' * (bar_width - pos)
            output += f"║  {param:8s} {value:6.2f} {unit:6s} [{bar}] {desc:20s} ║\n"
        
        return output
    
    def render_history(self) -> str:
        """Render PCSI history"""
        if len(self.history) < 2:
            return ""
        
        output = f"╠{'═' * (self.width-2)}╣\n"
        output += f"║  {'PCSI History (last 10)':^{self.width-6}}  ║\n"
        output += f"╠{'═' * (self.width-2)}╣\n"
        
        # Plot sparkline
        recent = [h['pcsi'] for h in self.history[-20:]]
        if recent:
            spark_width = self.width - 20
            min_pcsi = min(recent)
            max_pcsi = max(recent)
            
            spark = ""
            for val in recent:
                if max_pcsi - min_pcsi == 0:
                    pos = spark_width // 2
                else:
                    pos = int((val - min_pcsi) / (max_pcsi - min_pcsi) * (spark_width - 1))
                
                if val > 0.8:
                    spark += "🔴"
                elif val > 0.55:
                    spark += "🟡"
                else:
                    spark += "🟢"
            
            output += f"║  Trend: {spark:<{spark_width}}  ║\n"
        
        # Last 10 values
        output += f"║  {'─' * (self.width-6)}  ║\n"
        line = "║  "
        for i, h in enumerate(self.history[-10:]):
            if i > 0 and i % 5 == 0:
                line += f"\n║  "
            time_str = h['timestamp'][5:16] if 'timestamp' in h else 'unknown'
            line += f"{h['pcsi']:.2f} ({time_str})  "
        
        output += line + f"{' ' * (self.width - len(line) - 6)}║\n"
        
        return output
    
    def render_alerts(self) -> str:
        """Render alerts if any"""
        if not self.history:
            return ""
        
        latest = self.history[-1]
        pcsi = latest['pcsi']
        
        alerts = []
        
        # Check PCSI threshold
        if pcsi > 0.8:
            alerts.append(("🔴 CRITICAL", f"PCSI = {pcsi:.3f} exceeds critical threshold 0.80"))
        elif pcsi > 0.55:
            alerts.append(("🟡 WARNING", f"PCSI = {pcsi:.3f} in transitional zone"))
        
        # Check acceleration
        if len(self.history) >= 10:
            recent_pcsi = [h['pcsi'] for h in self.history[-10:]]
            if len(recent_pcsi) >= 2:
                rate = (recent_pcsi[-1] - recent_pcsi[0]) / len(recent_pcsi)
                if rate > 0.01:
                    alerts.append(("🔴 ACCEL", f"PCSI accelerating at {rate:.4f}/update"))
        
        if not alerts:
            return ""
        
        output = f"╠{'═' * (self.width-2)}╣\n"
        output += f"║  {'⚠️  ALERTS ⚠️':^{self.width-6}}  ║\n"
        output += f"╠{'═' * (self.width-2)}╣\n"
        
        for level, msg in alerts:
            output += f"║  {level}: {msg:<{self.width-15}}  ║\n"
        
        return output
    
    def render(self) -> str:
        """Render complete dashboard"""
        if not self.carbonica:
            return "CARBONICA instance not set"
        
        # Update data
        data = self.update()
        
        # Build dashboard
        dashboard = self.render_header()
        dashboard += self.render_pcsi_gauge(data['pcsi'])
        dashboard += self.render_parameters(data['parameters'])
        dashboard += self.render_history()
        dashboard += self.render_alerts()
        dashboard += f"╚{'═' * (self.width-2)}╝\n"
        
        return dashboard
    
    def live_dashboard(self, refresh_seconds: int = 5):
        """Run live updating dashboard"""
        import time
        import sys
        
        try:
            while True:
                # Clear screen
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Render and print
                print(self.render())
                
                # Wait
                time.sleep(refresh_seconds)
                
        except KeyboardInterrupt:
            print("\n\n📊 Dashboard stopped")
    
    def export_html(self, filepath: str = "dashboard.html") -> str:
        """Export dashboard as HTML (simplified)"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>CARBONICA Dashboard</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #0f0; padding: 20px; }}
        .dashboard {{ border: 2px solid #0f0; padding: 20px; max-width: 800px; }}
        .pcsi-gauge {{ background: #111; padding: 10px; margin: 10px 0; }}
        .parameters {{ background: #111; padding: 10px; margin: 10px 0; }}
        .critical {{ color: #f00; }}
        .transitional {{ color: #ff0; }}
        .stable {{ color: #0f0; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>🌍 CARBONICA Planetary Carbon Dashboard</h1>
        <p>Version: 1.0.0 | DOI: 10.5281/zenodo.18995446</p>
        <p>Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="pcsi-gauge">
            <h2>PCSI: {data['pcsi']:.3f} / 1.00</h2>
            <p>Status: {data['status']}</p>
        </div>
        
        <div class="parameters">
            <h2>Eight Parameters (2025)</h2>
            <pre>{self.render_parameters(data['parameters'])}</pre>
        </div>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return filepath
