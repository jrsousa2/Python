@echo off
REM Go to Python Scripts folder
cd /d C:\Python\Python3.11-v1\Scripts

REM Activate the virtual environment
call activate.bat

REM Run your Python script (path with spaces in quotes)
python "D:\Python\Stock Alert\Alert.py"
