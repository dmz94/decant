# Fixtures Structure

This directory contains structured fixture inputs and outputs
used for deterministic testing.

## input/
Raw HTML inputs used for core extraction and transformation tests.

Only source HTML files belong here.
No generated `.flowdoc.html` files should exist in this directory.

## user-study/
HTML inputs used for dyslexia validation testing.

### output/
Generated Flowdoc artifacts corresponding to user-study inputs.
These are version-pinned outputs used for regression awareness.

## scripts/
Helper scripts related to fixture generation or fetching
are located in `tests/scripts/`, not inside fixture directories.
