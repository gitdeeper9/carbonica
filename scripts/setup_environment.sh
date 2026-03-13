#!/bin/bash
# CARBONICA Environment Setup Script
# Run this script to set up the CARBONICA environment

echo "🌍 Setting up CARBONICA environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Install development requirements
echo "📦 Installing development requirements..."
pip install -r requirements-dev.txt

# Install CARBONICA in development mode
echo "📦 Installing CARBONICA..."
pip install -e .

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/keeling
mkdir -p data/socat
mkdir -p data/gcp
mkdir -p data/gtnp
mkdir -p data/glodap
mkdir -p data/modis
mkdir -p data/gosat
mkdir -p data/oco2
mkdir -p data/raw
mkdir -p data/processed
mkdir -p results
mkdir -p logs
mkdir -p config

# Create default config
echo "⚙️  Creating default configuration..."
cat > config/carbonica.json << CONFIG_EOF
{
    "version": "1.0.0",
    "doi": "10.5281/zenodo.18995446",
    "data_dir": "./data",
    "results_dir": "./results",
    "log_dir": "./logs",
    "created": "$(date -Iseconds)"
}
CONFIG_EOF

# Download sample data
echo "📥 Downloading sample data..."
carbonica-download-sample

echo ""
echo "✅ CARBONICA environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run tests: pytest tests/"
echo "  3. Start dashboard: carbonica serve"
