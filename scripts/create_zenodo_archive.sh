#!/bin/bash
# CARBONICA Zenodo Archive Creator

echo "📦 CARBONICA Zenodo Archive Creator"
echo "==================================="

VERSION="1.0.0"
DATE=$(date +%Y%m%d)
ARCHIVE_NAME="carbonica-${VERSION}-${DATE}.zip"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "📁 Creating temporary directory: $TEMP_DIR"

# Copy files to temporary directory
echo "📋 Copying files..."
cp -r carbonica $TEMP_DIR/
cp -r tests $TEMP_DIR/
cp -r scripts $TEMP_DIR/
cp -r docs $TEMP_DIR/
cp -r notebooks $TEMP_DIR/
cp -r config $TEMP_DIR/

# Copy documentation files
cp README.md $TEMP_DIR/
cp LICENSE $TEMP_DIR/
cp CITATION.cff $TEMP_DIR/
cp CHANGELOG.md $TEMP_DIR/
cp CONTRIBUTING.md $TEMP_DIR/
cp CODE_OF_CONDUCT.md $TEMP_DIR/
cp AUTHORS.md $TEMP_DIR/
cp COMPLETION.md $TEMP_DIR/
cp COMPLETION_CERTIFICATE.txt $TEMP_DIR/

# Copy configuration files
cp requirements.txt $TEMP_DIR/
cp requirements-dev.txt $TEMP_DIR/
cp setup.py $TEMP_DIR/
cp setup.cfg $TEMP_DIR/
cp pyproject.toml $TEMP_DIR/
cp MANIFEST.in $TEMP_DIR/
cp .gitignore $TEMP_DIR/
cp .dockerignore $TEMP_DIR/
cp Dockerfile $TEMP_DIR/
cp docker-compose.yml $TEMP_DIR/
cp .env.example $TEMP_DIR/

# Copy CI/CD files
cp .gitlab-ci.yml $TEMP_DIR/ 2>/dev/null || echo "⚠️  .gitlab-ci.yml not found"
cp .pre-commit-config.yaml $TEMP_DIR/ 2>/dev/null || echo "⚠️  .pre-commit-config.yaml not found"
cp .readthedocs.yaml $TEMP_DIR/ 2>/dev/null || echo "⚠️  .readthedocs.yaml not found"
cp netlify.toml $TEMP_DIR/ 2>/dev/null || echo "⚠️  netlify.toml not found"

# Create metadata file
echo "📄 Creating metadata..."
cat > $TEMP_DIR/zenodo.json << ZENODO_EOF
{
    "title": "CARBONICA: Advanced Planetary Carbon Accounting \u0026 Feedback Dynamics",
    "version": "${VERSION}",
    "upload_type": "software",
    "description": "A physically rigorous eight-parameter framework for real-time quantification of global carbon cycle dynamics, natural sink capacity, and the critical threshold at which Earth's self-regulating biogeochemical systems approach saturation.",
    "creators": [
        {
            "name": "Baladi, Samir",
            "affiliation": "Ronin Institute / Rite of Renaissance",
            "orcid": "0009-0003-8903-0029"
        }
    ],
    "license": "MIT",
    "keywords": [
        "carbon cycle",
        "climate science",
        "earth system",
        "biogeochemistry",
        "permafrost",
        "ocean carbon",
        "revelle factor",
        "photosynthesis",
        "carbon budget",
        "planetary boundaries"
    ],
    "access_right": "open",
    "communities": [
        {"identifier": "climate"},
        {"identifier": "earth-system-science"}
    ]
}
ZENODO_EOF

# Create archive
echo "🗜️  Creating archive: $ARCHIVE_NAME"
cd $TEMP_DIR
zip -r ../$ARCHIVE_NAME . > /dev/null
cd ..

# Move archive to current directory
mv $TEMP_DIR/../$ARCHIVE_NAME ./

# Clean up
rm -rf $TEMP_DIR

echo ""
echo "✅ Archive created: $ARCHIVE_NAME"
echo "📏 Size: $(du -h $ARCHIVE_NAME | cut -f1)"
echo ""
echo "Next steps:"
echo "  1. Upload to Zenodo: https://zenodo.org/deposit"
echo "  2. DOI: 10.5281/zenodo.18995446"
