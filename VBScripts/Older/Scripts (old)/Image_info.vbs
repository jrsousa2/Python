Const DIMENSIONS = 31
CONST WIDTH  = 162
CONST HEIGTH = 164
Const Size = 1
Const FileType = 2

'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet
Dim objWorkbook

Set fso = CreateObject("Scripting.FileSystemObject")
Set oShell  = CreateObject("Shell.Application")

Wscript.Echo ""
Wscript.StdOut.Write "Enter directory to read images info from: "
Diret = WScript.StdIn.ReadLine

Set directorio = fso.GetFolder(Diret).Files
Set oFolder = oShell.Namespace(Diret)

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

objExcel.Cells(1, 1) = "Location"
objExcel.Cells(1, 2) = "Height"
objExcel.Cells(1, 3) = "Width"
objExcel.Cells(1, 4) = "Size"
objExcel.Cells(1, 5) = "Type"


i=1
For Each file in directorio
i=i+1

Location = File.path
Nome = File.name
Set oFile   = oFolder.ParseName(Nome)

'strDimensions = oFolder.GetDetailsOf(oFile, DIMENSIONS)    
strWidth  = oFolder.GetDetailsOf(oFile, WIDTH)
strHeigth = oFolder.GetDetailsOf(oFile, HEIGTH)
strType = File.Type
strSize = File.size

objExcel.Cells(i, 1) = location
objExcel.Cells(i, 2) = strHeigth
objExcel.Cells(i, 3) = strWidth
objExcel.Cells(i, 4) = strSize
objExcel.Cells(i, 5) = strType

if (i - 100*(i\100)) = 0 then WScript.Echo "File no: " & i

Next

'SAVE FILE
objExcel.DisplayAlerts = False

Wscript.StdOut.Write "Output name (file will be saved to D:\Python\Excel\): "
result = WScript.StdIn.ReadLine
'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
my_sheet = "D:\Python\Excel\"& result &".xls"
objWorkbook.SaveAs(my_sheet)

'objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close

objExcel.Quit
