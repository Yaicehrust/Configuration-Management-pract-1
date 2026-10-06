#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main --vfs data/vfs/minimal.csv --script scripts/stage2_start.txt
