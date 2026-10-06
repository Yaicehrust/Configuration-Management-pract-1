#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
python3 -m src.main --vfs data/vfs/nested.csv --script scripts/stage3_nested.txt
