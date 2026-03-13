# 🌍 CARBONICA Deployment Guide v1.0.0
## Advanced Planetary Carbon Accounting & Feedback Dynamics

**DOI**: 10.5281/zenodo.18995446  
**Repository**: github.com/gitdeeper9/carbonica  
**Web**: carbonica.netlify.app

---

## 📋 Deployment Overview

This guide covers deployment options for CARBONICA across different environments.

### Deployment Architectures

| Architecture | Use Case | Resources | Data Processing |
|-------------|----------|-----------|-----------------|
| **Single Node** | Local analysis | 1 server (8GB RAM, 4 CPU) | Monthly updates |
| **Research Cluster** | Regional center | 4-8 nodes (32GB RAM, 16 CPU) | Daily updates |
| **Cloud-Based** | Global monitoring | Auto-scaling | Real-time |
| **Edge** | Field stations | Raspberry Pi 4 | Hourly updates |

---

## 🏗️ Architecture Components

```

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│  Data Loaders   │────▶│  Local Storage  │
│  (NOAA, SOCAT,  │     │  (Keeling,      │     │  (NetCDF4/HDF5) │
│   MODIS, GTN-P) │     │   SOCAT, etc.)  │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                       │
└───────────────────────┘
▼
┌─────────────────┐
│  CarbonBudget   │
│  (Core Engine)  │
└─────────────────┘
│
┌─────────────────┼─────────────────┐
▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│OceanSinkMod │   │PermafrostEn │   │QuantumYield │
│ (S_ocean,   │   │ (F_perma,   │   │ (Φ_q, NPP)  │
│  β)         │   │  τ_soil)    │   │             │
└─────────────┘   └─────────────┘   └─────────────┘
│                 │                 │
└─────────────────┼─────────────────┘
▼
┌─────────────────┐
│  PCSI Composite │
│  (0-1)          │
└─────────────────┘
│
┌─────────────────┼─────────────────┐
▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Reports   │   │  Dashboard  │   │  API/Cloud  │
│ (PDF/CSV)   │   │  (Netlify)  │   │  (Optional) │
└─────────────┘   └─────────────┘   └─────────────┘

```

---

## 🔧 Local Deployment (Single Node)

### 1. Hardware Requirements

```yaml
Minimum Specifications:
  CPU: 4+ cores (Intel i5/AMD Ryzen 5)
  RAM: 8GB
  Storage: 100GB SSD (for raw data + processed)
  Network: Internet connection for data downloads
  
Recommended Specifications:
  CPU: 8+ cores (Intel i7/AMD Ryzen 7)
  RAM: 16GB
  Storage: 500GB SSD
  Network: 100 Mbps+
  
Data Requirements:
  - Keeling Curve: ~1 MB (65 years)
  - SOCAT: ~5 GB (35,000+ cruises)
  - MODIS NPP: ~50 GB (2000-2025)
  - GLODAP: ~2 GB
  - GTN-P: ~500 MB
  - GOSAT/OCO-2: ~20 GB
  - Total: ~80-100 GB
```

2. Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose git \
  libhdf5-dev libnetcdf-dev libopenblas-dev

# 2. Clone repository
git clone https://github.com/gitdeeper9/carbonica.git
cd carbonica

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# 4. Install Python package
pip install --upgrade pip
pip install carbonica

# Or install from source
pip install -e .[all]

# 5. Create data directories
mkdir -p data/{raw,processed,cache}
mkdir -p logs
mkdir -p output/{reports,figures}

# 6. Download sample data
python -m carbonica.cli.download_sample --output ./data/raw

# 7. Initialize database (if using PostgreSQL)
python -m carbonica.cli.init_db

# 8. Run initial processing
python -m carbonica.cli.process --year 2025 --output ./output

# 9. Verify deployment
python -m carbonica.cli.verify --all
```

3. Configuration File Example

```yaml
# config/config.yaml
project:
  name: "CARBONICA"
  version: "1.0.0"
  data_dir: "./data"
  output_dir: "./output"
  log_dir: "./logs"

data_sources:
  keeling:
    enabled: true
    source: "noaa"
    url: "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt"
    local_path: "./data/raw/keeling.csv"
    update_frequency: "monthly"
  
  socat:
    enabled: true
    version: "v2025"
    local_path: "./data/raw/socat"
    update_frequency: "yearly"
  
  modis:
    enabled: true
    product: "MOD17A2"
    version: "6.1"
    years: [2000, 2025]
    local_path: "./data/raw/modis"
  
  gtnp:
    enabled: true
    stations: 1240
    local_path: "./data/raw/gtnp"
  
  glodap:
    enabled: true
    version: "v2"
    local_path: "./data/raw/glodap"
  
  gosat:
    enabled: true
    product: "SIF"
    years: [2009, 2025]
    local_path: "./data/raw/gosat"

