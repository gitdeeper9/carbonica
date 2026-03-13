#!/bin/bash
# CARBONICA Netlify Deployment Script

echo "🌐 CARBONICA Netlify Deployment"
echo "==============================="

# Check if netlify-cli is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Installing netlify-cli..."
    npm install -g netlify-cli
fi

# Build dashboard
echo ""
echo "🏗️  Building dashboard..."
cd dashboard
npm install
npm run build

# Deploy to Netlify
echo ""
echo "🚀 Deploying to Netlify..."
netlify deploy --prod --dir=build --site=carbonica

echo ""
echo "✅ Deployment complete!"
echo "📊 Dashboard: https://carbonica.netlify.app"
