@echo off
REM IT SEEMS THAT IT NEEDS AT LEAST 4 IMAGES TO PROCESS OR IT WON'T DO IT.
REM setlocal enabledelayedexpansion

REM MOVES TO C:
C:

cd "C:\Program Files\Topaz Labs LLC\Topaz Video AI"

REM SET SYSTEM VARS JUST IN CASE
set FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
set FPS_BROWSER_USER_PROFILE_STRING=Default
set SESSIONNAME=Console


:: Set input and output directories
set input_dir=D:/Videos/Arosio/Input
set output_dir=D:/Videos/Arosio/Output


:: Count PNG files in the Input directory
for /f %%A in ('dir /b /a-d "%input_dir%\*.png" 2^>nul ^| find /c /v ""') do set total_frames=%%A


:: Count PNG files in the output directory
for /f %%A in ('dir /b /a-d "%output_dir%\*.png" 2^>nul ^| find /c /v ""') do set frames_to_go=%%A

echo.
echo.
echo Found %frames_to_go% PNG files in the output directory (of %total_frames%)
echo.
echo.

REM Increment count by 1
set /a frames_to_go+=1

REM CHECK IF THE CODE NEEDS TO RUN
if %frames_to_go% lss %total_frames% (
    ffmpeg -hide_banner -start_number %frames_to_go% -i "%input_dir%\frame_%%04d.png"  "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" "tvai_up=model=prob-4:scale=0:w=1072:h=712:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=0.2:device=0:vram=0.1:instances=1,scale=w=1072:h=712:flags=lanczos:threads=0" "-c:v" "png" "-pix_fmt" "rgb24" -start_number %frames_to_go% "%output_dir%\frame_%%04d.png"
) else (
    echo Skipping FFmpeg command...
)

REM GOES BACK TO ORIGINAL DRIVE:
D:

REM END OF SCRIPT
echo.
echo.
echo FINISHED...

