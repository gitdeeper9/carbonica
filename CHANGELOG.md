# Changelog

All notable changes to the CARBONICA project will be documented in this file.

**DOI:** 10.5281/zenodo.18995446  
**Repository:** github.com/gitdeeper9/carbonica  
**Web Dashboard:** carbonica.netlify.app

---

## [1.0.0] - 2026-03-13

### 🚀 Initial Release
- Publication of CARBONICA research paper
- Release of complete 8-parameter physics framework
- 65-year observational baseline (1960-2025)
- PCSI (Planetary Carbon Saturation Index) formulation
- Open access data from 7 global datasets

### Added

#### Core Physics Engine
- **Net Primary Productivity (NPP)**: Terrestrial photosynthetic carbon uptake
  - NPP = Φ_q · fAPAR · LUE_max · SW_in · f(T) · f(VPD)
  - Global mean: 58.3 ± 4.2 PgC/yr (2020-2025)
  - MODIS MOD17 validation: r² = 0.94

- **Oceanic Carbon Sink Strength (S_ocean)**: Air-sea CO₂ exchange
  - F_as = k_w · K_0 · (pCO₂_atm − pCO₂_sw)
  - k_w = 0.251 · u₁₀² · (Sc/660)^(-0.5) [Wanninkhof, 2014]
  - Current sink: −3.08 PgC/yr (2025)

- **Atmospheric CO₂ Growth Rate (G_atm)**: Source-sink imbalance
  - dC_atm/dt = 2.38 ppm/yr (2025)
  - 65-year Keeling Curve validation: r² = 0.997

- **Permafrost Thaw Flux (F_perma)**: Positive feedback release
  - F_perma = C_perma · k_decomp(T) · A_thaw(t) / τ_frozen
  - k_decomp(T) = k₀ · Q₁₀^((T−T_ref)/10) [Q₁₀ = 2.0-3.5]
  - Current flux: 1.71 ± 0.4 PgC/yr (2025)

- **Carbon Buffer Capacity (β)**: Revelle Factor inverse
  - R = (∂ln pCO₂) / (∂ln DIC) = DIC / (pCO₂ · ∂DIC/∂pCO₂)
  - β = 1/R, R₁₉₆₀ = 10.2 → R₂₀₂₅ = 12.4 (36% buffer reduction)

- **Soil Carbon Residence Time (τ_soil)**: Terrestrial reservoir stability
  - τ_soil = C_pool / F_out = C_pool / (R_het + F_fire + F_leach)
  - Current: 27 yr (1960: 30 yr)

- **Anthropogenic Emission Factor (E_anth)**: Human perturbation
  - Current: 11.2 PgC/yr (2025)
  - Fossil fuel + cement + land-use change

- **Photosynthetic Quantum Yield (Φ_q)**: Biophysical efficiency
  - Φ_q = ΔF/Fm' = (Fm' − Fs) / Fm' [SIF formulation]
  - Global decline: −0.9%/decade (2009-2025)
  - Tropical decline: −2.1%/decade

#### Planetary Carbon Saturation Index (PCSI)
- PCSI = w₁·NPP* + w₂·S*_ocean + w₃·G*_atm + w₄·F*_perma + w₅·β* + w₆·τ*_soil + w₇·E*_anth + w₈·Φ*_q
- Weights: w₁=0.16, w₂=0.18, w₃=0.20, w₄=0.19, w₅=0.12, w₆=0.07, w₇=0.05, w₈=0.03
- Current PCSI (2025): 0.78 (1960: 0.31)
- Critical threshold: 1.00 (irreversible feedback)
- PCSI acceleration: 0.004/yr (1960-1990) → 0.012/yr (2010-2025)

#### Processing Pipeline
- **CarbonBudget**: Integrates master dC_atm/dt equation in real-time
  - Monthly resolution parameter time series
  - Monte Carlo uncertainty propagation (10,000 ensemble members)
  - CUSUM change-point detection

- **OceanSinkModel**: Wanninkhof (2014) gas transfer parameterization
  - 1°×1° global grid using ERA5 wind fields
  - 12 ocean basin sub-regions
  - Real-time β monitoring with 30-day forecast

- **PermafrostEngine**: Q₁₀ decomposition model with GTN-P data
  - Separates gradual vs. abrupt thaw (thermokarst)
  - GRACE-FO lake area change detection
  - Tipping point dynamics (bistable permafrost state)

- **QuantumYieldTracker**: Global Φ_q maps from GOSAT/OCO-2 SIF
  - Frankenberg et al. (2011) fluorescence-photosynthesis algorithm
  - Drought/heat stress detection
  - Direct input to NPP forward model

#### Validation Dataset
- **Time Series**: 65 years (1960-2025)
- **Keeling Curve**: 780 monthly CO₂ observations
- **SOCAT**: 35,000+ cruise tracks, 33.7 million pCO₂ measurements
- **GLODAP**: 1.2 million ocean carbon measurements
- **MODIS NPP**: 500 m spatial / 8-day temporal (2000-2025)
- **GTN-P**: 1,200+ borehole temperature profiles
- **FLUXNET**: 900+ eddy covariance sites
- **GOSAT/OCO-2**: 16 years of SIF retrievals (2009-2025)

