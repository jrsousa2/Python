rem ESSE SCRIPT IRA CRIAR UMA PLANILHA EXCEL COM TODOS OS ARQUIVOS
rem DE UMA PLAYLIST
rem Para trazer as tags adicionais USAR AS OPCOES ABAIXO
rem Art fields (-A): Covers e formato 
rem Hex fields (-H): Art size, Art size in Hexdec and art_chars (Bytes) (demorado)
rem Dim fields (-D): pega height, width and art size fields
rem Sort fields (-S): pega sort fields
rem Sort fields (-C): pega field counts

D:
cd D:\Python\Scripts
cscript Excel.vbs -a -c

