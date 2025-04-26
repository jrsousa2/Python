@echo off
rem setlocal

REM Path to your existing repo clone
set REPO_PATH=D:\iTunes\Music_clone

rem Create the target folder (if it doesn't exist)
if not exist "%REPO_PATH%" (
    echo Creating target folder...
    mkdir "%REPO_PATH%"
)

REM Go to the repo and ensure it is linked to the remote
cd /d %REPO_PATH%
git init
git remote add origin https://github.com/jrsousa2/Python-scripts-for-iTunes-WMP.git
git pull origin main

REM SKIP LINE
echo .

REM FIRST iTunes
copy /y "D:\iTunes\Music\Call_Save_to_Excel.py" "%REPO_PATH%"
copy /y "D:\iTunes\Music\Call_Sync_Plays.py" "%REPO_PATH%"
copy /y "D:\iTunes\Music\Read_PL.py" "%REPO_PATH%"
copy /y "D:\iTunes\Music\README.md" "%REPO_PATH%"

REM NOW WMP
copy /y "D:\iTunes\WMP\WMP_Read_PL.py" "%REPO_PATH%"

REM SKIP LINE
echo .
REM CHECK IF ALL IS RIGHT BEFORE TRYING TO PUSH THE CHANGES
rem pause

REM PREPARE THE GITHUB REPO
git add .
git branch -M main
git commit -m "Updating selected files"
git push origin main
echo .
echo .
echo VIEWS IF BATCH SUCCEEDED
git log -n 1

rem CD BACK TO ORIGINAL FOLDER
cd D:\iTunes

REM Give Git a little time to finish any background tasks
timeout /t 3

rem Delete the target folder after operation (optional)
rd /s /q "%REPO_PATH%"

