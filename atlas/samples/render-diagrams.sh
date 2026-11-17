#!/bin/sh
# Build-time only: mmdc 11.12.0 and Chromium. No Mermaid runtime in the gallery.
set -eu
here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
out="$here/../../assets/mermaid"
mkdir -p "$out"
for source in "$here"/*.mmd; do
  name=$(basename "$source" .mmd)
  # Software rasterization avoids small GPU-dependent differences. Override -p for custom Chromium setups.
  mmdc -p "$here/diagram-browser.json" "$@" -i "$source" -o "$out/$name.png" \
    -c "$here/diagram-style.json" -b '#fbf7eb' -w 800 -s 2
done
