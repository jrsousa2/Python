rem ESSE SCRIPT IRA CRIAR UMA PLANILHA EXCEL COM TODOS OS ARQUIVOS
rem DE UMA PLAYLIST
rem PARAMETROS VAO DEPOIS DA CHAMADA AO SCRIPT
rem Para trazer as tags adicionais USAR AS OPCOES ABAIXO
rem Art fields (-A): pega art size, formato and art_chars
rem Hex fields (-H): pega Hex fields (demorado)
rem Dim fields (-D): pega height, width and art size+art fields
rem Sort fields (-S): pega sort fields
rem Sort fields (-X): pega Date fields

D:
cd D:\Python\Scripts
cscript Excel.vbs -X

