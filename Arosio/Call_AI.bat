@echo off
REM IT SEEMS THAT IT NEEDS AT LEAST 4 IMAGES TO PROCESS OR IT WON'T DO IT.
REM setlocal enabledelayedexpansion

REM SET INPUT PARAMETERS, AND SETS A DEFAULT FOR NO PARAMETER PROVIDED
REM setlocal


if "%1%"=="" (
    set "Sel_model=Proteus"
) else (
    set Sel_model=%1
)

REM endlocal

echo.
echo Input was Parameter was: %1%
echo Sel_Model was set to: %Sel_Model%

REM MOVES TO C:
C:

cd "C:\Program Files\Topaz Labs LLC\Topaz Video AI"

REM SET SYSTEM VARS JUST IN CASE
set FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
set FPS_BROWSER_USER_PROFILE_STRING=Default
set SESSIONNAME=Console

:: Set input and output directories
REM set Input_dir=D:/Videos/Arosio/Input
REM set Output_dir=D:/Videos/Arosio/Output

REM #########################################################################

REM THIS IS FOR TEST PURPOSES ONLY
set Input_dir=D:/Videos/Arosio/5s
set output_dir=D:/Videos/Arosio/Tests/%Sel_model%

REM #########################################################################
REM DEFINE THE 5 MODELS

set Proteus="tvai_up=model=prob-4:scale=0:w=1280:h=720:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=0.2:device=0:vram=0.1:instances=1,scale=w=1280:h=720:flags=lanczos:threads=0:force_original_aspect_ratio=increase,crop=1280:720"

set Iris="tvai_up=model=iris-2:scale=0:w=1280:h=720:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=0.2:device=0:vram=0.1:instances=1,scale=w=1280:h=720:flags=lanczos:threads=0:force_original_aspect_ratio=increase,crop=1280:720"

set Nyx="tvai_up=model=nyx-3:scale=1:w=1280:h=720:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:device=0:vram=0.1:instances=1,scale=w=1280:h=720:flags=lanczos:threads=0:force_original_aspect_ratio=increase,crop=1280:720"

set Artemis="tvai_up=model=ahq-12:scale=0:w=1280:h=720:blend=0.2:device=0:vram=0.1:instances=1,scale=w=1280:h=720:flags=lanczos:threads=0:force_original_aspect_ratio=increase,crop=1280:720"

set Theia="tvai_up=model=thf-4:scale=0:w=1280:h=720:noise=0:blur=0:compression=0:device=0:vram=0.1:instances=1,scale=w=1280:h=720:flags=lanczos:threads=0:force_original_aspect_ratio=increase,crop=1280:720"

REM #########################################################################
REM SET THE CHOSEN MODEL


REM Use if/else to assign the corresponding value to Model
if "%Sel_model%"=="Proteus" (
    set Model=%Proteus%
) else if "%Sel_model%"=="Iris" (
    set Model=%Iris%
) else if "%Sel_model%"=="Nyx" (
    set Model=%Nyx%
) else if "%Sel_model%"=="Artemis" (
    set Model=%Artemis%
) else if "%Sel_model%"=="Theia" (
    set Model=%Theia%
) else (
    echo Invalid model selected.
)

REM #########################################################################
REM DISPLAYS INPUT/OUTPUT

echo.
echo INPUT FOLDER is %Input_dir%
echo.
echo OUTPUT FOLDER is %Output_dir%
echo.

REM DISPLAYS THE MODEL CHOSEN
echo CHOSEN MODEL is %Sel_model%
echo.

REM Display the result
echo Model is: %Model%
echo.

REM CHECK IF THE VARIABLES ARE RIGHT
pause

REM #########################################################################

:: Count PNG files in the Input directory
for /f %%A in ('dir /b /a-d "%input_dir%\*.png" 2^>nul ^| find /c /v ""') do set total_frames=%%A


:: Count PNG files in the output directory
for /f %%A in ('dir /b /a-d "%output_dir%\*.png" 2^>nul ^| find /c /v ""') do set frames_done=%%A


REM Increment count by 1
set /a frames_done_pls_1=%frames_done%+1

set frames_done_pls_1=1739

echo.
echo Found %frames_done% PNG files in the output directory (out of %total_frames%)
echo Next frame: %frames_done_pls_1% 
echo.


@echo on

REM CHECK IF THE CODE NEEDS TO RUN
if %frames_done_pls_1% lss %total_frames% (

echo.
echo Found %frames_done% PNG files in the output directory (out of %total_frames%)
echo.

REM -start_number  %frames_done_pls_1%
ffmpeg -hide_banner -start_number %frames_done_pls_1% -i "%input_dir%\frame_%%04d.png"  "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" %Model% "-c:v" "png" "-pix_fmt" "rgb24" -start_number  %frames_done_pls_1% -y "%output_dir%\frame_%%04d.png"

) 
REM else (
REM        echo Skipping FFmpeg command...
REM      )

REM GOES BACK TO ORIGINAL DRIVE:
D:

REM END OF SCRIPT
echo.
echo.
echo FINISHED...

