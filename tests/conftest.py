"""
CARBONICA Test Configuration
Shared fixtures for all tests
"""

import os
import sys
import pytest
import tempfile
import json
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from carbonica import CARBONICA
from carbonica.pcsi import PCSI


@pytest.fixture
def carbonica_instance():
    """Create CARBONICA instance for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        instance = CARBONICA(data_dir=tmpdir)
        yield instance


@pytest.fixture
def pcsi_calculator():
    """Create PCSI calculator for testing"""
    return PCSI()


@pytest.fixture
def sample_parameters_2025():
    """Sample parameters for 2025"""
    return {
        'NPP': 58.3,
        'S_ocean': -3.08,
        'G_atm': 2.38,
        'F_perma': 1.71,
        'beta': 0.081,
        'tau_soil': 27,
        'E_anth': 11.2,
        'Phi_q': 0.071
    }


@pytest.fixture
def sample_parameters_1960():
    """Sample parameters for 1960"""
    return {
        'NPP': 59.1,
        'S_ocean': -1.21,
        'G_atm': 0.90,
        'F_perma': 0.0,
        'beta': 0.098,
        'tau_soil': 30,
        'E_anth': 2.8,
        'Phi_q': 0.076
    }


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_keeling_data():
    """Sample Keeling curve data"""
    return [
        {'year': 1960, 'co2_ppm': 316.9},
        {'year': 1970, 'co2_ppm': 325.7},
        {'year': 1980, 'co2_ppm': 338.7},
        {'year': 1990, 'co2_ppm': 354.2},
        {'year': 2000, 'co2_ppm': 369.4},
        {'year': 2010, 'co2_ppm': 389.8},
        {'year': 2020, 'co2_ppm': 414.2},
        {'year': 2025, 'co2_ppm': 424.0}
    ]


@pytest.fixture
def sample_correlation_matrix():
    """Sample correlation matrix"""
    return {
        ('NPP', 'G_atm'): 0.31,
        ('NPP', 'Phi_q'): 0.78,
        ('G_atm', 'E_anth'): 0.86,
        ('S_ocean', 'beta'): -0.88,
        ('F_perma', 'tau_soil'): 0.77
    }
