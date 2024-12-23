echo off
rem Reading date
set Year=%date:~7,4%
set Month=%date:~3,3%
set Day=%date:~0,2%

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
set past_date=01-%month_no%-2012

rem Creates dates
echo Date is %today_date%
echo Past date is %past_date%

rem Sets date to past
rem date %past_date%
rem start "" "C:\Program Files\SASHome\x86\SASEnterpriseGuide\4.3\SEGuide.exe" /openfile:D:\iTunes\Codes\organiza.egp

rem The below will set the date back to what it was
rem echo Press a key to continue
rem pause 
rem date %today_date%