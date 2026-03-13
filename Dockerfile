# CARBONICA Dockerfile
# Advanced Planetary Carbon Accounting & Feedback Dynamics
# Version: 1.0.0 | DOI: 10.5281/zenodo.18995446

FROM python:3.10-slim as builder

LABEL maintainer="Samir Baladi <gitdeeper@gmail.com>"
LABEL description="CARBONICA - Advanced Planetary Carbon Accounting & Feedback Dynamics"
LABEL version="1.0.0"
LABEL doi="10.5281/zenodo.18995446"
LABEL org.opencontainers.image.source="https://github.com/gitdeeper9/carbonica"
LABEL org.opencontainers.image.licenses="MIT"

# ============================================
# Build arguments
# ============================================
ARG DEBIAN_FRONTEND=noninteractive
ARG CARBONICA_VERSION=1.0.0

# ============================================
# Install system dependencies
# ============================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    wget \
    curl \
    git \
    ca-certificates \
    libhdf5-dev \
    libnetcdf-dev \
    libopenblas-dev \
    libfftw3-dev \
    liblapack-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Create working directory
# ============================================
WORKDIR /app

# ============================================
# Install Python dependencies
# ============================================
COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn numpy scipy pandas xarray netCDF4 h5py

# ============================================
# Copy application code
# ============================================
COPY . .

# ============================================
# Install CARBONICA
# ============================================
RUN pip install -e .

# ============================================
# Create necessary directories
# ============================================
RUN mkdir -p /app/data/{raw,processed,cache} \
    && mkdir -p /app/logs \
    && mkdir -p /app/output \
    && mkdir -p /app/config \
    && mkdir -p /app/models

# ============================================
# Create non-root user
# ============================================
RUN useradd -m -u 1000 -s /bin/bash carbonica && \
    chown -R carbonica:carbonica /app

USER carbonica

# ============================================
# Environment variables
# ============================================
ENV CARBONICA_ENV=production \
    CARBONICA_VERSION=1.0.0 \
    CARBONICA_HOME=/app \
    CARBONICA_DATA_DIR=/app/data \
    CARBONICA_OUTPUT_DIR=/app/output \
    CARBONICA_LOG_DIR=/app/logs \
    CARBONICA_CONFIG_DIR=/app/config \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# ============================================
# Expose ports
# ============================================
EXPOSE 5000 8000 9090

# ============================================
# Health check
# ============================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# ============================================
# Entry point
# ============================================
ENTRYPOINT ["carbonica"]

# ============================================
# Default command
# ============================================
CMD ["serve", "--host", "0.0.0.0", "--port", "5000"]
