#!/bin/bash
# scripts/setup_env.sh — Environment Setup Script
#
# PURPOSE:
#   Automates the creation of a virtual environment and installation
#   of all project dependencies. Run this once when setting up the project.
#
# USAGE:
#   bash scripts/setup_env.sh
#
# WHAT IT DOES:
#   1. Creates a .venv virtual environment
#   2. Activates it
#   3. Upgrades pip
#   4. Installs project dependencies in editable mode

set -e

echo "🔧 Setting up AI Bug Triage System..."

# Create virtual environment
python3 -m venv .venv
echo "✅ Virtual environment created at .venv/"

# Activate
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
pip install --upgrade pip
echo "✅ pip upgraded"

# Install dependencies
pip install -e ".[dev]"
echo "✅ Dependencies installed"

# Copy .env template if .env doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env created from .env.example — please fill in your API keys!"
else
    echo "ℹ️  .env already exists, skipping"
fi

echo ""
echo "🎉 Setup complete! Next steps:"
echo "   1. Edit .env and add your OPENAI_API_KEY"
echo "   2. Run: make load-data"
echo "   3. Run: make run-ui"
