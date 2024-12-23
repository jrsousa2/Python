Set fso = CreateObject("scripting.filesystemobject")
 
strHex = "0000E66E"
Artsize_pmt = CLng("&H" & strHex)-14
WScript.Echo "Hex: " & strHex & ", valor: " & Artsize_pmt
 