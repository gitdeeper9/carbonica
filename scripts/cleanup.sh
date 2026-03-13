#!/bin/bash
# CARBONICA Cleanup Script

echo "🧹 CARBONICA Cleanup"
echo "===================="

# Ask for confirmation
read -p "This will remove all generated files. Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled"
    exit 1
fi

# Remove Python cache
echo "🗑️  Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Remove test cache
echo "🗑️  Removing test cache..."
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov
rm -rf *.egg-info

# Remove build artifacts
echo "🗑️  Removing build artifacts..."
rm -rf build
rm -rf dist
rm -rf *.egg-info

# Remove logs
echo "🗑️  Removing logs..."
rm -rf logs/*

# Remove results (optional)
read -p "Remove results directory? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing results..."
    rm -rf results/*
fi

# Remove data (optional)
read -p "Remove downloaded data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing data..."
    rm -rf data/raw/*
    rm -rf data/processed/*
fi

echo ""
echo "✅ Cleanup complete!"
