Sub JPGExtract (strSourceFile)
'remove duplicate space from the Target file name
 
'For i = 1 to 2000
'        strTargetFile = Replace(strTargetFile, "  ", " ")
'   next
 
With CreateObject("ADODB.Stream")
             'Binary stream    
         .Type = 1
         .Open
         .LoadFromFile strSourceFile
         .Position = 0
             'get the whole binary
         arrBuffer = .Read(.Size) 
             'convert byte() to char()	
         strBuffer = MidB(arrBuffer, 1, .Size) 
             'get 50 49 43 "PIC" token position to skip extraneous bytes	
         lngPrePos = InstrB(1, arrBuffer, ChrB(&H50) & ChrB(&H49) & ChrB(&H43), 0) 
             '"PIC" token not found - searching from start
         If lngPrePos = 0 Then lngPrePos = 1: exit sub 
    'get FF D8 token position
         lngPosBeg = InstrB(lngPrePos, arrBuffer, ChrB(&HFF) & ChrB(&HD8), 0)
             'get FF D9 token position	
         lngPosEnd = InstrB(lngPosBeg, arrBuffer, ChrB(&HFF) & ChrB(&HD9), 0)
             'move stream position to FF D8	
         Wscript.Echo "Size: " & lngPosEnd - lngPosBeg + 1
         .Position = lngPosBeg - 1 
             'assign to buffer the portion of binary from FF D8 up to FF D9 tokens inclusive	
         'arrBuffer = .Read(lngPosEnd - lngPosBeg + 1) 
         
End With
 
 'With CreateObject("ADODB.Stream")
         ' Binary stream	
 '        .Type = 1 ' Binary stream
  '       .Open
   '      .Position = 0
    '     .Write arrBuffer
     '    .SaveToFile ".\ART\"&strTargetFile, 2
 'End With
End Sub

JPGExtract "D:\mp3\b\BW Stevenson - My Maria.mp3"