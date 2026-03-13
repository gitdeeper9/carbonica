"""
Unit tests for CUSUM change point detection
"""

import pytest
from carbonica.statistics.cusum import CUSUMDetector


class TestCUSUM:
    """Test CUSUM detector"""
    
    def test_initialization(self):
        """Test initialization"""
        cusum = CUSUMDetector(threshold=2.0, drift=0.5)
        assert cusum.threshold == 2.0
        assert cusum.drift == 0.5
    
    def test_detect_no_change(self):
        """Test detection with no change"""
        cusum = CUSUMDetector()
        data = [10, 10, 10, 10, 10, 10]
        
        result = cusum.detect(data)
        assert not result['significant']
        assert len(result['change_points']) == 0
    
    def test_detect_step_change(self):
        """Test detection of step change"""
        cusum = CUSUMDetector(threshold=2.0)
        # Mean shift at index 5
        data = [10, 10, 10, 10, 10, 20, 20, 20, 20, 20]
        
        result = cusum.detect(data)
        assert result['significant']
        assert len(result['change_points']) > 0
    
    def test_detect_multiple(self):
        """Test multiple change point detection"""
        cusum = CUSUMDetector(threshold=2.0)
        # Two shifts
        data = [10, 10, 10, 20, 20, 20, 15, 15, 15]
        
        changes = cusum.detect_multiple(data, min_segment=2)
        assert len(changes) >= 1
    
    def test_segment_series(self):
        """Test series segmentation"""
        cusum = CUSUMDetector()
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        change_points = [3, 7]
        
        segments = cusum.segment_series(data, change_points)
        assert len(segments) == 3
        assert segments[0] == [1, 2, 3]
        assert segments[1] == [4, 5, 6, 7]
        assert segments[2] == [8, 9, 10]
    
    def test_get_segment_means(self):
        """Test segment means"""
        cusum = CUSUMDetector()
        data = [1, 1, 1, 10, 10, 10, 5, 5, 5]
        change_points = [3, 6]
        
        means = cusum.get_segment_means(data, change_points)
        assert len(means) == 3
        assert means[0][2] == 1.0  # First segment mean
        assert means[1][2] == 10.0  # Second segment mean
        assert means[2][2] == 5.0   # Third segment mean
    
    def test_summary(self):
        """Test summary generation"""
        cusum = CUSUMDetector()
        data = [10, 10, 10, 20, 20, 20]
        
        summary = cusum.summary(data)
        assert 'CUSUM' in summary
        assert 'Change Detection' in summary
