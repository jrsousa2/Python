@echo off
REM MODEL IS CHOSEN BY AN INPUT PARAMETER AT CALL TIME: 
REM IT CAN BE: Proteus (Default-no pmt needed) Iris / Nyx / Gaia / Artemis / Theia

REM IT SEEMS THAT FILTER NEEDS AT LEAST 4 IMAGES TO PROCESS OR IT WON'T DO IT.
REM setlocal enabledelayedexpansion

REM SET ALL INPUT PARAMETERS (CODE SETS A DEFAULT FOR NO PARAMETER PROVIDED)
REM setlocal

REM ENTER HERE THE DEFAULT MODEL
set Default_mod=Proteus

if "%1%"=="" (
    set "Sel_model=%Default_mod%"
) else (
    set Sel_model=%1
)

REM SET THE BASE DIRECTORY HERE AND THE REST IS MOSTLY AUTOMATICALLY SET
set Base_dir=F:\Videos\Pobres

REM SET INPUT AND OUTPUT DIRECTORIES
set Input_dir=%Base_Dir%\Input

REM THE OUTPUT FOLDER IS NAMED AFTER THE CHOSEN MODEL
set output_dir=%Base_Dir%\Output_%Sel_model%

REM SET THE DIMENSIONS OF THE UPSCALE
REM EG (HD=1280X760 / FULL HD=1920X1080)

REM THESE VALES ARE BEING USED (NO NEED TO SPECIFY IF NOT RE-SCALING)
set dim_Wid=1440
set dim_Hei=1080

REM DON'T FORGET TO SET THE INPUT/OUTPUT IMAGE TYPE
set Ext=png

REM RE-SCALING VIDEO
set Re_scale_YN=Y

REM IF RE-SCALING THE VIDEO, IT'S EITHER PADDING WITH VERTICAL BARS OR CROPPING VIDEO BASELINES
set Re_scale_Pad=N

REM IF APPLICABLE, WILL THE ASPECT RATIO FOR THE UPSCALED MATCH THE THE ORIGINAL VIDEO?
set Aspect_ratio_change=N

REM INPUT QUALITY
set Input_quality=low

REM 0=no denoise, 0.1 to 1 (higher=remove more noise)
set noise=0

REM Sharpen/enhance details: 0.1 to 1 (0=no sharpening)
set details=0

REM Optional slight blur before processing (0=no pre-blur)
set preblur=0

REM Recover Detail (rdt)
REM Purpose: tells the AI to try to add or enhance fine textures and micro-details in the frame
REM that may have been lost due to compression, blur, or denoising.
REM Effect: makes edges sharper, surfaces more detailed.
REM Scope: mostly local detail, often affects textures in foliage, hair, fabric, etc.
REM Range: 0.0 TO 1.0
REM Default / safe: 0.3 – 0.4
REM Adds visible detail without making textures harsh or unnatural
REM Stronger: 0.5 – 0.6
REM For softer or compressed footage, but can look "crispy" if too high
set rdt=0.3

REM RECOVER ORIGINAL DETAIL / BLEND 
REM IN MODELS: PROTEUS/IRIS/NYX/ARTEMIS
REM NOT IN: GAIA / THEIA (NOT IN RHEA EITHER, BUT RHEA IS UNUSABLE ANYWAY)
REM Purpose: mixes a fraction of the original unprocessed frame back into the enhanced output.
REM Effect: prevents over-sharpening or "hallucination" by the AI; preserves naturalness and prevents artifacts.
REM Scope: global frame blending, not just micro-texture.
REM Always optional - you choose how much original image you want to "retain."
REM PMT IS CALLED BLEND IN THE FILTER
REM RANGE: 0.0 TO 1.0
set rec_orig_detail=0.4

REM estimate controls motion/temporal analysis depth
REM It's very expensive computationally
REM VALUES=8 (slowest) To 1 (fastest)
set estimate=8

REM VRAM USE AS A PERC OF GPU VRAM
set vram=0.7

REM INSTANCES (DEFAULT IS 1)
set instances=2

REM #########################################################################
REM #########################################################################

REM endlocal

echo.
echo Input Parameter was: %1%
echo Selected_Model was set to: %Sel_Model%

if not exist "%output_dir%" (
    echo.
    echo Directory "%output_dir%" doesn't exist, creating...
    mkdir "%output_dir%"
    REM pause
)


REM #########################################################################
REM #########################################################################
REM #########################################################################
REM NO PMTS BELOW


REM MOVES TO C:
C:

cd "C:\Program Files\Topaz Labs LLC\Topaz Video AI"

REM SET SYSTEM VARS JUST IN CASE
set FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
set FPS_BROWSER_USER_PROFILE_STRING=Default
set SESSIONNAME=Console


REM #########################################################################


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


REM ##################################################################################
REM ##################################################################################

REM DEFINE THE 6 MODELS


if %Input_quality%==low (
 set Iris_model=iris-3
) else (
 set Iris_model=iris-2
)

REM NEEDED SO AI UPSCALES THE FRAME
REM THE 2nd UPSCALE IS DONE BY FFMPEG (JUST A TOUCH-UP/ADJUSTMENT)
if %Re_scale_YN%==Y (
set Scale_pmt=:scale=0:w=%dim_Wid%:h=%dim_Hei%
) else (
set set Scale_pmt=
)

