import pytest
from carbonica.statistics.simple_stats import SimpleStats

class TestSimpleStats:
    def test_mean(self):
        assert SimpleStats.mean([1,2,3]) == 2.0
    
    def test_correlation(self):
        x = [1,2,3,4,5]
        y = [2,4,6,8,10]
        corr = SimpleStats.correlation(x, y)
        assert abs(corr - 1.0) < 1e-10

