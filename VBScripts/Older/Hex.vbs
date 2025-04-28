Set fso = CreateObject("scripting.filesystemobject")
 
text = fso.OpenTextFile("D:\Python\test.txt",1,False,-1).ReadAll  
' forreading, don't create, unicode
 
WScript.Echo "Incorrect simplistic read - gives incorrect ascii codes for unicode chars"
 
For i = 1 To Len(text) Step 1
	WScript.Echo Mid(text,i,1), Hex(Asc(Mid(text,i,1)))
Next
 
WScript.Echo "correct read - gives correct ascii codes for unicode chars using ASCW"
 
For i = 1 To Len(text) Step 1
	WScript.Echo Mid(text,i,1), Hex(Ascw(Mid(text,i,1)))
Next
 
WScript.Echo "hard code to Interpret as Unicode by reading double byte by double byte"
 
For i = 1 To Lenb(text) Step 2
	WScript.Echo Midb(text,i,2), Hex(AscW(Midb(text,i,2)))
Next
 
WScript.Echo "simply reading each unicode char a byte at a time - notice we have to display the 2nd byte first to match the example above"
 
For i = 1 To Lenb(text) Step 2
	WScript.Echo Hex(ascb(Midb(text,i+1,1))),Hex(ascb(Midb(text,i,1)))
next