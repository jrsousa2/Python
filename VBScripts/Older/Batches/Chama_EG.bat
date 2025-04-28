echo off
rem Reading date
set Day=%date:~0,2%
set Month=%date:~3,3% 
set Year=%date:~7,4%

rem echo Year is %Year%
rem echo Month is %Month%
rem echo Day is %Day%

rem CONVERTS MONTH TO NUMERIC
if %month% equ Jan set Month_no=1
if %month% equ Feb set Month_no=2
if %month% equ Mar set Month_no=3
if %month% equ Apr set Month_no=4
if %month% equ May set Month_no=5
if %month% equ Jun set Month_no=6
if %month% equ Jul set Month_no=7
if %month% equ Aug set Month_no=8
if %month% equ Sep set Month_no=9
if %month% equ Oct set Month_no=10
if %month% equ Nov set Month_no=11
if %month% equ Dec set Month_no=12

echo Month is %month_no%
set today_date=%day%-%month_no%-%year%
set past_date=23-08-2012

rem Creates dates
echo Today date is %today_date%
echo Past date is %past_date%
rem O abaixo eh para eu ver primeiro as datas antes de chamar SAS
rem pause

rem Sets date to past
date %past_date%
start "" "C:\Program Files\SASHome\x86\SASEnterpriseGuide\4.3\SEGuide.exe" /openfile:F:\Python\EG\organiza.egp

rem The below will set the date back to what it was
echo Press a key to continue
pause 
date %today_date%