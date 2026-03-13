#!/bin/bash
# CARBONICA Test Runner Script

echo "🧪 CARBONICA Test Runner"
echo "========================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Run unit tests
echo ""
echo "📊 Running unit tests..."
pytest tests/unit/ -v --tb=short

# Run integration tests
echo ""
echo "📊 Running integration tests..."
pytest tests/integration/ -v --tb=short

# Run validation tests
echo ""
echo "📊 Running validation tests..."
pytest tests/validation/ -v --tb=short

# Run with coverage
echo ""
echo "📊 Running tests with coverage..."
pytest --cov=carbonica --cov-report=term --cov-report=html tests/

echo ""
echo "✅ All tests completed!"
echo "📁 Coverage report saved to htmlcov/index.html"
