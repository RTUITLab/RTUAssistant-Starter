@echo off

Python\python.exe -m venv env

call env\Scripts\activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt

call env\Scripts\deactivate.bat