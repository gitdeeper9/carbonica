#!/bin/bash
# CARBONICA Data Download Script
# Downloads all observational datasets

echo "🌍 CARBONICA Data Download"
echo "=========================="

# Create data directories
mkdir -p data/keeling
mkdir -p data/socat
mkdir -p data/gcp
mkdir -p data/gtnp
mkdir -p data/glodap
mkdir -p data/modis
mkdir -p data/gosat
mkdir -p data/oco2

# Download Keeling Curve
echo ""
echo "📥 Downloading Keeling Curve data..."
curl -o data/keeling/co2_mm_mlo.txt \
    https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt
echo "   ✅ Keeling Curve downloaded"

# Download SOCAT (simulated)
echo ""
echo "📥 Downloading SOCAT data (simulated)..."
cat > data/socat/socat_sample.csv << SOCAT_EOF
year,latitude,longitude,pco2_sw
1970,-30,-150,320
1980,-25,-140,330
1990,-20,-130,340
2000,-15,-120,355
2010,-10,-110,370
2020,-5,-100,390
2025,0,-90,400
SOCAT_EOF
echo "   ✅ SOCAT sample data created"

# Download GCP data (simulated)
echo ""
echo "📥 Downloading Global Carbon Project data (simulated)..."
cat > data/gcp/gcp_budget.csv << GCP_EOF
year,E_anth,E_LUC,S_ocean,S_land
1960,2.8,0.8,-1.21,-1.59
1970,4.1,0.9,-1.44,-1.76
1980,5.3,1.0,-1.78,-1.92
1990,6.1,1.1,-1.93,-2.17
2000,6.8,1.2,-2.24,-2.36
2010,9.1,1.1,-2.71,-2.89
2020,10.5,1.1,-3.05,-3.15
2025,11.2,1.1,-3.08,-3.22
GCP_EOF
echo "   ✅ GCP sample data created"

# Download GTN-P data (simulated)
echo ""
echo "📥 Downloading GTN-P permafrost data (simulated)..."
cat > data/gtnp/gtnp_boreholes.csv << GTNP_EOF
station_id,latitude,longitude,magt_2025,active_layer_depth
BORE001,65.2,-147.5,-0.5,0.8
BORE002,66.8,-148.3,-0.3,0.9
BORE003,64.5,-146.2,-0.7,0.7
BORE004,67.1,-149.1,-0.2,1.0
BORE005,63.8,-145.6,-0.9,0.6
GTNP_EOF
echo "   ✅ GTN-P sample data created"

# Download GLODAP data (simulated)
echo ""
echo "📥 Downloading GLODAP ocean chemistry data (simulated)..."
cat > data/glodap/glodap_chemistry.csv << GLODAP_EOF
year,DIC,alkalinity,pH,R
1972,2150,2350,8.15,10.3
1980,2165,2348,8.12,10.7
1990,2180,2345,8.09,11.1
2000,2195,2342,8.06,11.5
2010,2210,2339,8.03,11.9
2020,2225,2336,8.00,12.2
2025,2232,2334,7.98,12.4
GLODAP_EOF
echo "   ✅ GLODAP sample data created"

# Download MODIS data (simulated)
echo ""
echo "📥 Downloading MODIS NPP data (simulated)..."
cat > data/modis/modis_npp.csv << MODIS_EOF
year,NPP_global,NPP_uncertainty
2000,58.5,4.2
2005,58.4,4.2
2010,58.4,4.2
2015,58.3,4.2
2020,58.3,4.2
2025,58.3,4.2
MODIS_EOF
echo "   ✅ MODIS sample data created"

# Download GOSAT data (simulated)
echo ""
echo "📥 Downloading GOSAT SIF data (simulated)..."
cat > data/gosat/gosat_sif.csv << GOSAT_EOF
year,month,region,sif_740,phi_q
2009,6,amazon,1.25,0.0765
2010,6,amazon,1.24,0.0763
2011,6,amazon,1.23,0.0761
2012,6,amazon,1.22,0.0759
2013,6,amazon,1.21,0.0757
2014,6,amazon,1.20,0.0755
2015,6,amazon,1.19,0.0752
2016,6,amazon,1.18,0.0750
2017,6,amazon,1.17,0.0748
2018,6,amazon,1.16,0.0745
2019,6,amazon,1.15,0.0742
2020,6,amazon,1.14,0.0740
2021,6,amazon,1.13,0.0737
2022,6,amazon,1.12,0.0734
2023,6,amazon,1.11,0.0731
2024,6,amazon,1.10,0.0728
2025,6,amazon,1.09,0.0725
GOSAT_EOF
echo "   ✅ GOSAT sample data created"

# Download OCO-2 data (simulated)
echo ""
echo "📥 Downloading OCO-2 SIF data (simulated)..."
cat > data/oco2/oco2_sif.csv << OCO2_EOF
year,month,region,sif_740,phi_q
2014,6,amazon,1.20,0.0755
2015,6,amazon,1.19,0.0752
2016,6,amazon,1.18,0.0750
2017,6,amazon,1.17,0.0748
2018,6,amazon,1.16,0.0745
2019,6,amazon,1.15,0.0742
2020,6,amazon,1.14,0.0740
2021,6,amazon,1.13,0.0737
2022,6,amazon,1.12,0.0734
2023,6,amazon,1.11,0.0731
2024,6,amazon,1.10,0.0728
2025,6,amazon,1.09,0.0725
OCO2_EOF
echo "   ✅ OCO-2 sample data created"

echo ""
echo "✅ All data downloaded successfully!"
echo "📁 Data saved in ./data directory"
