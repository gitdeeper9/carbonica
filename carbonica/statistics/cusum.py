"""
CUSUM Change Point Detection
Detecting rate-of-change anomalies in time series
"""

import math
from typing import List, Dict, Optional, Tuple


class CUSUMDetector:
    """
    Cumulative Sum (CUSUM) change point detection
    
    Detects when the mean of a time series changes significantly.
    """
    
    def __init__(self, threshold: float = 2.0, drift: float = 0.0):
        """
        Initialize CUSUM detector
        
        Parameters
        ----------
        threshold : float
            Detection threshold (in standard deviations)
        drift : float
            Allowable drift
        """
        self.threshold = threshold
        self.drift = drift
    
    def detect(self, timeseries: List[float], 
               target_mean: Optional[float] = None) -> Dict:
        """
        Detect change points in time series
        
        Parameters
        ----------
        timeseries : list
            Time series data
        target_mean : float, optional
            Target mean (if None, uses series mean)
        
        Returns
        -------
        dict
            Change point detection results
        """
        if len(timeseries) < 2:
            return {
                'change_points': [],
                'cusum_low': [],
                'cusum_high': [],
                'significant': False
            }
        
        # Use series mean if target not provided
        if target_mean is None:
            target_mean = sum(timeseries) / len(timeseries)
        
        # Calculate standard deviation
        std_dev = math.sqrt(
            sum((x - target_mean) ** 2 for x in timeseries) / (len(timeseries) - 1)
        )
        
        # Initialize CUSUM
        cusum_low = [0.0]
        cusum_high = [0.0]
        change_points = []
        
        for i, value in enumerate(timeseries[1:], 1):
            # Update CUSUM statistics
            cusum_low.append(max(0, cusum_low[-1] + target_mean - value - self.drift))
            cusum_high.append(max(0, cusum_high[-1] + value - target_mean - self.drift))
            
            # Check for change
            if cusum_high[-1] > self.threshold * std_dev:
                change_points.append(i)
                cusum_high[-1] = 0
                cusum_low[-1] = 0
            elif cusum_low[-1] > self.threshold * std_dev:
                change_points.append(i)
                cusum_high[-1] = 0
                cusum_low[-1] = 0
        
        return {
            'change_points': change_points,
            'cusum_low': cusum_low,
            'cusum_high': cusum_high,
            'target_mean': target_mean,
            'std_dev': std_dev,
            'significant': len(change_points) > 0
        }
    
    def detect_multiple(self, timeseries: List[float], 
                       min_segment: int = 5) -> List[Dict]:
        """
        Detect multiple change points recursively
        
        Parameters
        ----------
        timeseries : list
            Time series data
        min_segment : int
            Minimum segment length
        
        Returns
        -------
        list
            List of change point dictionaries
        """
        result = self.detect(timeseries)
        
        if not result['significant'] or len(timeseries) < 2 * min_segment:
            return []
        
        change_points = []
        cp_idx = result['change_points'][0]
        
        # Split series at change point
        left_series = timeseries[:cp_idx]
        right_series = timeseries[cp_idx:]
        
        # Recursively detect in segments
        if len(left_series) >= min_segment:
            left_cps = self.detect_multiple(left_series, min_segment)
            for cp in left_cps:
                change_points.append(cp)
        
        change_points.append({
            'index': cp_idx,
            'value': timeseries[cp_idx],
            'cusum': result['cusum_high'][cp_idx] if result['cusum_high'][cp_idx] > 0 
                     else -result['cusum_low'][cp_idx]
        })
        
        if len(right_series) >= min_segment:
            right_cps = self.detect_multiple(right_series, min_segment)
            for cp in right_cps:
                change_points.append({
                    'index': cp['index'] + cp_idx,
                    'value': cp['value'],
                    'cusum': cp['cusum']
                })
        
        return sorted(change_points, key=lambda x: x['index'])
    
    def segment_series(self, timeseries: List[float],
                      change_points: List[int]) -> List[List[float]]:
        """
        Split time series at change points
        
        Parameters
        ----------
        timeseries : list
            Time series data
        change_points : list
            Change point indices
        
        Returns
        -------
        list
            List of segments
        """
        if not change_points:
            return [timeseries]
        
        segments = []
        start = 0
        
        for cp in sorted(change_points):
            if cp > start:
                segments.append(timeseries[start:cp])
                start = cp
        
        if start < len(timeseries):
            segments.append(timeseries[start:])
        
        return segments
    
    def get_segment_means(self, timeseries: List[float],
                         change_points: List[int]) -> List[Tuple[int, int, float]]:
        """
        Get mean of each segment
        
        Returns
        -------
        list
            List of (start, end, mean) tuples
        """
        segments = self.segment_series(timeseries, change_points)
        result = []
        start = 0
        
        for i, seg in enumerate(segments):
            end = start + len(seg)
            mean_val = sum(seg) / len(seg) if seg else 0
            result.append((start, end, mean_val))
            start = end
        
        return result
    
    def summary(self, timeseries: List[float]) -> str:
        """Print CUSUM analysis summary"""
        result = self.detect(timeseries)
        segments = self.get_segment_means(timeseries, result['change_points'])
        
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║                    CUSUM Change Detection                      ║
╠════════════════════════════════════════════════════════════════╣
║  Series length     : {len(timeseries)} points                       ║
║  Target mean       : {result['target_mean']:.3f}                      ║
║  Standard deviation: {result['std_dev']:.3f}                      ║
║  Change points     : {result['change_points']}                          ║
║  Significant       : {result['significant']}                         ║
╠════════════════════════════════════════════════════════════════╣
║  Segments:                                                     ║
        """
        
        for i, (start, end, mean_val) in enumerate(segments):
            summary += f"\n║    {i+1}: {start:3d}-{end-1:3d} → mean = {mean_val:.3f}"
        
        summary += "\n╚════════════════════════════════════════════════════════════════╝"
        
        return summary
