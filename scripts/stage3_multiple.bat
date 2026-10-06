@echo off
cd /d "%~dp0\.."
python -m src.main --vfs data/vfs/multiple.csv --script scripts/stage3_multiple.txt
