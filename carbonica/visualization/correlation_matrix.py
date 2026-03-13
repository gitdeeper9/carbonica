"""
Correlation Matrix Visualization
Heatmap of correlations between eight CARBONICA parameters
"""

from typing import Dict, List, Optional, Tuple


class CorrelationMatrix:
    """
    Correlation matrix visualization for eight parameters
    
    Based on the correlation matrix from the research paper:
    https://carbonica.netlify.app/figures/correlation-matrix
    """
    
    def __init__(self):
        """Initialize correlation matrix"""
        # Correlation matrix from paper (Table in Section 5.5)
        self.correlation_matrix = {
            ('NPP', 'NPP'): 1.00, ('NPP', 'S_ocean'): -0.48, ('NPP', 'G_atm'): 0.31,
            ('NPP', 'F_perma'): -0.61, ('NPP', 'beta'): -0.52, ('NPP', 'tau_soil'): -0.43,
            ('NPP', 'E_anth'): -0.19, ('NPP', 'Phi_q'): 0.78,
            
            ('S_ocean', 'S_ocean'): 1.00, ('S_ocean', 'G_atm'): -0.73,
            ('S_ocean', 'F_perma'): -0.38, ('S_ocean', 'beta'): -0.88,
            ('S_ocean', 'tau_soil'): -0.35, ('S_ocean', 'E_anth'): -0.54,
            ('S_ocean', 'Phi_q'): -0.41,
            
            ('G_atm', 'G_atm'): 1.00, ('G_atm', 'F_perma'): 0.67,
            ('G_atm', 'beta'): 0.71, ('G_atm', 'tau_soil'): 0.49,
            ('G_atm', 'E_anth'): 0.86, ('G_atm', 'Phi_q'): 0.28,
            
            ('F_perma', 'F_perma'): 1.00, ('F_perma', 'beta'): 0.51,
            ('F_perma', 'tau_soil'): 0.77, ('F_perma', 'E_anth'): 0.59,
            ('F_perma', 'Phi_q'): -0.55,
            
            ('beta', 'beta'): 1.00, ('beta', 'tau_soil'): 0.43,
            ('beta', 'E_anth'): 0.62, ('beta', 'Phi_q'): -0.48,
            
            ('tau_soil', 'tau_soil'): 1.00, ('tau_soil', 'E_anth'): 0.39,
            ('tau_soil', 'Phi_q'): -0.38,
            
            ('E_anth', 'E_anth'): 1.00, ('E_anth', 'Phi_q'): -0.15,
            
            ('Phi_q', 'Phi_q'): 1.00
        }
        
        self.parameters = ['NPP', 'S_ocean', 'G_atm', 'F_perma', 
                          'beta', 'tau_soil', 'E_anth', 'Phi_q']
        
        # Color mapping
        self.color_map = {
            'very_strong_pos': '🔴',   # > 0.7
            'strong_pos': '🟠',         # 0.5-0.7
            'moderate_pos': '🟡',       # 0.3-0.5
            'weak_pos': '🟢',            # 0.1-0.3
            'none': '⚪',                # -0.1-0.1
            'weak_neg': '🔵',            # -0.3 - -0.1
            'moderate_neg': '🟣',        # -0.5 - -0.3
            'strong_neg': '🟤',          # -0.7 - -0.5
            'very_strong_neg': '⚫'      # < -0.7
        }
    
    def get_correlation(self, param1: str, param2: str) -> float:
        """Get correlation between two parameters"""
        return self.correlation_matrix.get((param1, param2),
               self.correlation_matrix.get((param2, param1), 0.0))
    
    def get_color(self, corr: float) -> str:
        """Get color for correlation value"""
        if corr > 0.7:
            return self.color_map['very_strong_pos']
        elif corr > 0.5:
            return self.color_map['strong_pos']
        elif corr > 0.3:
            return self.color_map['moderate_pos']
        elif corr > 0.1:
            return self.color_map['weak_pos']
        elif corr > -0.1:
            return self.color_map['none']
        elif corr > -0.3:
            return self.color_map['weak_neg']
        elif corr > -0.5:
            return self.color_map['moderate_neg']
        elif corr > -0.7:
            return self.color_map['strong_neg']
        else:
            return self.color_map['very_strong_neg']
    
    def render_text_matrix(self, width: int = 60) -> str:
        """Render text-based correlation matrix"""
        output = "\n📊 Parameter Correlation Matrix (1960-2025)\n"
        output += "═" * (len(self.parameters) * 8 + 12) + "\n\n"
        
        # Header
        output += " " * 12
        for p in self.parameters:
            output += f"{p:8s}"
        output += "\n"
        
        # Rows
        for p1 in self.parameters:
            output += f"{p1:12s}"
            for p2 in self.parameters:
                corr = self.get_correlation(p1, p2)
                color = self.get_color(corr)
                output += f" {color}{corr:6.2f} "
            output += "\n"
        
        output += "\n" + "═" * (len(self.parameters) * 8 + 12) + "\n"
        
        # Legend
        output += "\nLegend:\n"
        output += f"{self.color_map['very_strong_pos']} > 0.7  "
        output += f"{self.color_map['strong_pos']} 0.5-0.7  "
        output += f"{self.color_map['moderate_pos']} 0.3-0.5  "
        output += f"{self.color_map['weak_pos']} 0.1-0.3  "
        output += f"{self.color_map['none']} -0.1-0.1\n"
        output += f"{self.color_map['weak_neg']} -0.3- -0.1  "
        output += f"{self.color_map['moderate_neg']} -0.5- -0.3  "
        output += f"{self.color_map['strong_neg']} -0.7- -0.5  "
        output += f"{self.color_map['very_strong_neg']} < -0.7\n"
        
        return output
    
    def get_strongest_correlations(self, n: int = 5) -> List[Tuple[str, str, float]]:
        """Get strongest correlations (absolute value)"""
        correlations = []
        
        for i, p1 in enumerate(self.parameters):
            for p2 in self.parameters[i+1:]:
                corr = self.get_correlation(p1, p2)
                correlations.append((p1, p2, corr, abs(corr)))
        
        # Sort by absolute value
        correlations.sort(key=lambda x: x[3], reverse=True)
        
        return [(p1, p2, corr) for p1, p2, corr, _ in correlations[:n]]
    
    def get_positive_feedbacks(self) -> List[Tuple[str, str, float]]:
        """Get positive feedback loops (both directions positive)"""
        feedbacks = []
        
        # Check each pair
        for i, p1 in enumerate(self.parameters):
            for p2 in self.parameters[i+1:]:
                corr = self.get_correlation(p1, p2)
                if corr > 0.5:  # Strong positive correlation
                    feedbacks.append((p1, p2, corr))
        
        return feedbacks
    
    def get_negative_feedbacks(self) -> List[Tuple[str, str, float]]:
        """Get negative feedback loops (one direction negative)"""
        feedbacks = []
        
        for i, p1 in enumerate(self.parameters):
            for p2 in self.parameters[i+1:]:
                corr = self.get_correlation(p1, p2)
                if corr < -0.5:  # Strong negative correlation
                    feedbacks.append((p1, p2, corr))
        
        return feedbacks
    
    def summary(self) -> str:
        """Print correlation matrix summary"""
        strongest = self.get_strongest_correlations(5)
        positive = self.get_positive_feedbacks()
        negative = self.get_negative_feedbacks()
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║              Correlation Matrix Summary                        ║
╠════════════════════════════════════════════════════════════════╣
║  Strongest Correlations:                                       ║
        """
        
        for i, (p1, p2, corr) in enumerate(strongest, 1):
            summary += f"\n║    {i}. {p1:8s} ↔ {p2:8s} : {corr:6.2f}"
        
        summary += f"""
╠════════════════════════════════════════════════════════════════╣
║  Key Findings (from paper):                                   ║
║    • G_atm ↔ E_anth    : 0.86 (direct emission link)         ║
║    • S_ocean ↔ β       : -0.88 (ocean buffer chemistry)      ║
║    • F_perma ↔ τ_soil  : 0.77 (temperature driver)           ║
║    • NPP ↔ Φ_q         : 0.78 (photosynthetic efficiency)    ║
╚════════════════════════════════════════════════════════════════╝
        """
        return summary
    
    def to_dict(self) -> Dict:
        """Export correlation matrix to dictionary"""
        matrix = {}
        for p1 in self.parameters:
            for p2 in self.parameters:
                matrix[f"{p1}_{p2}"] = self.get_correlation(p1, p2)
        return matrix
    
    def to_csv(self, filepath: str = "correlation_matrix.csv") -> str:
        """Export correlation matrix to CSV"""
        with open(filepath, 'w') as f:
            # Header
            f.write("," + ",".join(self.parameters) + "\n")
            
            # Rows
            for p1 in self.parameters:
                row = [p1]
                for p2 in self.parameters:
                    row.append(str(self.get_correlation(p1, p2)))
                f.write(",".join(row) + "\n")
        
        return filepath
