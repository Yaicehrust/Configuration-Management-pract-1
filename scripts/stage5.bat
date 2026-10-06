@echo off
cd /d "%~dp0\.."
python -m src.main --vfs data/vfs/nested.csv --script scripts/stage5_start.txt
