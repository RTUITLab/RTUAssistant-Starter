@echo off

set VIRTUAL_ENV=test_venv

call test_venv\Scripts\activate.bat

where python

pip list