'Allows a batch to Run in invisible mode

Set WshShell = CreateObject("WScript.Shell" )
WshShell.Run chr(34) & "d:\freedb\append.bat" & Chr(34), 0
Set WshShell = Nothing
