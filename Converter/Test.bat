@echo off
set Diret=D:\Porno\Brasil
    for /R "%Diret%" %%f in (*.avi) do (
    echo %%~nf
)
pause