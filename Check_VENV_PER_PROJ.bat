@echo off
cd /d D:\Python
echo Searching 6 GB SIZED VENV's...
echo.
findstr /s /i /c:"Python3.9-v2" settings.json
echo.
findstr /s /i /c:"Python3.10-v1" settings.json
echo.
echo Done.
cmd /k