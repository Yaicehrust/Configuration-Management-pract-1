@echo off
cd /d "%~dp0\.."
python -m src.main --vfs data/vfs/minimal.csv --script scripts/stage3_minimal.txt
