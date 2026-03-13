#!/usr/bin/env python3
# CARBONICA Setup Script
# Advanced Planetary Carbon Accounting & Feedback Dynamics
# Version: 1.0.0 | DOI: 10.5281/zenodo.18995446

import os
import sys
from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read version
version = "1.0.0"

setup(
    name="carbonica",
    version=version,
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="CARBONICA: Advanced Planetary Carbon Accounting & Feedback Dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitdeeper9/carbonica",
    project_urls={
        "Documentation": "https://carbonica.netlify.app/docs",
        "Source": "https://github.com/gitdeeper9/carbonica",
        "Bug Reports": "https://github.com/gitdeeper9/carbonica/issues",
        "Discussion": "https://github.com/gitdeeper9/carbonica/discussions",
        "DOI": "https://doi.org/10.5281/zenodo.18995446",
        "Web Dashboard": "https://carbonica.netlify.app",
    },
    packages=find_packages(include=["carbonica", "carbonica.*"]),
    install_requires=requirements,
    python_requires=">=3.9, <3.12",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="carbon-cycle climate-science earth-system biogeochemistry permafrost ocean-carbon",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "carbonica=carbonica.cli.main:cli",
            "carbonica-init=carbonica.cli.init:main",
            "carbonica-download=carbonica.cli.download:main",
            "carbonica-process=carbonica.cli.process:main",
            "carbonica-pcsi=carbonica.cli.pcsi:main",
            "carbonica-serve=carbonica.cli.serve:main",
            "carbonica-diagnostic=carbonica.cli.diagnostic:main",
            "carbonica-download-sample=carbonica.cli.download_sample:main",
            "carbonica-validate=carbonica.cli.validate:main",
            "carbonica-report=carbonica.cli.report:main",
            "carbonica-plot=carbonica.cli.plot:main",
            "carbonica-config=carbonica.cli.config:main",
            "carbonica-db=carbonica.cli.database:main",
        ],
        "carbonica.physics": [
            "npp = carbonica.physics.npp:NetPrimaryProductivity",
            "ocean_sink = carbonica.physics.ocean_sink:OceanCarbonSink",
            "revelle = carbonica.physics.revelle:RevelleFactor",
            "permafrost = carbonica.physics.permafrost:PermafrostThawFlux",
            "soil = carbonica.physics.soil:SoilCarbonResidence",
            "quantum_yield = carbonica.physics.quantum_yield:PhotosyntheticQuantumYield",
            "pcsi = carbonica.physics.pcsi:PlanetaryCarbonSaturationIndex",
        ],
        "carbonica.data": [
            "keeling = carbonica.data.loaders.keeling:KeelingLoader",
            "socat = carbonica.data.loaders.socat:SOCATLoader",
            "modis = carbonica.data.loaders.modis:MODISLoader",
            "gtnp = carbonica.data.loaders.gtnp:GTNPLoader",
            "glodap = carbonica.data.loaders.glodap:GLODAPLoader",
            "gosat = carbonica.data.loaders.gosat:GOSATLoader",
            "oco2 = carbonica.data.loaders.oco2:OCO2Loader",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xdist>=3.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "ml": [
            "tensorflow>=2.12.0",
            "torch>=2.0.0",
            "xgboost>=1.7.0",
            "statsmodels>=0.14.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
        "web": [
            "flask>=2.3.0",
            "dash>=2.9.0",
            "gunicorn>=20.1.0",
        ],
        "db": [
            "psycopg2-binary>=2.9.6",
            "sqlalchemy>=2.0.12",
            "redis>=4.5.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "tensorflow>=2.12.0",
            "torch>=2.0.0",
            "sphinx>=7.0.0",
            "flask>=2.3.0",
            "dash>=2.9.0",
            "psycopg2-binary>=2.9.6",
            "sqlalchemy>=2.0.12",
            "redis>=4.5.0",
        ],
    },
    platforms=["any"],
    license="MIT",
)

print("✅ CARBONICA setup complete!")
print(f"📦 Version: {version}")
print("📚 Documentation: https://carbonica.netlify.app/docs")
print("🐍 Python: >=3.9, <3.12")
