@echo off
REM Check if the argument %1 is provided

IF "%~1"=="" (
    echo Setting description to Updt
    echo .
    set Desc=Updt
) ELSE (
  set Desc=%1
)


 cd D:\Python
 set GIT_TRACE=1
 echo FORCE A RE-READING OF THE .gitignore list
 git rm -r --cached .
 git add .
 git branch -M main
 git commit -m %Desc%
 REM COMMENTED OUT CODE FORCES A PUSH
 REM It loses track of remote updates
 REM git push origin main --force
 git push origin main
 REM echo sem nada mostra o echo status
 echo .
 echo .
 echo VIEWS IF BATCH SUCCEEDED
 git log -n 1

