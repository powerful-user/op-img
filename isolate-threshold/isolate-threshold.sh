#!/bin/bash
# isolate-black.sh — Extract black lines from an image with transparent background
# Uses nearest-neighbor upscaling for a crisp, pixelated aesthetic
#
# Usage: ./isolate-black.sh <input> [output] [scale]
#   input  - Source image (GIF, PNG, JPG, etc.)
#   output - Output PNG path (default: <input>-black-4x.png)
#   scale  - Upscale multiplier (default: 4)
#
# Example:
#   ./isolate-black.sh ~/Desktop/consciousness.gif
#   ./isolate-black.sh ~/Desktop/consciousness.gif ~/output/result.png 8

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <input> [output] [scale]"
  exit 1
fi

INPUT="$1"
SCALE="${3:-4}"

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT"
  exit 1
fi

# Derive default output name from input
if [ -n "${2:-}" ]; then
  OUTPUT="$2"
else
  DIR=$(dirname "$INPUT")
  BASE=$(basename "$INPUT" | sed 's/\.[^.]*$//')
  OUTPUT="${DIR}/${BASE}-black-${SCALE}x.png"
fi

# Get original dimensions
DIMS=$(magick identify -format "%wx%h" "$INPUT")
W=$(echo "$DIMS" | cut -dx -f1)
H=$(echo "$DIMS" | cut -dx -f2)
NEW_W=$((W * SCALE))
NEW_H=$((H * SCALE))

echo "Input:  $INPUT ($DIMS)"
echo "Output: $OUTPUT (${NEW_W}x${NEW_H}, ${SCALE}x scale)"

magick "$INPUT" \
  -threshold 50% \
  \( +clone -negate \) \
  -alpha off -compose copy-opacity -composite \
  -filter point -resize "${NEW_W}x${NEW_H}" \
  "$OUTPUT"

echo "Done."
