# 🤝 Contributing to CARBONICA

## Advanced Planetary Carbon Accounting & Feedback Dynamics

**DOI**: 10.5281/zenodo.18995446  
**Repository**: github.com/gitdeeper9/carbonica  
**Web**: carbonica.netlify.app

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contributing to Physics Modules](#contributing-to-physics-modules)
- [Contributing to Data Processing](#contributing-to-data-processing)
- [Contributing to Documentation](#contributing-to-documentation)
- [Testing Guidelines](#testing-guidelines)
- [Data Contributions](#data-contributions)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

### Our Pledge
We as members, contributors, and leaders pledge to make participation in the CARBONICA community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members
- Acknowledging the global importance of climate science and carbon cycle research
- Promoting open science and reproducible research

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gitdeeper@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install development dependencies
python --version  # 3.9-3.11 required
git --version     # 2.30+ recommended
docker --version  # 20.10+ for containerized development
```

Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/carbonica.git
cd carbonica

# Add upstream remote
git remote add upstream https://github.com/gitdeeper9/carbonica.git
```

Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install --upgrade pip
pip install -e .[dev]
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial setup
python scripts/init_dev.py
```

Development Tools

```bash
# Code formatting
black carbonica/ tests/
isort carbonica/ tests/

# Linting
flake8 carbonica/ tests/ --max-line-length=100
pylint carbonica/ tests/

# Type checking
mypy carbonica/ --ignore-missing-imports

# Testing
pytest tests/ -v --cov=carbonica --numprocesses=auto
```

---

🔄 Development Workflow

Branch Naming Convention

```
feature/        # New features (e.g., feature/methane-module)
bugfix/         # Bug fixes (e.g., bugfix/revelle-calculation)
docs/           # Documentation (e.g., docs/api-refactor)
physics/        # Physics module updates (e.g., physics/permafrost-q10)
data/           # Data contributions (e.g., data/new-carbon-flux-2025)
parameter/      # Parameter updates (e.g., parameter/pcsi-weights)
```

Development Process

```bash
# 1. Update your main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... code changes ...

# 4. Run tests locally
pytest tests/ -v

# 5. Commit with conventional commit message
git add .
git commit -m "feat: add methane cycle module for CARBONICA v2.0"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create Pull Request on GitHub
```

Commit Message Convention

We follow Conventional Commits with scientific context:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation only
· style: Code style (formatting)
· refactor: Code change that neither fixes bug nor adds feature
· perf: Performance improvement
· test: Adding missing tests
· chore: Changes to build process or auxiliary tools
· physics: Changes to physics equations or parameters
· data: Data additions or updates
· parameter: Parameter or weight updates

Examples:

```
feat(permafrost): add Q₁₀ = 3.5 for Yedoma deposits based on Schuur et al. 2015
fix(ocean): correct Revelle Factor calculation in beta time series
docs(pcsi): update threshold values based on 2025 validation
physics: refine NPP LUE model with vapor pressure deficit stress function
data: add 2025 atmospheric CO₂ data from NOAA/Scripps
parameter: update PCSI weights based on 1960-2025 PCA regression
```

---

🔬 Contributing to Physics Modules

Core Physics Equations

CARBONICA is built on eight governing equations from the research paper:

```python
# carbonica/physics/npp.py
def compute_net_primary_productivity(quantum_yield, fapar, lue_max,
                                     shortwave_radiation, temperature, vpd):
    """
    Compute Net Primary Productivity (NPP)
    
    NPP = Φ_q · fAPAR · LUE_max · SW_in · f(T) · f(VPD)
    
    Parameters
    ----------
    quantum_yield : float
        Photosynthetic quantum yield Φ_q (mol C / mol photons)
        Theoretical max: 0.125 for C3 plants
        Observed global mean: 0.055-0.075
    fapar : float
        Fraction of absorbed photosynthetically active radiation
        From MODIS NDVI retrievals
    lue_max : float
        Biome-specific maximum light use efficiency (gC/MJ)
        Range: 0.389 (tropical) to 0.608 (croplands)
    shortwave_radiation : float
        Incident shortwave radiation (W/m²)
    temperature : float
        Temperature (°C)
    vpd : float
        Vapor pressure deficit (kPa)
    
    Returns
    -------
    float
        Net Primary Productivity (PgC/yr)
    
    Notes
    -----
    Global NPP 2020-2025 mean: 58.3 ± 4.2 PgC/yr
    Critical threshold: < 52.0 PgC/yr (sink collapse)
    """
    # Temperature limitation function (Gaussian)
    t_opt = 22.5  # Optimal temperature (°C)
    t_width = 15.0  # Width parameter
    f_temp = np.exp(-((temperature - t_opt) / t_width) ** 2)
    
    # VPD stress function
    f_vpd = np.exp(-vpd / 2.5) if vpd > 0 else 1.0
    
    # LUE model
    npp = quantum_yield * fapar * lue_max * shortwave_radiation * f_temp * f_vpd
    
    return npp
```

```python
# carbonica/physics/ocean_sink.py
def compute_ocean_carbon_sink(wind_speed_10m, sea_surface_temperature,
                              salinity, pco2_atm, pco2_sw):
    """
    Compute Oceanic Carbon Sink Strength (S_ocean)
    
    F_as = k_w · K_0 · (pCO₂_atm − pCO₂_sw)
    k_w = 0.251 · u₁₀² · (Sc/660)^(-0.5) [Wanninkhof, 2014]
    
    Parameters
    ----------
    wind_speed_10m : float
        Wind speed at 10m height (m/s)
    sea_surface_temperature : float
        Sea surface temperature (°C)
    salinity : float
        Salinity (PSU)
    pco2_atm : float
        Atmospheric CO₂ partial pressure (µatm)
    pco2_sw : float
        Surface seawater CO₂ partial pressure (µatm)
    
    Returns
    -------
    float
        Ocean carbon sink strength (PgC/yr)
    
    Notes
    -----
    Current sink (2025): −3.08 PgC/yr
    Critical threshold: < −1.5 PgC/yr (weakening alarm)
    """
    # Schmidt number calculation
    sc = 2073.1 - 125.62 * sst + 3.6276 * sst**2 - 0.043219 * sst**3
    
    # Gas transfer velocity
    k_w = 0.251 * wind_speed_10m**2 * (sc / 660) ** (-0.5)
    
    # CO₂ solubility (Henry's Law)
    K0 = np.exp(9345.17 / (sst + 273.15) - 60.2409 + 23.3585 * np.log((sst + 273.15) / 100))
    
    # Air-sea flux
    F_as = k_w * K0 * (pco2_atm - pco2_sw)
    
    return F_as
```

```python
# carbonica/physics/revelle.py
def compute_revelle_factor(dic, alkalinity, temperature, salinity):
    """
    Compute Revelle Factor (R)
    
    R = (∂ln pCO₂) / (∂ln DIC) = DIC / (pCO₂ · ∂DIC/∂pCO₂)
    β = 1/R (Buffer Capacity)
    
    Parameters
    ----------
    dic : float
        Dissolved Inorganic Carbon (µmol/kg)
    alkalinity : float
        Total Alkalinity (µmol/kg)
    temperature : float
        Temperature (°C)
    salinity : float
        Salinity (PSU)
    
    Returns
    -------
    float
        Revelle Factor R
    
    Notes
    -----
    Pre-industrial (1750): R = 9.1
    Keeling baseline (1960): R = 10.2
    Current (2025): R = 12.4 (36% buffer reduction)
    Critical threshold: R ≥ 14.0 (β ≤ 0.071)
    """
    # Solve carbonate system
    # Implementation of CO2SYS algorithms
    # Returns Revelle Factor
    
    return revelle_factor
```

```python
# carbonica/physics/permafrost.py
def compute_permafrost_thaw_flux(permafrost_carbon_density,
                                  active_layer_depth, temperature,
                                  q10=2.5, area_thawing=None):
    """
    Compute Permafrost Thaw Flux (F_perma)
    
    F_perma = C_perma · k_decomp(T) · A_thaw(t) / τ_frozen
    k_decomp(T) = k₀ · Q₁₀^((T−T_ref)/10)
    
    Parameters
    ----------
    permafrost_carbon_density : float
        Carbon density (kgC/m²)
        Mean: 28.1 kgC/m² for continuous permafrost
    active_layer_depth : float
        Active layer depth (m)
    temperature : float
        Temperature anomaly above baseline (°C)
    q10 : float
        Temperature sensitivity coefficient
        2.1 (mineral soils), 3.5 (Yedoma deposits)
    area_thawing : float, optional
        Area of actively thawing permafrost (m²)
    
    Returns
    -------
    float
        Permafrost thaw flux (PgC/yr)
    
    Notes
    -----
    Current flux (2025): 1.71 ± 0.4 PgC/yr
    Critical threshold: ≥ 2.8 PgC/yr (self-sustaining)
    Abrupt thaw (thermokarst): 31% of current flux from 5% of area
    """
    # Temperature-dependent decomposition
    k_decomp = q10 ** ((temperature - 0) / 10)
    
    # Flux calculation
    F_perma = permafrost_carbon_density * k_decomp * area_thawing / 1000  # Convert to PgC
    
    return F_perma
```

```python
# carbonica/physics/pcsi.py
def compute_pcsi(parameters, weights=None):
    """
    Compute Planetary Carbon Saturation Index (PCSI)
    
    PCSI = w₁·NPP* + w₂·S*_ocean + w₃·G*_atm + w₄·F*_perma +
           w₅·β* + w₆·τ*_soil + w₇·E*_anth + w₈·Φ*_q
    
    Default weights (PCA-regularized regression):
    w₁=0.16, w₂=0.18, w₃=0.20, w₄=0.19, w₅=0.12, w₆=0.07, w₇=0.05, w₈=0.03
    
    Parameters
    ----------
    parameters : dict
        Dictionary with keys: 'NPP', 'S_ocean', 'G_atm', 'F_perma',
                              'beta', 'tau_soil', 'E_anth', 'Phi_q'
    weights : dict, optional
        Custom weights for each parameter
    
    Returns
    -------
    float
        PCSI value (0-1)
    
    Thresholds:
    - PCSI < 0.55: STABLE - sinks dominating
    - PCSI 0.55-0.80: TRANSITIONAL - sink weakening detectable
    - PCSI > 0.80: CRITICAL - self-reinforcing feedbacks emerging
    - PCSI = 1.00: SATURATION - irreversible runaway carbon feedback
    
    Current PCSI (2025): 0.78
    """
    # Normalize each parameter to [0,1]
    normalized = {}
    
    # NPP: 0 = pre-industrial (60.2), 1 = critical (52.0)
    normalized['NPP'] = max(0, min(1, (60.2 - parameters['NPP']) / 8.2))
    
    # S_ocean: 0 = pre-industrial (-0.18), 1 = critical (-1.5)
    normalized['S_ocean'] = max(0, min(1, (parameters['S_ocean'] + 0.18) / 1.32))
    
    # G_atm: 0 = pre-industrial (0.002), 1 = critical (3.5)
    normalized['G_atm'] = max(0, min(1, parameters['G_atm'] / 3.5))
    
    # F_perma: 0 = pre-industrial (0), 1 = critical (2.8)
    normalized['F_perma'] = max(0, min(1, parameters['F_perma'] / 2.8))
    
    # beta: 0 = pre-industrial (0.110), 1 = critical (0.071)
    normalized['beta'] = max(0, min(1, (0.110 - parameters['beta']) / 0.039))
    
    # tau_soil: 0 = pre-industrial (32), 1 = critical (18)
    normalized['tau_soil'] = max(0, min(1, (32 - parameters['tau_soil']) / 14))
    
    # E_anth: 0 = pre-industrial (0), 1 = critical (10) [net-zero by 2050]
    normalized['E_anth'] = max(0, min(1, parameters['E_anth'] / 10))
    
    # Phi_q: 0 = pre-industrial (0.078), 1 = critical (0.040)
    normalized['Phi_q'] = max(0, min(1, (0.078 - parameters['Phi_q']) / 0.038))
    
    # Apply weights
    default_weights = {'NPP': 0.16, 'S_ocean': 0.18, 'G_atm': 0.20,
                       'F_perma': 0.19, 'beta': 0.12, 'tau_soil': 0.07,
                       'E_anth': 0.05, 'Phi_q': 0.03}
    
    w = weights or default_weights
    
    pcsi = sum(w[key] * normalized[key] for key in parameters)
    
    return pcsi
```

Adding New Physics Models

```python
# carbonica/physics/new_model.py
"""
Template for contributing new physics models
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class NewModelConfig:
    """Configuration for new physics model"""
    parameter1: float
    parameter2: float
    calibration_factor: Optional[float] = 1.0
    uncertainty_bounds: Tuple[float, float] = (0.0, 1.0)

class NewPhysicsModel:
    """
    New physics model implementation
    
    References
    ----------
    [1] Author et al. (2026) - DOI: 10.xxxx/xxxxx
    [2] CARBONICA Research Paper - DOI: 10.5281/zenodo.18995446
    """
    
    def __init__(self, config: Dict):
        self.config = NewModelConfig(**config)
        self.validate_against_observations()
    
    def compute(self, input_data: np.ndarray) -> float:
        """
        Compute model output
        
        Parameters
        ----------
        input_data : np.ndarray
            Input data
        
        Returns
        -------
        float
            Model output
        """
        # Implement your model here
        result = self.config.parameter1 * np.mean(input_data)
        return result * self.config.calibration_factor
    
    def validate_against_observations(self):
        """Validate model against observational data"""
        # Load validation data from Keeling Curve, SOCAT, MODIS, etc.
        # Compare predictions with observations
        # Report validation metrics
        # Ensure r² ≥ 0.90 for acceptance
        pass
    
    def get_references(self) -> list:
        """Return list of academic references"""
        return [
            "Author, A. et al. (2026). Title. Journal, volume, pages.",
            "Baladi, S. (2026). CARBONICA Research Paper. DOI: 10.5281/zenodo.18995446"
        ]
    
    def get_uncertainty(self) -> float:
        """Return uncertainty estimate"""
        return self.config.uncertainty_bounds[1] - self.config.uncertainty_bounds[0]
```

---

📊 Contributing to Data Processing

Data Loaders

```python
# carbonica/data/loaders/keeling.py
"""
NOAA Mauna Loa Keeling Curve data loader

Atmospheric CO₂ measurements (1960-2025)
"""

import pandas as pd
import requests
from typing import Optional

class KeelingLoader:
    """
    Loader for NOAA/Scripps Keeling Curve data
    
    Provides monthly mean CO₂ concentrations from Mauna Loa Observatory
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or "data/raw"
        self.url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    
    def load_local(self, filename: str = "co2_mm_mlo.txt") -> pd.DataFrame:
        """
        Load data from local file
        
        Parameters
        ----------
        filename : str
            Local filename
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns: year, month, decimal_date, co2_ppm
        """
        filepath = f"{self.data_dir}/{filename}"
        df = pd.read_csv(filepath, comment='#', delim_whitespace=True,
                         names=['year', 'month', 'decimal_date', 'co2_ppm',
                                'co2_unc', 'n_days'])
        return df
    
    def download_latest(self) -> pd.DataFrame:
        """
        Download latest data from NOAA
        
        Returns
        -------
        pd.DataFrame
            Latest Keeling Curve data
        """
        response = requests.get(self.url)
        lines = response.text.split('\n')
        
        # Parse data
        data = []
        for line in lines:
            if line.startswith('#'):
                continue
            if line.strip():
                parts = line.split()
                data.append({
                    'year': int(parts[0]),
                    'month': int(parts[1]),
                    'decimal_date': float(parts[2]),
                    'co2_ppm': float(parts[3]),
                    'co2_unc': float(parts[4]),
                    'n_days': int(parts[5])
                })
        
        return pd.DataFrame(data)
    
    def compute_growth_rate(self, df: pd.DataFrame) -> pd.Series:
        """
        Compute atmospheric CO₂ growth rate G_atm
        
        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with co2_ppm column
        
        Returns
        -------
        pd.Series
            Annual growth rate (ppm/yr)
        """
        # Group by year and compute annual mean
        annual = df.groupby('year')['co2_ppm'].mean()
        
        # Compute first difference (growth rate)
        growth_rate = annual.diff()
        
        return growth_rate
```

Carbon Budget Processing

```python
# carbonica/processing/budget.py
"""
Carbon Budget integration module

Implements the master dC_atm/dt equation with Monte Carlo uncertainty
"""

import numpy as np
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class CarbonBudgetConfig:
    """Configuration for Carbon Budget processing"""
    ensemble_size: int = 10000
    random_seed: int = 42
    change_point_detection: bool = True
    output_resolution: str = "monthly"

class CarbonBudget:
    """
    Real-time carbon budget integrator
    
    dC_atm/dt = E_anth + F_nat + F_perma − S_ocean − S_land
    where S_land = NPP − R_eco
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = CarbonBudgetConfig(**(config or {}))
        self.rng = np.random.default_rng(self.config.random_seed)
    
    def compute_budget(self, params: Dict[str, float]) -> Dict[str, float]:
        """
        Compute carbon budget for given parameters
        
        Parameters
        ----------
        params : dict
            Dictionary with keys: 'E_anth', 'F_nat', 'F_perma',
                                 'S_ocean', 'NPP', 'R_eco'
        
        Returns
        -------
        dict
            Budget components and dC_atm/dt
        """
        # Terrestrial sink
        s_land = params['NPP'] - params['R_eco']
        
        # Atmospheric growth rate
        dC_dt = (params['E_anth'] + params['F_nat'] + params['F_perma'] - 
                 params['S_ocean'] - s_land)
        
        return {
            'dC_dt': dC_dt,
            's_land': s_land,
            'dC_dt_ppm': dC_dt * 0.47  # Convert PgC to ppm (approx)
        }
    
    def propagate_uncertainty(self, params_with_uncertainty: Dict[str, tuple]) -> Dict:
        """
        Monte Carlo uncertainty propagation
        
        Parameters
        ----------
        params_with_uncertainty : dict
            Dictionary with parameter names as keys and
            (mean, std) tuples as values
        
        Returns
        -------
        dict
            Ensemble statistics
        """
        ensemble = []
        
        for _ in range(self.config.ensemble_size):
            # Sample each parameter
            sample = {}
            for name, (mean, std) in params_with_uncertainty.items():
                sample[name] = self.rng.normal(mean, std)
            
            # Compute budget
            result = self.compute_budget(sample)
            ensemble.append(result['dC_dt'])
        
        ensemble = np.array(ensemble)
        
        return {
            'mean': np.mean(ensemble),
            'std': np.std(ensemble),
            'p5': np.percentile(ensemble, 5),
            'p95': np.percentile(ensemble, 95),
            'ensemble': ensemble
        }
```

---

📚 Contributing to Documentation

Documentation Structure

```
docs/
├── api/                    # API documentation
│   ├── physics.md
│   ├── data.md
│   └── pcsi.md
├── tutorials/              # Step-by-step tutorials
│   ├── quickstart.md
│   ├── pcsi-calculation.md
│   ├── revelle-factor.md
│   └── case-studies/
│       ├── amazon-pivot.md
│       ├── arctic-carbon.md
│       └── mauna-loa.md
├── explanations/           # Conceptual guides
│   ├── carbon-cycle.md
│   ├── eight-parameters.md
│   ├── pcsi-explained.md
│   └── feedback-loops.md
├── theory/                 # Theoretical foundations
│   ├── box-model.md
│   ├── revelle-equation.md
│   ├── permafrost-q10.md
│   └── quantum-yield.md
└── contributing/           # Contribution guides
    └── style-guide.md
```

Docstring Style (NumPy/Google)

```python
def compute_pcsi(parameters: Dict[str, float], weights: Optional[Dict] = None) -> float:
    """
    Calculate Planetary Carbon Saturation Index from eight parameters.
    
    The PCSI is a weighted composite of normalized parameter values,
    ranging from 0 (pre-industrial stable state) to 1 (irreversible
    runaway carbon feedback).
    
    Parameters
    ----------
    parameters : Dict[str, float]
        Dictionary containing the eight CARBONICA parameters:
        - NPP : Net Primary Productivity (PgC/yr)
        - S_ocean : Oceanic carbon sink strength (PgC/yr)
        - G_atm : Atmospheric CO₂ growth rate (ppm/yr)
        - F_perma : Permafrost thaw flux (PgC/yr)
        - beta : Buffer capacity (1/R)
        - tau_soil : Soil carbon residence time (years)
        - E_anth : Anthropogenic emission factor (PgC/yr)
        - Phi_q : Photosynthetic quantum yield (mol C / mol photons)
    
    weights : Optional[Dict]
        Custom weights for each parameter. If None, uses PCA-derived
        weights from the 65-year training period:
        w = {'NPP': 0.16, 'S_ocean': 0.18, 'G_atm': 0.20,
             'F_perma': 0.19, 'beta': 0.12, 'tau_soil': 0.07,
             'E_anth': 0.05, 'Phi_q': 0.03}
    
    Returns
    -------
    float
        Planetary Carbon Saturation Index (0-1)
    
    Examples
    --------
    >>> params = {
    ...     'NPP': 58.3, 'S_ocean': -3.08, 'G_atm': 2.38,
    ...     'F_perma': 1.71, 'beta': 0.081, 'tau_soil': 27,
    ...     'E_anth': 11.2, 'Phi_q': 0.071
    ... }
    >>> pcsi = compute_pcsi(params)
    >>> print(f"{pcsi:.2f}")
    0.78
    
    Notes
    -----
    Reference thresholds:
    - PCSI < 0.55: STABLE - sinks dominating
    - 0.55 ≤ PCSI < 0.80: TRANSITIONAL - sink weakening
    - PCSI ≥ 0.80: CRITICAL - self-reinforcing feedbacks
    - PCSI = 1.00: SATURATION - irreversible runaway feedback
    
    References
    ----------
    .. [1] Baladi, S. (2026). CARBONICA Research Paper.
           DOI: 10.5281/zenodo.18995446
    """
    pass
```

Building Documentation Locally

```bash
# Install documentation tools
pip install mkdocs mkdocs-material mkdocstrings[python] pymdown-extensions

# Build docs
mkdocs build

# Serve locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

🧪 Testing Guidelines

Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── physics/
│   │   ├── test_npp.py
│   │   ├── test_ocean_sink.py
│   │   ├── test_revelle.py
│   │   ├── test_permafrost.py
│   │   └── test_pcsi.py
│   ├── data/
│   │   ├── test_keeling_loader.py
│   │   └── test_socat_loader.py
│   └── processors/
│       ├── test_uncertainty.py
│       └── test_change_point.py
├── integration/            # Integration tests
│   ├── test_full_pipeline.py
│   ├── test_pcsi_calculation.py
│   └── test_65year_validation.py
├── validation/             # Validation against observations
│   ├── test_keeling_curve.py
│   ├── test_revelle_glodap.py
│   └── test_amazon_case.py
└── conftest.py             # Shared fixtures
```

Writing Tests

```python
# tests/unit/physics/test_revelle.py
import pytest
import numpy as np
from carbonica.physics.revelle import compute_revelle_factor

class TestRevelleFactor:
    """Test suite for Revelle Factor calculations"""
    
    @pytest.mark.parametrize("dic,alkalinity,expected_range", [
        (2000, 2300, (9.0, 9.5)),    # Pre-industrial
        (2100, 2300, (10.0, 10.5)),  # 1960 baseline
        (2200, 2300, (12.0, 12.8)),  # 2025 current
    ])
    def test_revelle_range(self, dic, alkalinity, expected_range):
        """Test Revelle Factor range for different DIC values"""
        
        R = compute_revelle_factor(
            dic=dic,
            alkalinity=alkalinity,
            temperature=20.0,
            salinity=35.0
        )
        
        assert expected_range[0] <= R <= expected_range[1]
    
    def test_temperature_sensitivity(self):
        """Test Revelle Factor temperature dependence"""
        
        R_cold = compute_revelle_factor(
            dic=2150,
            alkalinity=2300,
            temperature=5.0,
            salinity=35.0
        )
        
        R_warm = compute_revelle_factor(
            dic=2150,
            alkalinity=2300,
            temperature=25.0,
            salinity=35.0
        )
        
        # R should decrease with temperature (CO₂ more soluble in cold water)
        assert R_cold < R_warm
    
    def test_historical_increase(self):
        """Test Revelle Factor increase from 1960 to 2025"""
        
        # 1960 conditions
        R_1960 = compute_revelle_factor(
            dic=2100,
            alkalinity=2300,
            temperature=20.0,
            salinity=35.0
        )
        
        # 2025 conditions
        R_2025 = compute_revelle_factor(
            dic=2200,
            alkalinity=2300,
            temperature=20.5,  # slight warming
            salinity=35.0
        )
        
        # Should increase by ~2.2
        increase = R_2025 - R_1960
        assert 2.0 <= increase <= 2.5

# tests/unit/physics/test_permafrost.py
class TestPermafrostFlux:
    """Test suite for permafrost thaw flux calculations"""
    
    def test_q10_sensitivity(self):
        """Test Q₁₀ temperature sensitivity"""
        from carbonica.physics.permafrost import compute_permafrost_thaw_flux
        
        # Same conditions, different Q₁₀
        flux_q10_2 = compute_permafrost_thaw_flux(
            permafrost_carbon_density=28.1,
            active_layer_depth=1.0,
            temperature=2.0,
            q10=2.0,
            area_thawing=1e12
        )
        
        flux_q10_3 = compute_permafrost_thaw_flux(
            permafrost_carbon_density=28.1,
            active_layer_depth=1.0,
            temperature=2.0,
            q10=3.0,
            area_thawing=1e12
        )
        
        # Q₁₀=3 should give ~1.5x higher flux than Q₁₀=2 for 2°C warming
        ratio = flux_q10_3 / flux_q10_2
        assert 1.4 <= ratio <= 1.6
    
    def test_abrupt_thaw_fraction(self):
        """Test abrupt thaw contribution"""
        from carbonica.physics.permafrost import PermafrostEngine
        
        engine = PermafrostEngine()
        
        # Simulate gradual thaw only
        gradual = engine.simulate_thaw(
            area_type='gradual',
            temperature_scenario='ssp3-70',
            year=2025
        )
        
        # Simulate including abrupt thaw
        with_abrupt = engine.simulate_thaw(
            area_type='total',
            temperature_scenario='ssp3-70',
            year=2025
        )
        
        # Abrupt thaw should contribute significant fraction
        abrupt_fraction = (with_abrupt - gradual) / with_abrupt
        assert 0.25 <= abrupt_fraction <= 0.35  # 25-35% from paper
```

Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=carbonica --cov-report=html

# Run specific test file
pytest tests/unit/physics/test_revelle.py -v

# Run tests matching pattern
pytest -k "permafrost"

# Run with parallel execution
pytest -n auto

# Run validation tests only
pytest tests/validation/ -v
```

---

🌍 Data Contributions

Contributing New Carbon Cycle Data

If you have carbon cycle data that could help validate or extend CARBONICA:

1. Prepare your data in the required format:

```python
# Required columns for CSV export
# year, month, NPP, S_ocean, G_atm, F_perma, beta, tau_soil, E_anth, Phi_q, PCSI, data_source
```

1. Include metadata:

```yaml
dataset:
  name: "Amazon Flux Tower Network 2025"
  description: "Eddy covariance measurements from Amazon rainforest"
  time_period: "2025-01-01 to 2025-12-31"
  location:
    latitude: -3.0 to -10.0
    longitude: -60.0 to -50.0
  measurement_type: "eddy_covariance"
  variables: ["NEE", "GPP", "Reco", "NPP"]
  
parameters_contributed:
  - "NPP"
  - "Phi_q"  # derived from SIF
  
validation:
  independent_source: "MODIS MOD17"
  correlation_coefficient: 0.94
  
contributor:
  name: "Your Name"
  affiliation: "Your Institution"
  email: "your.email@institution.org"
  orcid: "0000-0000-0000-0000"
  reference: "DOI or citation if published"
```

1. Data format example:

```csv
year,month,NPP,S_ocean,G_atm,F_perma,beta,tau_soil,E_anth,Phi_q,PCSI,data_source
2025,1,58.2,null,2.38,null,0.081,27,11.2,0.071,0.78,modis
2025,2,58.4,null,2.39,null,0.081,27,11.2,0.071,0.78,modis
...
```

1. Submit via pull request to the data/contributions/ directory

---

🔀 Pull Request Process

PR Checklist

· Code follows project style guide
· Tests added/updated and passing
· Documentation updated
· CHANGELOG.md updated
· All CI checks passing
· Reviewed by at least one maintainer
· Physics changes validated against observations (if applicable)
· Parameter changes validated against Keeling Curve (if applicable)
· Performance benchmarks meet targets (if applicable)

PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactor
- [ ] Data contribution
- [ ] Parameter update

## Related Issues
Closes #XXX

## Physics Changes (if applicable)
- [ ] Equations modified
- [ ] Constants updated
- [ ] Validation against observations (r² ≥ 0.90)
- [ ] Documentation updated with equations

## Parameter Changes (if applicable)
- [ ] Weights modified
- [ ] PCA-regularized regression re-run
- [ ] Cross-validation performed
- [ ] Impact on PCSI quantified

## Data Contribution (if applicable)
- [ ] Data format validated
- [ ] Metadata complete
- [ ] Independent verification source provided
- [ ] License compatible

## Testing Performed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] 65-year Keeling Curve validation
- [ ] Performance benchmarks

## Additional Notes
Any additional information reviewers should know
```

Review Process

1. Automated Checks: CI runs tests, linting, type checking
2. Code Review: At least one maintainer reviews
3. Physics Review: For changes to core equations
4. Parameter Review: For changes to PCSI weights
5. Data Validation: For data contributions

---

🌍 Community Guidelines

Communication Channels

· GitHub Issues: Bug reports, feature requests
· GitHub Discussions: Q&A, ideas, community support
· Email: gitdeeper@gmail.com (project lead)
· ORCID: 0009-0003-8903-0029

Recognition

Contributors are recognized in:

· AUTHORS.md
· Release notes
· Academic publications (where applicable)

Research Contributions

If you use CARBONICA in your research:

1. Cite the paper: Baladi, S. (2026). CARBONICA. DOI: 10.5281/zenodo.18995446
2. Share your data/code when possible
3. Submit a case study to our repository

---

📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CARBONICA! 🌍

For questions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
EOF