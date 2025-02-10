@echo off
REM IT SEEMS THAT IT NEEDS AT LEAST 4 IMAGES TO PROCESS OR IT WON'T DO IT.
setlocal enabledelayedexpansion

C:

cd "C:\Program Files\Topaz Labs LLC\Topaz Video AI"

REM SET SYSTEM VARS JUST IN CASE
set FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
set FPS_BROWSER_USER_PROFILE_STRING=Default
set SESSIONNAME=Console


:: Set input and output directories
set input_dir=D:/Videos/Olivia/Input
set output_dir=D:/Videos/Olivia/output

:: Initialize counter
set count=0

:: Count PNG files in the output directory
for /f %%A in ('dir /b /a-d "%output_dir%\*.png" 2^>nul ^| find /c /v ""') do set frames_to_go=%%A

echo.
echo.
echo Found %frames_to_go% PNG files in the output directory.
echo.
echo.

:: Increment count by 1
set /a frames_to_go+=1

REM RANGE OF FILES OUTSIDE THE LOOP
rem -vframes goes after input
ffmpeg -hide_banner -start_number %frames_to_go% -i "%input_dir%\frame_%%04d.png"  "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" "tvai_up=model=prob-4:scale=0:w=640:h=480:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=0.2:device=0:vram=0.1:instances=1,scale=w=640:h=480:flags=lanczos:threads=0" "-c:v" "png" "-pix_fmt" "rgb24" -start_number %frames_to_go% "%output_dir%\frame_%%04d.png"

echo.
echo.
echo FINISHED...

:: Loop through all files in the input directory
@REM for %%F in (%input_dir%\*.png) do (
@REM     set file=%%~nxF
@REM     set input_file=%Input_dir%\!file!

@REM     set output_file=%Output_dir%\!file!

@REM     :: Check if the file is not in the output folder
@REM     if not exist "!output_file!" (
@REM         :: If the file doesn't exist in the output folder, process it
@REM         echo.
@REM         echo.
@REM         echo Processing "%input_dir%\!file!"
@REM         echo.
@REM         echo.
@REM         @REM ffmpeg -hide_banner "-framerate" "29.97" "-start_number" "%count%" -i "%input_dir%\!file!" -vframes "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" "tvai_up=model=prob-4:scale=0:w=640:h=480:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=0.2:device=0:vram=0.1:instances=1,scale=w=640:h=480:flags=lanczos:threads=0" "-c:v" "png" "-pix_fmt" "rgb24" "%output_dir%\!file!"
        
@REM     )
@REM )
