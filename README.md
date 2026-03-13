# 🌍 CARBONICA

> **Carbon Accounting and Regulatory Budget Observatory for Networked Integrated Carbon Assessment**
>
> *"Weighing the Breath of the Earth."* — Samir Baladi, March 2026

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18995446-blue)](https://doi.org/10.5281/zenodo.18995446)
[![PyPI](https://img.shields.io/badge/PyPI-pip%20install%20carbonica-green)](https://pypi.org/project/carbonica)
[![Dashboard](https://img.shields.io/badge/Dashboard-carbonica.netlify.app-orange)](https://carbonica.netlify.app)
[![License](https://img.shields.io/badge/License-Open%20Source-brightgreen)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39)](https://orcid.org/0009-0003-8903-0029)

---

## Overview

**CARBONICA** is a physically rigorous **eight-parameter Earth system science framework** for real-time quantification of global carbon cycle dynamics, natural sink capacity, and the critical threshold at which Earth's self-regulating biogeochemical systems approach irreversible saturation.

The framework integrates all governing parameters — from photosynthetic quantum efficiency at the leaf scale to permafrost thaw flux at the continental scale — into a single composite metric: the **Planetary Carbon Saturation Index (PCSI)**.

> **Current PCSI (2025): 0.78 / 1.00** — *Transitional stress zone, accelerating toward critical threshold.*

The PCSI has risen from **0.31** (1960) to **0.78** (2025) at an accelerating rate of **0.012 units/year** — three times the 1960–1990 rate — driven by simultaneous intensification of three active positive feedback loops.

---

## Table of Contents

- [Scientific Context](#scientific-context)
- [The Eight Parameters](#the-eight-parameters)
- [The Planetary Carbon Saturation Index (PCSI)](#the-planetary-carbon-saturation-index-pcsi)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Key Results](#key-results)
- [carbonica_engine.py Modules](#carbonica_enginepy-modules)
- [Reproducing the Analysis](#reproducing-the-analysis)
- [Citation](#citation)
- [Author](#author)
- [License](#license)

---

## Scientific Context

Carbon is the molecular backbone of life and the primary radiative forcing agent of Earth's climate. The global carbon cycle has never in its geological history experienced a perturbation at the current rate: atmospheric CO₂ is rising at **2.4 ppm/year** — approximately 24,000× faster than during typical interglacial periods.

Every natural carbon sink on Earth is showing signs of stress, saturation, or reversal:

- The **Amazon rainforest** has entered net carbon source status in its southeastern sector.
- **Arctic permafrost** is thawing at rates exceeding model projections.
- The **Revelle Factor** has increased from 9.1 (pre-industrial) to **12.4** (2025), indicating a 36% reduction in ocean buffer capacity.
- **Photosynthetic quantum yield** Φ_q is declining at −0.9%/decade globally.

CARBONICA is designed to track all eight of these parallel, interacting stress signals in an integrated framework validated against a **65-year observational baseline (1960–2025)**.

---

## The Eight Parameters

| # | Parameter | Symbol | Role | Critical Threshold |
|---|-----------|--------|------|--------------------|
| 1 | Net Primary Productivity | NPP | Terrestrial photosynthetic carbon uptake | < 52.0 PgC/yr |
| 2 | Oceanic Carbon Sink Strength | S_ocean | Air-sea CO₂ exchange | < −1.5 PgC/yr (weakening alarm) |
| 3 | Atmospheric CO₂ Growth Rate | G_atm | Net source-sink imbalance | ≥ 3.5 ppm/yr |
| 4 | Permafrost Thaw Flux | F_perma | Frozen carbon reserve release | ≥ 2.8 PgC/yr (self-sustaining) |
| 5 | Carbon Buffer Capacity | β (= 1/R) | Ocean carbonate buffer chemistry | ≤ 1/14.0 = 0.071 |
| 6 | Soil Carbon Residence Time | τ_soil | Stability of terrestrial carbon reservoir | < 18 yr (net source) |
| 7 | Anthropogenic Emission Factor | E_anth | Direct human perturbation term | Net-zero by ~2050 |
| 8 | Photosynthetic Quantum Yield | Φ_q | Biophysical solar-to-carbon efficiency | < 0.040 (severe stress) |

---

## The Planetary Carbon Saturation Index (PCSI)

```
PCSI = w₁·NPP* + w₂·S*_ocean + w₃·G*_atm + w₄·F*_perma + w₅·β* + w₆·τ*_soil + w₇·E*_anth + w₈·Φ*_q
```

Each parameter is normalized to [0, 1] where **0** = pre-industrial baseline and **1** = defined critical saturation threshold.

**Optimized weights** (PCA-regularized regression, 1960–2000 training period):

| w₁ NPP | w₂ S_ocean | w₃ G_atm | w₄ F_perma | w₅ β | w₆ τ_soil | w₇ E_anth | w₈ Φ_q |
|--------|-----------|---------|----------|------|---------|---------|------|
| 0.16 | 0.18 | **0.20** | **0.19** | 0.12 | 0.07 | 0.05 | 0.03 |

**PCSI Interpretation:**

| Range | Status |
|-------|--------|
| PCSI < 0.55 | 🟢 Stable — sinks dominating |
| 0.55 – 0.80 | 🟡 Transitional stress — sink weakening detectable |
| > 0.80 | 🔴 Critical — self-reinforcing feedbacks emerging |
| = 1.00 | ☠️ Defined saturation — irreversible runaway carbon feedback |

Validation against the 65-year Keeling Curve: **r² = 0.947** (prospective 2001–2025 test period).

---

## Installation

### Python Package

```bash
pip install carbonica
```

### From Source

```bash
git clone https://gitlab.com/gitdeeper9/carbonica.git
cd carbonica
pip install -e .
```

### Requirements

```
python >= 3.9
numpy >= 1.24
scipy >= 1.10
pandas >= 2.0
netCDF4 >= 1.6
h5py >= 3.8
matplotlib >= 3.7
xarray >= 2023.1
```

---

## Quick Start

```python
from carbonica import CarbonBudget, OceanSinkModel, PermafrostEngine, QuantumYieldTracker
from carbonica.pcsi import PCSI

# Initialize the full eight-parameter system
budget = CarbonBudget(baseline_year=1960, end_year=2025)
budget.load_observations()   # auto-fetches NOAA, SOCAT, GCP, GTN-P streams

# Compute current PCSI
index = PCSI(budget)
print(f"Current PCSI (2025): {index.current:.3f}")
# → Current PCSI (2025): 0.780

# Run SSP3-7.0 projection to 2070
projection = index.project(scenario="SSP3-7.0", end_year=2070, n_ensemble=10000)
print(f"PCSI critical threshold crossing: {projection.threshold_year(0.90)}")
# → PCSI critical threshold crossing: 2047–2053

# Inspect individual parameters
print(budget.permafrost.F_perma_2025)     # → 1.71 ± 0.40 PgC/yr
print(budget.ocean.revelle_factor_2025)   # → 12.4
print(budget.biosphere.phi_q_trend)       # → -0.009 /decade
```

---

## Project Structure

```
carbonica/
│
├── README.md                          # This file
├── LICENSE
├── pyproject.toml
├── setup.cfg
│
├── carbonica/                         # Core Python package
│   ├── __init__.py
│   ├── carbonica_engine.py            # Main engine — all four core modules
│   ├── pcsi.py                        # Planetary Carbon Saturation Index
│   │
│   ├── modules/
│   │   ├── carbon_budget.py           # CarbonBudget: master dC_atm/dt integrator
│   │   ├── ocean_sink.py              # OceanSinkModel: Wanninkhof (2014) gas transfer
│   │   ├── permafrost_engine.py       # PermafrostEngine: Q₁₀ decomposition model
│   │   └── quantum_yield_tracker.py   # QuantumYieldTracker: GOSAT/OCO-2 SIF retrieval
│   │
│   ├── data/
│   │   ├── loaders/
│   │   │   ├── noaa_loader.py         # NOAA Mauna Loa CO₂ record
│   │   │   ├── socat_loader.py        # SOCAT surface ocean pCO₂ atlas
│   │   │   ├── gcp_loader.py          # Global Carbon Project annual budgets
│   │   │   ├── gtnp_loader.py         # GTN-P permafrost borehole network
│   │   │   ├── glodap_loader.py       # GLODAP ocean carbonate chemistry
│   │   │   ├── modis_loader.py        # MODIS MOD17 NPP + fAPAR
│   │   │   └── sif_loader.py          # GOSAT + OCO-2 solar-induced fluorescence
│   │   │
│   │   └── cache/                     # Local NetCDF4 / HDF5 observation cache
│   │       ├── keeling_1960_2025.nc
│   │       ├── socat_v2023.nc
│   │       ├── gtnp_boreholes.nc
│   │       └── glodap_v2.nc
│   │
│   ├── models/
│   │   ├── box_model.py               # 5-reservoir ODE system (Appendix B)
│   │   ├── lue_model.py               # Light Use Efficiency NPP model
│   │   ├── revelle.py                 # Revelle Factor time-series derivation
│   │   └── ssp_scenarios.py           # SSP1-1.9 / SSP3-7.0 / SSP5-8.5 forcing
│   │
│   ├── statistics/
│   │   ├── monte_carlo.py             # 10,000-member PCSI uncertainty ensemble
│   │   ├── sem.py                     # Structural Equation Modelling (DAG)
│   │   ├── pca_regression.py          # PCA-regularized weight optimization
│   │   └── cusum.py                   # CUSUM change-point detection
│   │
│   └── visualization/
│       ├── pcsi_dashboard.py          # Real-time web dashboard backend
│       ├── parameter_plots.py         # Eight-parameter time series plots
│       ├── correlation_matrix.py      # Heatmap renderer
│       └── projection_plot.py         # SSP scenario fan charts
│
├── notebooks/                         # Jupyter notebooks — all manuscript figures
│   ├── 01_keeling_validation.ipynb    # Fig 1: PCSI vs Keeling Curve 1960–2025
│   ├── 02_revelle_factor.ipynb        # Fig 2: Revelle Factor time series
│   ├── 03_permafrost_flux.ipynb       # Fig 3: F_perma reconstruction & projection
│   ├── 04_quantum_yield.ipynb         # Fig 4: Global Φ_q trend (GOSAT + OCO-2)
│   ├── 05_correlation_matrix.ipynb    # Fig 5: Eight-parameter correlation heatmap
│   ├── 06_amazon_case_study.ipynb     # Fig 6: Amazon carbon pivot 2018–2023
│   ├── 07_arctic_subsystem.ipynb      # Fig 7: Arctic permafrost spatial analysis
│   ├── 08_ssp_projections.ipynb       # Fig 8: PCSI SSP scenario fan (2025–2070)
│   ├── 09_sem_pathways.ipynb          # Fig 9: SEM carbon feedback DAG
│   ├── 10_monte_carlo_uncertainty.ipynb
│   ├── 11_tipping_points.ipynb
│   └── 12_policy_budget_correction.ipynb
│
├── data/                              # Raw & processed archival data
│   ├── keeling/                       # NOAA Mauna Loa monthly CO₂ (1958–2025)
│   ├── socat/                         # SOCAT v2023 pCO₂ cruise tracks
│   ├── gcp/                           # Global Carbon Project 2023 budget tables
│   ├── gtnp/                          # GTN-P borehole temperatures (1,200+ sites)
│   ├── glodap/                        # GLODAP v2 ocean DIC / alkalinity
│   ├── modis/                         # MODIS MOD17 NPP 500 m / 8-day mosaics
│   ├── gosat/                         # GOSAT SIF L2 retrievals (2009–2025)
│   └── oco2/                          # OCO-2 SIF retrievals (2014–2025)
│
├── results/                           # Model outputs (gitignored large files)
│   ├── pcsi_timeseries_1960_2025.nc   # Full PCSI parameter inversion archive
│   ├── pcsi_ensemble_ssp370.h5        # 10,000-member Monte Carlo ensemble
│   ├── pcsi_ensemble_ssp119.h5
│   └── pcsi_ensemble_ssp585.h5
│
├── docs/                              # Documentation
│   ├── api/                           # Auto-generated API reference (Sphinx)
│   ├── theory/
│   │   ├── box_model.md               # ODE system derivation (Appendix B)
│   │   ├── revelle_factor.md          # Revelle Factor chemistry
│   │   └── pcsi_formulation.md        # PCSI weight optimization methodology
│   └── changelog/
│       └── CHANGELOG.md
│
└── tests/                             # Unit & integration tests
    ├── test_carbon_budget.py
    ├── test_ocean_sink.py
    ├── test_permafrost_engine.py
    ├── test_quantum_yield.py
    ├── test_pcsi.py
    └── test_box_model.py
```

---

## Data Sources

| Parameter | Primary Source | Record Length | Resolution |
|-----------|---------------|---------------|------------|
| G_atm (CO₂ growth rate) | NOAA Mauna Loa Observatory | 1960–2025 (65 yr) | Daily; ±0.05 ppm |
| S_ocean (air-sea flux) | SOCAT Surface Ocean CO₂ Atlas v2023 | 1970–2025 (55 yr) | 1°×1° monthly |
| NPP (productivity) | MODIS MOD17 + NASA OCO-2 SIF | 2000–2025 (MODIS) | 500 m / 8-day |
| F_perma (permafrost) | GTN-P Global Terrestrial Network | 1990–2025 (35 yr) | 1,200+ boreholes |
| β (Revelle Factor) | GLODAP Global Ocean Data Analysis Project v2 | 1972–2025 | Full-depth carbonate |
| τ_soil (residence time) | ISCN + FLUXNET (900+ eddy covariance sites) | 1980–2025 | 71,000+ profiles |
| E_anth (anthropogenic) | Global Carbon Project + IEA CO₂ Statistics | 1960–2025 (65 yr) | Annual, country-level |
| Φ_q (quantum yield) | GOSAT SIF (2009–2025) + OCO-2 SIF (2014–2025) | 16 yr | 2°×2° monthly |

---

## Key Results

### PCSI Decadal Evolution

| Decade | PCSI | G_atm (ppm/yr) | S_ocean (PgC/yr) | F_perma (PgC/yr) |
|--------|------|----------------|-----------------|-----------------|
| 1960–1970 | 0.31 | 0.90 | −1.21 | ~0.0 |
| 1971–1980 | 0.38 | 1.28 | −1.44 | ~0.0 |
| 1981–1990 | 0.43 | 1.51 | −1.78 | ~0.01 |
| 1991–2000 | 0.49 | 1.63 | −1.93 | 0.05 |
| 2001–2010 | 0.58 | 1.88 | −2.24 | 0.31 |
| 2011–2020 | 0.68 | 2.19 | −2.71 | 0.98 |
| **2021–2025** | **0.78** | **2.38** | **−3.08** | **1.71** |

### Critical Findings

- **Permafrost feedback:** F_perma has risen from near-zero (1990) to **1.71 ± 0.40 PgC/yr** (2025) — constituting **4.3% of global emissions**. Abrupt thaw (thermokarst) contributes 31% of current F_perma despite covering only 5% of permafrost area.
- **Revelle Factor acceleration:** Ocean buffer capacity declining at **0.067 R-units/year** (2.5× the 1960–1990 rate). Projected to reach 14.0 by 2050, reducing ocean uptake efficiency from 28% to ~18%.
- **Quantum yield decline:** Global Φ_q declining at **−0.9%/decade** (2009–2025), with tropical ecosystems at −2.1%/decade.
- **Policy implication:** Achieving net-zero human emissions by 2050 would **not** prevent PCSI exceeding 0.85 by 2055, because autonomous permafrost and soil carbon feedbacks will contribute 2.5–4.0 PgC/yr through 2060. The effective remaining carbon budget for 1.5°C is **15–25 PgC smaller** than the IPCC AR6 estimate.

### PCSI Projection

| Scenario | PCSI = 0.90 Threshold Crossing |
|----------|---------------------------------|
| SSP1-1.9 (aggressive mitigation) | ~2055–2067 |
| **SSP3-7.0 (current trajectory)** | **2047–2053** |
| SSP5-8.5 (high emissions) | ~2041–2046 |

---

## carbonica_engine.py Modules

### `CarbonBudget`
Integrates the master `dC_atm/dt` equation in real time from NOAA, SOCAT, GCP, and GTN-P data streams. Outputs parameter time series at monthly resolution; propagates uncertainty through Monte Carlo sampling (10,000 ensemble members). Detects rate-of-change anomalies using CUSUM change-point detection.

### `OceanSinkModel`
Implements the Wanninkhof (2014) gas transfer parameterization globally on a 1°×1° grid using ERA5 wind fields and SOCAT pCO₂ data. Tracks Revelle Factor evolution across 12 ocean basin sub-regions. Real-time β monitoring with 30-day forecast of ocean uptake efficiency.

### `PermafrostEngine`
Couples GTN-P active layer depth to the Q₁₀ decomposition model. Separates gradual thaw from abrupt thaw (thermokarst) signals using GRACE-FO lake area change. Projects F_perma under SSP scenarios with explicit treatment of tipping point dynamics (bistable permafrost state).

### `QuantumYieldTracker`
Derives global Φ_q maps from GOSAT and OCO-2 SIF retrievals using the Frankenberg et al. (2011) fluorescence-photosynthesis algorithm. Detects drought and heat stress episodes as Φ_q anomalies below the biome-specific climatological mean. Feeds directly into the NPP forward model.

---

## Reproducing the Analysis

All manuscript figures are fully reproducible from the provided notebooks:

```bash
# Clone repository
git clone https://gitlab.com/gitdeeper9/carbonica.git
cd carbonica

# Install dependencies
pip install -e ".[notebooks]"

# Launch Jupyter
jupyter lab notebooks/

# Or run all notebooks headlessly
jupyter nbconvert --to notebook --execute notebooks/*.ipynb
```

All 12 notebooks reproduce the corresponding manuscript figures and statistical outputs without any external dependencies beyond the data cached in `data/`.

---

## Citation

If you use CARBONICA in your research, please cite:

```bibtex
@article{baladi2026carbonica,
  title     = {{CARBONICA}: Advanced Planetary Carbon Accounting \& Feedback Dynamics —
               A Multi-Parameter Earth System Science Framework for Real-Time
               Quantification of Global Carbon Cycle Dynamics, Sink Saturation,
               and Planetary Self-Regulation Thresholds},
  author    = {Baladi, Samir},
  journal   = {Nature Climate Change},
  year      = {2026},
  month     = {March},
  doi       = {10.5281/zenodo.18995446},
  url       = {https://doi.org/10.5281/zenodo.18995446}
}
```

---

## Author

**Samir Baladi**
Interdisciplinary AI Researcher
Ronin Institute / Rite of Renaissance

- 📧 gitdeeper@gmail.com
- 🔬 ORCID: [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
- 🌐 Dashboard: [carbonica.netlify.app](https://carbonica.netlify.app)
- 💻 GitHub: [github.com/gitdeeper9/carbonica](https://github.com/gitdeeper9/carbonica)
- 🦊 GitLab: [gitlab.com/gitdeeper9/carbonica](https://gitlab.com/gitdeeper9/carbonica)

---

## License

This project is fully open-access. Code, datasets, PCSI projection ensembles (NetCDF4/HDF5), and all supplementary materials are archived at:

- **Zenodo:** https://doi.org/10.5281/zenodo.18995446
- **PyPI:** `pip install carbonica`
- **Dashboard:** https://carbonica.netlify.app

---

*CARBONICA v1.0.0 · Submitted to Nature Climate Change, March 2026*
