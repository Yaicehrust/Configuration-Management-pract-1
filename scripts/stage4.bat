@echo off
cd /d "%~dp0\.."
python -m src.main --vfs data/vfs/nested.csv --script scripts/stage4_start.txt
