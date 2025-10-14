#!/bin/bash
# Setup script for Comet ML environment variables

echo "Setting up Comet ML environment variables..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Add Comet ML credentials to .env if not already present
if ! grep -q "COMET_API_KEY" .env; then
    echo "" >> .env
    echo "# Comet ML Configuration" >> .env
    echo "COMET_API_KEY=your_comet_api_key_here" >> .env
    echo "COMET_PROJECT_NAME=your_project_name" >> .env
    echo "COMET_WORKSPACE=your_workspace_name" >> .env
    echo "✅ Comet ML credentials template added to .env"
    echo "⚠️  Please edit .env and add your actual Comet ML credentials"
else
    echo "⚠️  Comet ML credentials already exist in .env"
    echo "Please update them manually if needed:"
    echo "  COMET_API_KEY=your_comet_api_key_here"
    echo "  COMET_PROJECT_NAME=your_project_name"
    echo "  COMET_WORKSPACE=your_workspace_name"
fi

echo ""
echo "✅ Setup complete!"
echo "You can now run the application with Comet ML tracking enabled."
