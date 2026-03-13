#!/bin/bash
# CARBONICA Documentation Generator

echo "📚 CARBONICA Documentation Generator"
echo "===================================="

# Create docs directory
mkdir -p docs/api
mkdir -p docs/theory
mkdir -p docs/examples

# Generate API documentation
echo ""
echo "📄 Generating API documentation..."
cat > docs/api/README.md << API_EOF
# CARBONICA API Reference

## Main Classes

### \`CARBONICA\`
Main engine class that integrates all eight parameters.

**Methods:**
- \`__init__(data_dir="./data")\` - Initialize CARBONICA
- \`compute_pcsi(year=2025)\` - Compute PCSI for given year
- \`get_parameter(param_name, year)\` - Get parameter value
- \`update_parameter(param_name, value, year)\` - Update parameter
- \`summary()\` - Print summary

### \`PCSI\`
Planetary Carbon Saturation Index calculator.

**Methods:**
- \`compute(parameters)\` - Compute PCSI from parameters
- \`normalize(param_name, value)\` - Normalize parameter
- \`get_status(pcsi)\` - Get status description

## Modules

### \`OceanSinkModel\`
Ocean carbon sink calculations.

### \`PermafrostEngine\`
Permafrost thaw flux calculations.

### \`QuantumYieldTracker\`
Photosynthetic quantum yield tracking.

## Data Loaders

- \`KeelingLoader\` - Keeling Curve data
- \`SOCATLoader\` - Ocean pCO₂ data
- \`GCPLoader\` - Global Carbon Project data
- \`GTNPLoader\` - Permafrost data
- \`GLODAPLoader\` - Ocean chemistry data
- \`MODISLoader\` - NPP data
- \`SIFLoader\` - SIF data

## Statistics

- \`SimpleStats\` - Basic statistics
- \`MonteCarloPropagator\` - Uncertainty propagation
- \`CUSUMDetector\` - Change point detection
- \`StructuralEquationModel\` - SEM analysis
- \`PCARegression\` - PCA regression

## Visualization

- \`ParameterPlots\` - Time series plots
- \`PCSIDashboard\` - Real-time dashboard
- \`CorrelationMatrix\` - Correlation heatmap
- \`ProjectionPlot\` - SSP scenario projections

## Command Line Interface

\`\`\`bash
carbonica init           # Initialize project
carbonica download       # Download data
carbonica process        # Process data
carbonica pcsi           # Compute PCSI
carbonica serve          # Start dashboard
carbonica plot           # Generate plots
carbonica export         # Export results
carbonica validate       # Validate against observations
\`\`\`
API_EOF

# Generate theory documentation
echo ""
echo "📄 Generating theory documentation..."
cat > docs/theory/eight_parameters.md << THEORY_EOF
# The Eight CARBONICA Parameters

## 1. Net Primary Productivity (NPP)
Terrestrial photosynthetic carbon uptake.

**Equation:** NPP = Φ_q · fAPAR · LUE_max · SW_in · f(T) · f(VPD)

**Current (2025):** 58.3 ± 4.2 PgC/yr
**Critical threshold:** < 52.0 PgC/yr

## 2. Oceanic Carbon Sink Strength (S_ocean)
Air-sea CO₂ exchange.

**Equation:** F_as = k_w · K_0 · (pCO₂_atm − pCO₂_sw)

**Current (2025):** -3.08 PgC/yr
**Critical threshold:** < -1.5 PgC/yr

## 3. Atmospheric CO₂ Growth Rate (G_atm)
Net source-sink imbalance.

**Equation:** dC_atm/dt = E_anth + F_nat + F_perma − S_ocean − S_land

**Current (2025):** 2.38 ppm/yr
**Critical threshold:** ≥ 3.5 ppm/yr

## 4. Permafrost Thaw Flux (F_perma)
Frozen carbon reserve release.

**Equation:** F_perma = C_perma · k_decomp(T) · A_thaw / τ_frozen

**Current (2025):** 1.71 ± 0.4 PgC/yr
**Critical threshold:** ≥ 2.8 PgC/yr

## 5. Carbon Buffer Capacity (β)
Ocean carbonate buffer chemistry (Revelle Factor inverse).

**Equation:** β = 1/R, R = (∂ln pCO₂) / (∂ln DIC)

**Current (2025):** 0.081 (R = 12.4)
**Critical threshold:** β ≤ 0.071 (R ≥ 14.0)

## 6. Soil Carbon Residence Time (τ_soil)
Stability of terrestrial carbon reservoir.

**Equation:** τ_soil = C_pool / F_out

**Current (2025):** 27 years
**Critical threshold:** < 18 years

## 7. Anthropogenic Emission Factor (E_anth)
Direct human perturbation term.

**Current (2025):** 11.2 PgC/yr
**Critical threshold:** Net-zero by ~2050

## 8. Photosynthetic Quantum Yield (Φ_q)
Biophysical solar-to-carbon efficiency.

**Equation:** Φ_q = ΔF/Fm' (from SIF)

**Current (2025):** 0.071
**Critical threshold:** < 0.040
THEORY_EOF

# Generate examples
echo ""
echo "📄 Generating example notebooks..."
cat > docs/examples/quickstart.py << EXAMPLE_EOF
#!/usr/bin/env python3
"""
CARBONICA Quickstart Example
"""

from carbonica import CARBONICA

# Initialize
carbonica = CARBONICA(data_dir="./data")

# Compute PCSI for 2025
pcsi_2025 = carbonica.compute_pcsi(2025)
print(f"PCSI 2025: {pcsi_2025:.3f}")
print(f"Status: {carbonica.get_pcsi_status(pcsi_2025)}")

# Get individual parameters
print("\nEight Parameters (2025):")
params = carbonica.compute_current_state(2025)
for param, value in params.items():
    print(f"  {param}: {value}")

# Update a parameter
carbonica.update_parameter('NPP', 59.0, 2025)
pcsi_updated = carbonica.compute_pcsi(2025)
print(f"\nUpdated PCSI: {pcsi_updated:.3f}")

# Print summary
print(carbonica.summary())
EXAMPLE_EOF

chmod +x docs/examples/quickstart.py

echo ""
echo "✅ Documentation generated in ./docs directory"
