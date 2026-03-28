@echo off
REM IT SEEMS THAT IT NEEDS AT LEAST 4 IMAGES TO PROCESS OR IT WON'T DO IT.
REM setlocal enabledelayedexpansion

REM SET INPUT PARAMETERS, AND SETS A DEFAULT FOR NO PARAMETER PROVIDED
REM setlocal

:: Set input and output directories
REM set Input_dir=D:/Videos/Praia/Input
REM set Output_dir=D:/Videos/Praia/Output

REM #########################################################################

REM SET THE DIMENSIONS OF THE UPSCALE
rem set dim_Hei=1080
rem set dim_Wid=1920

rem set dim_Hei=760
rem set dim_Wid=1280

set dim_Hei=1080
set dim_Wid=1440

REM DON'T FORGET TO SET THE IMAGE TYPE
set Ext=tiff

REM #########################################################################

REM ENTER HERE THE DEFAULT MODEL
set Default_mod=Proteus

if "%1%"=="" (
    set "Sel_model=%Default_mod%"
) else (
    set Sel_model=%1
)

REM endlocal

echo.
echo Input Parameter was: %1%
echo Sel_Model was set to: %Sel_Model%

REM THIS IS FOR TEST PURPOSES ONLY
set Input_dir=D:/Videos/Praia/5s
set output_dir=D:/Videos/Praia/Models/%Sel_model%

if not exist "%output_dir%" (
    echo.
    echo Directory "%output_dir%" doesn't exist, creating...
    mkdir "%output_dir%"
)


REM MOVES TO C:
C:

cd "C:\Program Files\Topaz Labs LLC\Topaz Video AI"

REM SET SYSTEM VARS JUST IN CASE
set FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
set FPS_BROWSER_USER_PROFILE_STRING=Default
set SESSIONNAME=Console


REM #########################################################################
REM SET THE VARIABLES

REM RE-SCALING VIDEO
set Re_scale_YN=Y

REM IF RE-SCALING THE VIDEO, IT'S EITHER PADDING WITH VERTICAL BARS OR CROPPING VIDEO BASELINES
set Re_scale_Pad=N

REM IF APPLICABLE, WILL THE ASPECT RATIO FOR THE UPSCALED MATCH THE THE ORIGINAL VIDEO?
set Aspect_ratio_change=N

REM BLOCK OF NESTED IF'S
if %Re_scale_YN%==Y (

    if %Aspect_ratio_change%==Y (
        
        REM IF ASPECT RATIO WILL CHANGE SET VAR CROP
        if %Re_scale_Pad%==Y (
            REM ADICIONA BARRAS LATERAIS PRA COMPLETAR AS DIMENSOES
            echo.
            echo Padding with vertical bars to obtain desired aspect ratio
            set crop=decrease^,pad=%dim_Wid%:%dim_Hei%:-1:-1:color=black
        ) else (
            REM REDIMENSIONA TIRANDO PARTES DOS LADOS PRA DAR 16:9
            echo.
            echo Cropping frames to obtain desired aspect ratio
            set crop=increase^,crop=%dim_Wid%:%dim_Hei%
        )

        REM FORCE ASPECT RATIO ONLY NEEDED IF ASPECT RATIO IS DIFFERENT FROM ORIGINAL
        set Aspect_ratio=^:force_original_aspect_ratio=%crop%

    ) else (
        REM IF THE ASPECT RATIO IS THE SAME FOR THE UPSCALED AS THE ORIGINAL VIDEO THEN VARIABLE IS BLANK
        echo.
        echo Video aspect ratio won't change
        set Aspect_ratio=
    )

    REM SET RE-SCALING VARIABLE
    set Re_scale=^,scale=w=%dim_Wid%:h=%dim_Hei%:flags=lanczos:threads=0%Aspect_ratio%

) else (

    REM IF NOT RE-SCALING THEN VARIABLE IS BLANK
    echo.
    echo Not re-scaling video
    set Re_scale=
)


rem RECOVER DETAIL (MODELS PROTEUS/IRIS/ARTEMIS) 0.0 TO 1.0
set rec_detail=0.4

REM DEFINE THE 5 MODELS

REM PROTEUS: GENERAL ENHANCEMENT FOR MOST VIDEOS
set Proteus="tvai_up=model=prob-4:scale=0:w=%dim_Wid%:h=%dim_Hei%:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=%rec_detail%:device=0:vram=0.1:instances=1%Re_scale%"

REM IRIS: SPECIAL ENHANCEMENT FOR FACES 
set Iris="tvai_up=model=iris-2:scale=0:w=%dim_Wid%:h=%dim_Hei%:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:blend=%rec_detail%:device=0:vram=0.1:instances=1%Re_scale%"

REM NYX: DEDICATED DENOISING
set Nyx="tvai_up=model=nyx-3:scale=1:w=%dim_Wid%:h=%dim_Hei%:preblur=0:noise=0:details=0:halo=0:blur=0:compression=0:estimate=8:device=0:vram=0.1:instances=1%Re_scale%"

REM ARTEMIS: DENOISE AND SHARPEN
set Artemis="tvai_up=model=ahq-12:scale=0:w=%dim_Wid%:h=%dim_Hei%:blend=%rec_detail%:device=0:vram=0.1:instances=1%Re_scale%"

REM THEIA: HIGH FIDELITY AND DETAIL ENHANCEMENT
set Theia="tvai_up=model=thf-4:scale=0:w=%dim_Wid%:h=%dim_Hei%:noise=0:blur=0:compression=0:device=0:vram=0.1:instances=1%Re_scale%"

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

REM #########################################################################

:: Count image files in the Input directory
for /f %%A in ('dir /b /a-d "%input_dir%\*.%Ext%" 2^>nul ^| find /c /v ""') do set total_frames=%%A


:: Count image files in the output directory
for /f %%A in ('dir /b /a-d "%output_dir%\*.%Ext%" 2^>nul ^| find /c /v ""') do set frames_done=%%A


REM Increment count by 1
set /a frames_done_pls_1=%frames_done%+1

REM SET START FRAME MANUALLY
REM set frames_done_pls_1=30

REM TURN OFF DISPLAY OF CMDS
REM @echo on

REM DISPLAY INFO BEFORE PROCEEDING
echo Found %frames_done% %Ext% files in the output directory ^(out of %total_frames%^)
echo Next frame: %frames_done_pls_1%
echo.

REM CHECK IF THE VARIABLES ARE RIGHT
rem pause

REM CHECK IF THE CODE NEEDS TO RUN
if %frames_done_pls_1% lss %total_frames% (

    REM THE MAIN COMMAND
    ffmpeg -hide_banner -start_number %frames_done_pls_1% -i "%input_dir%\frame_%%04d.%Ext%"  "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" %Model% "-c:v" "%Ext%" "-pix_fmt" "rgb24" -hwaccel_device 0 -start_number  %frames_done_pls_1% -y "%output_dir%\frame_%%04d.%Ext%"

    REM GOES BACK TO ORIGINAL DRIVE:
    D:

    REM END OF SCRIPT
    echo.
    echo.
    echo FINISHED THIS BATCH

    echo RESTARTING...
    call_AI

) else (
    D:
    echo THE END!
)

