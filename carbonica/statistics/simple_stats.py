"""
Simple Statistics Module
Basic statistical functions without NumPy
"""

import math
from typing import List, Dict, Optional, Tuple


class SimpleStats:
    """
    Simple statistical calculations without external dependencies
    """
    
    @staticmethod
    def mean(values: List[float]) -> float:
        """Calculate arithmetic mean"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def median(values: List[float]) -> float:
        """Calculate median"""
        if not values:
            return 0.0
        
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mid = n // 2
        
        if n % 2 == 0:
            return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        else:
            return sorted_vals[mid]
    
    @staticmethod
    def variance(values: List[float], ddof: int = 1) -> float:
        """Calculate variance"""
        if len(values) < 2:
            return 0.0
        
        m = SimpleStats.mean(values)
        squared_diffs = [(x - m) ** 2 for x in values]
        return sum(squared_diffs) / (len(values) - ddof)
    
    @staticmethod
    def std(values: List[float], ddof: int = 1) -> float:
        """Calculate standard deviation"""
        return math.sqrt(SimpleStats.variance(values, ddof))
    
    @staticmethod
    def percentile(values: List[float], p: float) -> float:
        """Calculate percentile (0-100)"""
        if not values:
            return 0.0
        
        sorted_vals = sorted(values)
        k = (len(sorted_vals) - 1) * (p / 100)
        f = int(k)
        c = int(k) + 1 if int(k) + 1 < len(sorted_vals) else int(k)
        
        if f == c:
            return sorted_vals[f]
        
        return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])
    
    @staticmethod
    def min_max_norm(values: List[float]) -> List[float]:
        """Min-max normalization to [0, 1]"""
        if not values:
            return []
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val - min_val == 0:
            return [0.5 for _ in values]
        
        return [(x - min_val) / (max_val - min_val) for x in values]
    
    @staticmethod
    def zscore_norm(values: List[float]) -> List[float]:
        """Z-score normalization (mean=0, std=1)"""
        if len(values) < 2:
            return [0.0 for _ in values]
        
        m = SimpleStats.mean(values)
        s = SimpleStats.std(values)
        
        if s == 0:
            return [0.0 for _ in values]
        
        return [(x - m) / s for x in values]
    
    @staticmethod
    def correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        mean_x = SimpleStats.mean(x)
        mean_y = SimpleStats.mean(y)
        
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = SimpleStats.std(x)
        std_y = SimpleStats.std(y)
        
        if std_x == 0 or std_y == 0:
            return 0.0
        
        return cov / ((n - 1) * std_x * std_y)
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Dict:
        """
        Simple linear regression
        
        Returns
        -------
        dict
            {'slope': m, 'intercept': b, 'r2': r_squared}
        """
        if len(x) != len(y) or len(x) < 2:
            return {'slope': 0, 'intercept': 0, 'r2': 0}
        
        n = len(x)
        mean_x = SimpleStats.mean(x)
        mean_y = SimpleStats.mean(y)
        
        # Calculate slope
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Calculate intercept
        intercept = mean_y - slope * mean_x
        
        # Calculate R²
        y_pred = [slope * xi + intercept for xi in x]
        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        if ss_tot == 0:
            r2 = 0
        else:
            r2 = 1 - ss_res / ss_tot
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r2': r2
        }
    
    @staticmethod
    def weighted_average(values: List[float], weights: List[float]) -> float:
        """Calculate weighted average"""
        if len(values) != len(weights) or not values:
            return 0.0
        
        total_weight = sum(weights)
        if total_weight == 0:
            return 0.0
        
        return sum(v * w for v, w in zip(values, weights)) / total_weight
    
    @staticmethod
    def exponential_moving_average(values: List[float], alpha: float = 0.3) -> List[float]:
        """
        Calculate exponential moving average
        
        Parameters
        ----------
        values : list
            Input time series
        alpha : float
            Smoothing factor (0-1)
        
        Returns
        -------
        list
            Smoothed series
        """
        if not values:
            return []
        
        ema = [values[0]]
        
        for i in range(1, len(values)):
            ema.append(alpha * values[i] + (1 - alpha) * ema[-1])
        
        return ema
