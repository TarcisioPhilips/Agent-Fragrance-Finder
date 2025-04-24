@echo off
echo Creating and setting up project with uv...

echo Initializing project...
uv init

echo Creating virtual environment...
uv venv

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies... 
uv pip install -r requirements.txt

echo Setup completed!
echo To activate the virtual environment in the future, run: .venv\Scripts\activate 