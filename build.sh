#!/usr/bin/env bash

ADDON_NAME="latex_svg_tikz_inkscape_v2"
OUTPUT_FILE="${ADDON_NAME}.ankiaddon"

rm -f "$OUTPUT_FILE"

zip -r "$OUTPUT_FILE" \
    __init__.py \
    manifest.json \
    config.json \
    README.md

echo "✓ Package created: $OUTPUT_FILE"
echo ""
echo "This version fixes the macOS PATH issue!"
echo ""
echo "Installation:"
echo "1. Uninstall previous LaTeX addon"
echo "2. Tools > Add-ons > Install from file..."
echo "3. Select $OUTPUT_FILE"
echo "4. Restart Anki"
echo ""
echo "The debug console should show:"
echo "  ✓ inkscape found at: /opt/homebrew/bin/inkscape"

