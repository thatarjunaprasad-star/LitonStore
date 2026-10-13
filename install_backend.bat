@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
call .venv\Scripts\activate.bat
python -m pip install -r backend\requirements.txt
