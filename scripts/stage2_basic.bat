@echo off
cd /d "%~dp0\.."
python -m src.main --vfs stage2-vfs.csv --script scripts/stage2_start.txt