REM PROTEUS: GENERAL ENHANCEMENT FOR MOST VIDEOS
set Proteus="tvai_up=model=prob-4%Scale_pmt%:preblur=0:noise=%noise%:details=%details%:halo=0:blur=0:compression=0:estimate=%estimate%:blend=%rec_orig_detail%:device=0:vram=0.1:instances=%instances%%Re_scale%"


REM IRIS: SPECIAL ENHANCEMENT FOR FACES 
REM Iris doesn't have pmt: rdt=%rdt% 
set Iris="tvai_up=model=%Iris_model%%Scale_pmt%:preblur=0:noise=%noise%:details=%details%:halo=0:blur=0:compression=0:estimate=%estimate%:blend=%rec_orig_detail%:device=0:vram=%vram%:instances=%instances%%Re_scale%"


REM NYX: DEDICATED DENOISING
set Nyx="tvai_up=model=nyx-3%Scale_pmt%:preblur=0:noise=%noise%:details=%details%:halo=0:blur=0:compression=0:estimate=%estimate%:device=0:vram=%vram%:instances=%instances%%Re_scale%"

REM ARTEMIS: DENOISE AND SHARPEN
set Artemis="tvai_up=model=ahq-12:scale=0:w=%dim_Wid%:h=%dim_Hei%:blend=%rec_orig_detail%:device=0:vram=%vram%:instances=%instances%%Re_scale%"

REM THEIA: HIGH FIDELITY AND DETAIL ENHANCEMENT
set Theia="tvai_up=model=thf-4%Scale_pmt%:noise=%noise%:blur=0:compression=0:device=0:vram=%vram%:instances=%instances%%Re_scale%"

REM GAIA: Upscale HQ: If your goal is to upscale high-quality footage to HD or 4K resolutions while REM preserving details, Gaia is a suitable choice. 
set Gaia="tvai_up=model=ghq-5%Scale_pmt%:preblur=0:noise=%noise%:details=%details%:halo=0:blur=0:compression=0:estimate=%estimate%:blend=%rec_orig_detail%:device=0:vram=%vram%:instances=%instances%%Re_scale%"

REM #########################################################################
REM SET THE CHOSEN MODEL


REM Use if/else to assign the corresponding value to Model
if "%Sel_model%"=="Proteus" (
    set Model=%Proteus%
) else if "%Sel_model%"=="Iris" (
    set Model=%Iris%
    set rdt=0.0
) else if "%Sel_model%"=="Nyx" (
    set Model=%Nyx%
) else if "%Sel_model%"=="Artemis" (
    set Model=%Artemis%
) else if "%Sel_model%"=="Gaia" (
    set Model=%Gaia%
) else if "%Sel_model%"=="Theia" (
    set Model=%Theia%
) else (
    echo Invalid model selected.
)

REM #########################################################################
REM DISPLAYS INPUT/OUTPUT

echo.
echo INPUT FOLDER is "%Input_dir%"
echo.
echo OUTPUT FOLDER is "%Output_dir%"
echo.

REM DISPLAYS THE MODEL CHOSEN
echo CHOSEN MODEL is %Sel_model%
echo.

echo INPUT/OUTPUT IMG TYPE: %Ext%
echo.

echo Re_scale_YN=%Re_scale_YN%
echo Re_scale_Padding=%Re_scale_Pad%
echo Aspect_ratio_change=%Aspect_ratio_change%
echo.

REM Display the result
echo Model is: %Model%
echo.

REM Display the input quality
echo Input quality is: %Input_quality%
echo.

echo Recover detail=%rdt%
echo.

echo Recover Original detail=%rec_orig_detail%
echo.

echo Noise (Increasing levels of noise reduction)=%noise%
echo.

echo Details (Extra sharpening)=%details%
echo.

echo Estimate (Lower->faster)=%estimate%
echo.

echo GPU VRAM percentage=%vram%
echo.

echo Running instances=%instances%
echo.

REM @FOR TEST
rem pause

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

REM THE CODE AS WILL BE RUN WITH TVAI FILTER
echo BELOW IS THE CMD THAT WILL BE RUN
echo ffmpeg -hide_banner -hwaccel_device 0 -start_number %frames_done_pls_1% -i "%input_dir%\frame_%%04d.%Ext%" "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" %Model% "-c:v" "%Ext%" "-pix_fmt" "rgb24" -start_number %frames_done_pls_1% -y "%output_dir%\frame_%%04d.%Ext%"
echo.

    REM RUN THE MAIN COMMAND
    ffmpeg -hide_banner -hwaccel_device 0 -start_number %frames_done_pls_1% -i "%input_dir%\frame_%%04d.%Ext%"  "-sws_flags" "spline+accurate_rnd+full_chroma_int" "-filter_complex" %Model% "-c:v" "%Ext%" "-pix_fmt" "rgb24" -start_number  %frames_done_pls_1% -y "%output_dir%\frame_%%04d.%Ext%"

    REM GOES BACK TO ORIGINAL DRIVE:
    D:

    REM END OF SCRIPT
    echo.
    echo.
    echo FINISHED CURRENT BATCH

    REM HERE THE BATCH SCRIPT IS CALLED AGAIN.
    echo RESTARTING...
    rem call_AI_Template %Sel_Model%
    call "%~dp0%~nx0" %Sel_Model%

) else (
    D:
    echo THE END!
    echo.
)

