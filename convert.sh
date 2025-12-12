#!/bin/bash

# Notion to Obsidian Converter - Unix/Linux/Mac Shell Script
# Usage: ./convert.sh <input_directory> <output_directory>

echo "========================================"
echo "Notion to Obsidian Converter"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check if arguments are provided
if [ $# -eq 0 ]; then
    echo "Usage: ./convert.sh <input_directory> <output_directory>"
    echo ""
    echo "Example:"
    echo "  ./convert.sh ./NotionExport ./ObsidianVault"
    echo ""
    exit 1
fi

if [ $# -eq 1 ]; then
    echo "Usage: ./convert.sh <input_directory> <output_directory>"
    echo ""
    echo "Example:"
    echo "  ./convert.sh ./NotionExport ./ObsidianVault"
    echo ""
    exit 1
fi

# Run the converter
echo "Converting from: $1"
echo "Converting to:   $2"
echo ""
echo "Please wait..."
echo ""

python3 notion_to_obsidian.py "$1" "$2" --verbose

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Conversion completed successfully!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "Conversion failed. Please check errors above."
    echo "========================================"
    exit 1
fi

echo ""