processing:
  carbon_budget:
    enabled: true
    resolution: "monthly"
    uncertainty_method: "monte_carlo"
    ensemble_size: 10000
    change_point_detection: true
  
  ocean_sink:
    enabled: true
    grid_resolution: 1.0  # degrees
    gas_transfer: "wanninkhof_2014"
    regions: 12  # ocean basins
  
  permafrost:
    enabled: true
    q10_mineral: 2.1
    q10_yedoma: 3.5
    abrupt_thaw: true
    grace_data: true
  
  quantum_yield:
    enabled: true
    satellite: ["gosat", "oco2"]
    algorithm: "frankenberg_2011"
    biome_stats: true

pcsi:
  weights:
    NPP: 0.16
    S_ocean: 0.18
    G_atm: 0.20
    F_perma: 0.19
    beta: 0.12
    tau_soil: 0.07
    E_anth: 0.05
    Phi_q: 0.03
  
  thresholds:
    stable: 0.55
    transitional: 0.80
    critical: 1.00
  
  output_formats: ["csv", "netcdf", "json"]

database:
  enabled: false  # Set to true for production
  type: "postgresql"
  host: "localhost"
  port: 5432
  name: "carbonica"
  user: "carbonica_user"
  password: "${DB_PASSWORD}"

api:
  enabled: false
  host: "0.0.0.0"
  port: 8000
  workers: 4
  rate_limit: 100  # requests per minute

dashboard:
  enabled: true
  host: "127.0.0.1"
  port: 5000
  debug: false
  update_interval: 3600  # seconds

alerts:
  enabled: false
  check_interval: 86400  # daily
  thresholds:
    pcsi_critical: 0.80
    revelle_acceleration: 0.07  # per year
    permaflux_acceleration: 0.12  # PgC/yr²
  
  channels:
    email:
      enabled: false
      recipients: ["user@example.com"]
    slack:
      enabled: false
      webhook: "https://hooks.slack.com/services/xxx"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/carbonica.log"
  max_size: 100  # MB
  backup_count: 5
```

---

🌐 Multi-Node Deployment (Research Cluster)

Cluster Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Master Node                  │
                    │    (Orchestration + Database)        │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   Worker 1      │     │   Worker 2      │     │   Worker 3      │
    │   (NPP + Φ_q)   │     │ (Ocean + β)     │     │ (Permafrost)    │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   MODIS Data    │     │   SOCAT Data    │     │   GTN-P Data    │
    │   2000-2025     │     │   1970-2025     │     │   1990-2025     │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

Cluster Configuration

```yaml
# config/cluster.yaml
cluster:
  name: "carbonica-cluster"
  master_node: "192.168.1.100"
  nodes:
    - id: "worker-01"
      ip: "192.168.1.101"
      role: "npp_phiq"
      cpu: 16
      ram: 32
      storage: 500
    - id: "worker-02"
      ip: "192.168.1.102"
      role: "ocean_beta"
      cpu: 16
      ram: 32
      storage: 500
    - id: "worker-03"
      ip: "192.168.1.103"
      role: "permafrost"
      cpu: 16
      ram: 32
      storage: 500
    - id: "worker-04"
      ip: "192.168.1.104"
      role: "pcsi_integration"
      cpu: 16
      ram: 64
      storage: 1000

scheduling:
  method: "round_robin"
  max_jobs_per_node: 4
  retry_failed: 3

distributed_storage:
  type: "glusterfs"
  mount_point: "/mnt/carbonica-data"
  replica_count: 2
  
database:
  type: "timescaledb"
  host: "192.168.1.100"
  port: 5432
  replication: true
  standby_nodes: ["192.168.1.101", "192.168.1.102"]
```

Deployment Script

```bash
#!/bin/bash
# deploy_cluster.sh

echo "🌍 Deploying CARBONICA on research cluster..."

MASTER_NODE="192.168.1.100"
WORKER_NODES=("192.168.1.101" "192.168.1.102" "192.168.1.103" "192.168.1.104")

# Deploy on master node
ssh user@$MASTER_NODE << 'EOF'
  cd ~/carbonica
  git pull
  pip install -e .[all]
  
  # Initialize database
  docker-compose -f docker-compose.cluster.yml up -d timescaledb
  
  # Start master services
  docker-compose -f docker-compose.cluster.yml up -d master
