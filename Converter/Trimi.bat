REM ESSE SCRIPT RECEBE PARAMETROS E CRIA UMA COPIA DO FILME
REM COMECANDO NO TEMPO INIT E TERMINANDO EM END
REM SALVA O ARQUIVO COM INIT E END COMO SUFIXO

@echo off
REM ABAIXO EH NECESSARIO PQ VARIAVEIS ESTAO SENDO SETADAS DENTRO DE UM LOOP

rem SAVES THE CURRENT DIRECTOR BEFORE CHANGING DIRS
set Init_CD=%CD%
echo.
echo FOLDER INICIAL=%Init_CD%

REM DIRETORIO QUE CONTEM ARQUIVO
set Diret=%1
echo.
echo DIRETORIO QUE CONTEM ARQUIVO=%Diret%

rem FILE TO BE PROCESSED
rem ###########################################################################
set File=%~2
rem ###########################################################################
echo.
echo FILE TO BE PROCESSED: "%File%"

rem O abaixo pula uma linha
echo.

REM SETA OS TEMPOS
set Ini_time=%3
set End_time=%4

REM SETA A SEQUENCIA DO OUTPUT
set Nbr=%5

REM SETA O PERSONAGEM
set Persona=%~6


rem Replaces chars
set spec=:
set word=_
rem REPLACE IN INITIAL TIME
call set Ini_time_val=%%Ini_time:%spec%=%word%%%
SET Ini_M=%Ini_time_val:~3,2%
SET Ini_S=%Ini_time_val:~6,2%

echo.
echo Ini_time_val=%Ini_time_val% Min=%Ini_M% Sec=%Ini_S%

rem REPLACE IN END TIME
call set End_time_val=%%End_time:%spec%=%word%%%
SET End_M=%End_time_val:~3,2%
SET End_S=%End_time_val:~6,2%

echo.
echo End_time_val=%End_time_val% Min=%End_M% Sec=%End_S%

echo.
echo FILE NUMBER "%Nbr%"

REM CORRIGE PERSONAGEM:
set Persona='%Persona:'=''%'
echo.
echo PERSONAGEM "%Persona%"

REM CRIANDO FILENAME COM PATH+NAME
set Fullfile=%Diret%\%File%

setlocal ENABLEDELAYEDEXPANSION

for /f "delims=|" %%f in ("dir /b %Fullfile%") do (

 set File_no_ext=%%~nf
 rem EPISODE NAME IS SIMPLY THE FILE NAME WITHOUT THE PREFIX "SATC-"
 SET Episode=!File_no_ext:~7,95!

 echo.
 echo FILE NAME WITHOUT EXTENSION "!File_no_ext!"
 echo EPISODE NAME "!Episode!"

 rem EXTENSION 
 set File_ext=%%~xf
 echo FILE EXTENSION "!File_ext!" 
)

set Episode='%Episode:'=''%'
echo EPISODE NAME CORRIGIDO "%Episode%"

echo.
ECHO TIME:
rem set Tempo=enable='between(t,60*%Ini_M%+%Ini_S%,60*%End_M%+%End_S%)'
set Tempo=enable='between(t,60*%Ini_M%+%Ini_S%,5+60*%Ini_M%+%Ini_S%)'
echo.
ECHO Tempo=%Tempo%

REM SOBE AS LEGENDAS UM POUCO PRA CIMA
set Offset=28
echo.
ECHO POSICAO1:
rem 9/10 OF THE HEIGHT
rem set Posicao1=x=(w-text_w)/2:y=9*(h-text_h)/10
rem BOTTOM CENTER
set Posicao1=x=(w-text_w)/2:y=-50-%Offset%+h-th
echo.
ECHO Posicao1=%Posicao1%

echo.
ECHO DRAWTEXT LINE1:
set Base1=drawtext=fontfile=C\\:/Windows/fonts/arial.ttf:text=%Episode%:fontcolor=yellow:fontsize=45
set Draw1=%Base1%:%Posicao1%:%Tempo%
echo.
ECHO DRAW1=%draw1%

echo.
ECHO POSICAO2:
rem 9/10 OF THE HEIGHT
rem set Posicao2=x=(w-text_w)/2:y=45+9*(h-text_h)/10
rem BOTTOM CENTER
set Posicao2=x=(w-text_w)/2:y=-%Offset%+h-th
echo.
ECHO Posicao2=%Posicao2%


echo.
ECHO DRAWTEXT LINE2:
set Base2=drawtext=fontfile=C\\:/Windows/fonts/arial.ttf:text=%Persona%:fontcolor=yellow:fontsize=38
set Draw2=%Base2%:%Posicao2%:%Tempo%
echo.
ECHO DRAW2=%Draw2%

echo.
ECHO DRAWTEXT BOTH LINES:
set Draw="[in]%Draw1%,%Draw2%[out]"
echo.
ECHO DRAW=%Draw%

set Output=%Init_CD%\%Nbr%-%File_no_ext%-%Ini_time_val%-%End_time_val%.mp4
echo.
echo OUTPUT FILE NAME "%Output%"

echo.
echo START TRIMMING: "%Diret%\%File%"
echo.

rem RE-ENCODE E INSERE O TEXTO
echo.
echo CODE="C:\ffmpeg\bin\ffmpeg.exe" -y -i "%Fullfile%" -ss %Ini_time% -to %End_time% -c:v libx265 -c:a copy -vf %Draw% "%Output%"

REM CALL CODE
call "C:\ffmpeg\bin\ffmpeg.exe" -y -i "%Fullfile%" -ss %Ini_time% -to %End_time% -c:v libx265 -c:a copy -vf %Draw% "%Output%"

echo.
echo TRIMMING FINISHED!

