#!/bin/bash
# Quick start: LLM-powered divergence analysis

set -e

echo "===== Bilingual AIA Divergence Analysis ====="
echo ""

# Step 1: Install dependencies
echo "📦 Installing OpenAI SDK..."
pip install openai python-dotenv

# Step 2: Setup API key
echo ""
echo "🔑 Setting up API key..."
if [ ! -f research/.env ]; then
    cp research/.env.template research/.env
    echo "✓ Created research/.env"
    echo "⚠️  Please add your OPENAI_API_KEY to research/.env"
    echo ""
    read -p "Press Enter once you've added your API key..."
else
    echo "✓ research/.env already exists"
fi

# Step 3: Verify corpus
echo ""
echo "🔍 Checking corpus..."
if [ ! -d data/processed ]; then
    echo "⚠️  No processed corpus found."
    echo "Run this first:"
    echo "  python research/crawl.py --limit 5"
    echo "  python research/extract_text.py"
    echo "  python research/normalize.py"
    exit 1
fi

RECORD_COUNT=$(find data/processed -name normalized.json | wc -l)
echo "✓ Found $RECORD_COUNT processed records"

# Step 4: Dry run
echo ""
echo "🧪 Dry run (no API calls)..."
python research/analyze_divergence.py --dry-run

# Step 5: Analyze
echo ""
echo "🚀 Running analysis (this will use API credits)..."
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python research/analyze_divergence.py --limit 5
    echo ""
    echo "✓ Analysis complete!"
    echo "  Analyses: research/output/divergence_analyses.jsonl"
    echo "  Report: research/output/divergence_report.json"
else
    echo "Cancelled."
fi
