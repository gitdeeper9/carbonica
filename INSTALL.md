# 🌍 CARBONICA Installation Guide v1.0.0
## Advanced Planetary Carbon Accounting & Feedback Dynamics

**DOI**: 10.5281/zenodo.18995446  
**Repository**: github.com/gitdeeper9/carbonica  
**Web**: carbonica.netlify.app

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, macOS 12+, Windows 10/11 (WSL2)
- **RAM**: 8 GB
- **Storage**: 100 GB free space (for data)
- **Python**: 3.9 - 3.11
- **CPU**: 4+ cores

### Recommended Requirements
- **RAM**: 16+ GB
- **Storage**: 500+ GB SSD
- **CPU**: 8+ cores
- **Python**: 3.10
- **GPU**: CUDA-compatible (optional, for ML projections)

### Data Requirements
- **Internet connection** for downloading datasets
- **Total data size**: ~80-100 GB
- **Datasets**:
  - Keeling Curve: ~1 MB (NOAA/Scripps)
  - SOCAT: ~5 GB (35,000+ cruises)
  - MODIS NPP: ~50 GB (2000-2025)
  - GLODAP: ~2 GB
  - GTN-P: ~500 MB
  - GOSAT/OCO-2: ~20 GB

---

## 🚀 Quick Installation (5 minutes)

### 1. Install via pip (Recommended)

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install CARBONICA
pip install --upgrade pip
pip install carbonica

# Verify installation
python -c "import carbonica; print(carbonica.__version__)"
# Should output: 1.0.0
```

2. Quick Test

```bash
# Download sample data
carbonica-download-sample --output ./sample_data

# Process sample data
carbonica-process --input ./sample_data --output ./results

# View PCSI results
carbonica-view --input ./results/pcsi.csv
```

3. Start Web Dashboard

```bash
# Start local server
carbonica-serve --host 127.0.0.1 --port 5000

# Open browser: http://127.0.0.1:5000
```

---

📦 Installation Methods

Method A: pip Install (Production)

```bash
# Basic installation
pip install carbonica

# With all optional dependencies
pip install carbonica[all]

# With specific extras
pip install carbonica[ml]      # Machine learning for projections
pip install carbonica[gpu]     # GPU acceleration
pip install carbonica[docs]    # Documentation tools
pip install carbonica[dev]     # Development tools
pip install carbonica[web]     # Web dashboard
```

Method B: From Source (Development)

```bash
# Clone repository
git clone https://github.com/gitdeeper9/carbonica.git
cd carbonica

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

Method C: Docker (Containerized)

```bash
# Pull from Docker Hub
docker pull gitdeeper9/carbonica:latest

# Run container
docker run -d \
  --name carbonica \
  -p 5000:5000 \
  -p 8000:8000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/config:/app/config \
  gitdeeper9/carbonica:latest

# Or build locally
docker build -t carbonica:latest .
docker-compose up -d
```

Method D: Conda (Alternative)

```bash
# Create conda environment
conda create -n carbonica python=3.10
conda activate carbonica

# Install from conda-forge (once available)
conda install -c conda-forge carbonica

# Or install via pip in conda
pip install carbonica
```

---

🔧 Detailed Installation Steps

Step 1: System Dependencies

Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y \
  python3-pip \
  python3-dev \
  python3-venv \
  git \
  build-essential \
  libhdf5-dev \
  libnetcdf-dev \
  libopenblas-dev \
  libfftw3-dev \
  curl \
  wget
```

macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install \
  python@3.10 \
  git \
  hdf5 \
  netcdf \
  openblas \
  fftw
```

Windows (WSL2)

```powershell
# In PowerShell (Admin)
wsl --install -d Ubuntu

# Then follow Ubuntu instructions in WSL terminal
```

Step 2: Python Environment

```bash
# Create virtual environment
python3 -m venv ~/venv/carbonica
source ~/venv/carbonica/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

Step 3: Install CARBONICA

```bash
# Core installation
pip install carbonica

# Verify installation
python -c "
import carbonica
print(f'CARBONICA version: {carbonica.__version__}')
print(f'Core modules: {carbonica.__all__}')
"
```

Step 4: Configure Environment

```bash
# Create configuration directory
mkdir -p ~/.carbonica

# Download example configuration
curl -o ~/.carbonica/config.yaml \
  https://raw.githubusercontent.com/gitdeeper9/carbonica/main/config/config.yaml

# Edit configuration
nano ~/.carbonica/config.yaml
```

Step 5: Download Data

```bash
# Create data directory
mkdir -p ~/carbonica_data

# Download Keeling Curve (small, fast)
carbonica-download --source keeling --output ~/carbonica_data

# Download other datasets (may take time)
carbonica-download --all --output ~/carbonica_data

# Or download specific years
carbonica-download --source modis --years 2020-2025 --output ~/carbonica_data
```

Step 6: Test Installation

```bash
# Run diagnostic
carbonica-diagnostic --all