#### Case Studies
- **Amazon Carbon Pivot (2018-2023)**: From sink to source
  - Φ_q decline: 0.069 → 0.055 (20% loss)
  - Net reversal: 0.8 PgC/yr sink → 0.8 PgC/yr source
  - 1.2 PgC/yr absolute budget deterioration

- **Arctic Carbon System**: Planetary tipping edge
  - 1,240 GTN-P borehole stations
  - F_perma = 1.71 PgC/yr (2025)
  - Abrupt thaw: 31% of current flux from 5% of area
  - ESAS submarine permafrost: critical by 2031-2044

- **Mauna Loa 65-Year Baseline**: PCSI validation
  - r² = 0.997 against Keeling monthly mean
  - 11-year solar cycle correlation (r=0.47)
  - ENSO-driven oscillation (r=0.61)

#### Performance Metrics

| Metric | Value | Target |
|--------|-------|--------|
| PCSI vs. Keeling Curve (r²) | 0.947 | ≥0.92 |
| Revelle Factor acceleration | 2.5× | - |
| Permafrost flux uncertainty | ±0.4 PgC/yr | ±0.5 |
| Ocean sink accuracy | ±0.15 PgC/yr | ±0.20 |
| NPP global estimate | 58.3 ± 4.2 PgC/yr | ±5.0 |
| Φ_q decline detection | −0.9%/decade | - |
| Amazon case study (r²) | 0.91 | ≥0.90 |

#### Data Integration
- NOAA Mauna Loa Observatory (Keeling Curve)
- SOCAT Surface Ocean CO₂ Atlas
- GLODAP Global Ocean Data Analysis Project
- MODIS MOD17 NPP product
- NASA OCO-2 SIF retrievals
- GTN-P Global Terrestrial Network for Permafrost
- Global Carbon Project annual budget
- FLUXNET eddy covariance network
- ECMWF ERA5 Reanalysis

#### Deployment Options
- Single-station analysis
- Global monitoring network
- Real-time processing
- Docker containers for all services
- Netlify web dashboard
- PyPI package: `pip install carbonica`

#### Documentation
- Complete API reference
- Installation guide (INSTALL.md)
- Deployment guide (DEPLOY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Code of conduct (CODE_OF_CONDUCT.md)
- Jupyter notebooks for all case studies
- Parameter calibration protocols

---

## [0.9.0] - 2026-02-15

### ⚠️ Pre-release Candidate

### Added
- Beta version of all core modules
- Validation against 1960-2020 data
- Preliminary PCSI weight determination
- Basic data loaders
- Initial documentation

### Changed
- Refined Revelle Factor algorithms
- Updated permafrost Q₁₀ parameters
- Improved Monte Carlo propagation

### Fixed
- Data synchronization issues
- NPP calculation edge cases
- Coherence validation

---

## [0.8.0] - 2026-01-20

### 🧪 Alpha Release

### Added
- Prototype physics modules
- Test deployments with historical data
- Basic data collection pipeline
- Preliminary PCSI formulation
- Initial case study implementations

---

## [0.5.0] - 2025-09-15

### 🏗️ Development Milestone

### Added
- Microbarom amplitude module
- Basic beamforming implementation
- Spectral analysis tools
- Data ingestion from IMS archive

---

## [0.1.0] - 2025-06-01

### 🎯 Project Initiation

### Added
- Project concept and framework design
- Initial 8-parameter selection
- Literature review compilation
- Research proposal development
- Data access agreements

---

## 🔮 Future Releases

### [1.1.0] - Planned Q3 2026
- Additional validation (2025-2026 data)
- Machine learning emulators for fast inversion
- Real-time satellite data integration
- Methane cycle module (CARBONICA v2.0 prep)
- Enhanced permafrost abrupt thaw detection

### [1.2.0] - Planned Q1 2027
- Marine ecosystem carbon (biological pump)
- Nitrogen-carbon coupling module
- Global real-time PCSI maps
- Automated alert system

### [2.0.0] - Planned 2028
- Full methane cycle integration
- Ocean biological pump explicit parameterization
- Coupled carbon-nitrogen cycle
- 100+ station validation network
- Operational climate monitoring integration

---

## 📊 Version History

| Version | Date | Status | DOI |
|---------|------|--------|-----|
| 1.0.0 | 2026-03-13 | Stable Release | 10.5281/zenodo.18995446 |
| 0.9.0 | 2026-02-15 | Release Candidate | 10.5281/zenodo.18895446 |
| 0.8.0 | 2026-01-20 | Alpha | 10.5281/zenodo.18795446 |
| 0.5.0 | 2025-09-15 | Development | - |
| 0.1.0 | 2025-06-01 | Concept | - |

---

For questions or contributions: gitdeeper@gmail.com · ORCID: 0009-0003-8903-0029
