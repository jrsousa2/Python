@echo off
REM Check if the argument %1 is provided

IF "%~1"=="" (
    echo Rerun code with commit description
) ELSE (
    cd D:\Python\Cloud
    set GIT_TRACE=1
    echo FORCE A RE-READING OF THE .gitignore list
    git rm -r --cached .
    git add .
    git branch -M main
    git commit -m %1
    REM COMMENTED OUT CODE FORCES A PUSH
    REM It loses track of remote updates
    REM The below command will only download the README.MD
    REM git pull origin main --allow-unrelated-histories
    REM DO NOT FORCE PUSH, BEST TO MERGE HISTORIES FIRST
    echo DO NOT EDIT ANYTHING REMOTELY TO NOT CAUSE CONFLICT
    REM git push origin main --force
    git push origin main
    REM echo sem nada mostra o echo status
    echo .
    echo .
    echo VIEWS IF BATCH SUCCEEDED
    git log -n 1
    cd D:\Python
)

rem Doublechek if the remote repo is fine
rem git remote -v