# Expected output:
# ✅ Python version: 3.10.x
# ✅ CARBONICA version: 1.0.0
# ✅ Core modules: installed
# ✅ NumPy: 1.24.x
# ✅ SciPy: 1.10.x
# ✅ Pandas: 2.0.x
# ✅ Xarray: 2023.4.x
# ✅ Database: connected (if configured)
# ✅ Data directories: found
```

---

🐳 Docker Installation Details

Docker Compose (Full Stack)

```bash
# Clone repository
git clone https://github.com/gitdeeper9/carbonica.git
cd carbonica

# Set environment variables
export DB_PASSWORD=$(openssl rand -base64 32)
export GRAFANA_PASSWORD=admin

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Access services:
# - Web Dashboard: http://localhost:5000
# - API: http://localhost:8000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9091
```

Docker Commands

```bash
# Build image
docker build -t carbonica:latest .

# Run with custom config
docker run -d \
  --name carbonica \
  -p 5000:5000 \
  -v $(pwd)/custom_config:/app/config \
  -v $(pwd)/custom_data:/data \
  carbonica:latest

# Execute commands in container
docker exec -it carbonica carbonica-process --year 2025

# Export results
docker cp carbonica:/app/output ./results
```

---

🌐 Web Dashboard Installation

Local Development

```bash
# Install with web extras
pip install carbonica[web]

# Start development server
carbonica-serve --debug --host 127.0.0.1 --port 5000
```

Production with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Start production server
gunicorn -w 4 -b 0.0.0.0:8000 carbonica.web.app:app
```

Netlify Deployment (Static Dashboard)

```bash
# Build static files
carbonica-build-static --output ./build

# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build --site=carbonica
```

---

📊 Database Setup

PostgreSQL/TimescaleDB

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create database
sudo -u postgres psql -c "CREATE DATABASE carbonica;"
sudo -u postgres psql -c "CREATE USER carbonica_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE carbonica TO carbonica_user;"

# Install TimescaleDB extension
sudo apt install -y timescaledb-postgresql-15
```

Initialize Database Schema

```bash
# Run migrations
carbonica-db migrate

# Verify connection
carbonica-db test
```

---

📈 Performance Optimization

Parallel Processing

```bash
# Set number of cores
export CARBONICA_NUM_CORES=8

# Enable parallel processing in config
carbonica-config set processing.parallel true
carbonica-config set processing.num_workers 8
```

GPU Acceleration

```bash
# Install with GPU support
pip install carbonica[gpu]

# Enable GPU in config
carbonica-config set ml.use_gpu true
carbonica-config set ml.gpu_id 0
```

Caching

```bash
# Enable Redis caching
carbonica-config set cache.enabled true
carbonica-config set cache.host localhost
carbonica-config set cache.port 6379
```

---

✅ Installation Verification

Complete Verification Script

```bash
#!/bin/bash
# verify_installation.sh

echo "🔍 Verifying CARBONICA installation..."

# Check Python
echo "Checking Python..."
python --version || exit 1

# Check package
echo "Checking CARBONICA package..."
pip show carbonica || exit 1

# Check version
echo "Checking version..."
python -c "import carbonica; print(f'Version: {carbonica.__version__}')"

# Check imports
echo "Checking module imports..."
python -c "
import carbonica.physics
import carbonica.data
import carbonica.visualization
print('✅ All modules imported successfully')
"

# Check data directories
echo "Checking data directories..."
[ -d "$HOME/carbonica_data" ] || mkdir -p "$HOME/carbonica_data"

# Run test processing
echo "Running test processing..."
carbonica-process --test --output ./test_output

# Check PCSI calculation
echo "Testing PCSI calculation..."
carbonica-pcsi --test

# Check API (if running)
if curl -s http://localhost:5000/health > /dev/null; then
  echo "✅ API is running"
else
  echo "⚠️ API not running (optional)"
fi

echo "✅ Installation verification complete!"
```

---

🚨 Troubleshooting

Common Issues

Issue: "Module not found" errors

```bash
# Solution: Reinstall with all dependencies
pip uninstall carbonica -y
pip install carbonica[all]
```

Issue: Data download fails

```bash
# Solution: Use mirror or manual download
carbonica-download --source keeling --url https://mirror.example.com/co2_mm_mlo.txt
```

Issue: Out of memory

```bash
# Solution: Reduce chunk size
carbonica-config set processing.chunk_size 1000
carbonica-config set processing.memory_limit 4096  # MB
```

Issue: Slow processing

```bash
# Solution: Enable parallel processing
carbonica-config set processing.parallel true
carbonica-config set processing.num_workers $(nproc)
```

Logs

```bash
# Check logs
tail -f ~/.carbonica/logs/carbonica.log

# Increase log level for debugging
carbonica-config set logging.level DEBUG
```

---

📚 Additional Resources

· Documentation: https://carbonica.netlify.app/docs
· API Reference: https://carbonica.netlify.app/api
· GitHub: https://github.com/gitdeeper9/carbonica
· PyPI: https://pypi.org/project/carbonica/
· Docker Hub: https://hub.docker.com/r/gitdeeper9/carbonica
· DOI: 10.5281/zenodo.18995446

---

📞 Support

For installation assistance:

· Email: gitdeeper@gmail.com
· GitHub Issues: https://github.com/gitdeeper9/carbonica/issues
· ORCID: 0009-0003-8903-0029

---

Version: 1.0.0
Last Updated: 2026-03-13
