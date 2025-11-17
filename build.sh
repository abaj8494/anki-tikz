#!/usr/bin/env bash

ADDON_NAME="latex_svg_tikz_inkscape_v2"
OUTPUT_FILE="${ADDON_NAME}.ankiaddon"

# Clean up any Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Remove old package
rm -f "$OUTPUT_FILE"

# Create package - ensure files are at root level, not in subfolder
zip "$OUTPUT_FILE" \
    __init__.py \
    manifest.json \
    config.json \
    README.md

echo "Package created: $OUTPUT_FILE"
echo ""
echo "Contents:"
unzip -l "$OUTPUT_FILE"
