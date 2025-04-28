'=========================================================================
'CREATE AN XL SHEET FROM A PLAYLIST
'CREATES AN EXCEL SHEET WITH ALL THE FILES IN A PLAYLIST,
'LISTING SONG NAME, ALBUM, YEAR, ETC.
'IN THIS CODE, I SAVE THE ART TO A FILE AND THEN CHECK ITS SIZE
'==========================================================================

Option Explicit

Dim TrackPath        ' The path to the track
Dim sources
Dim source
Dim playlists
Dim playlist
Dim playlistName
Dim m
Dim i  
Dim j
Dim k

Dim iTunesApp        ' iTunes.Application object used to access the iTunes application.
Dim tracks           ' The tracks collection object of the Library object. 
Dim FSO 
Dim objFile
Dim objLP
              
Dim result
Dim listarray
Dim match_row
Dim track
Dim songYear
Dim num
Dim NumRows
Dim numtracks
'ARTWORK VARIABLES
Dim Artobj
Dim Artobj_Count
Dim Simple_Fields
Dim Art_Fields
Dim Sort_Fields
Dim Dim_Fields
Dim Marca
Dim Args
Dim Arg
Dim ExtArray(4)
Dim Art_Size
Dim Art_Size2
Dim Art_Hei
Dim Art_Wid
Dim Art_Filename
Dim Formato
Dim Art_chars

'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet
Dim objWorkbook

'FUNCTION
Sub CoverSize (ByVal Row, ByVal strSourceFile, ByVal Format_pmt, ByRef Artsize_pmt)
'remove duplicate space from the Target file name
Dim strBuffer
Dim arrBuffer
Dim HeaderPos
Dim HeaderIni
Dim HeaderFim
Dim strHex
Dim Hex_Size
Dim Aux
Dim Tam
Dim Inicio
Dim Fim
Dim BS
Dim i
Dim j

Set BS = CreateObject("ADODB.Stream")

BS.Type = 1
BS.Open
BS.LoadFromFile strSourceFile
BS.Position = 0
arrBuffer = BS.Read(BS.Size) 
'strBuffer = MidB(arrBuffer, 1, .Size) 
'Ler entre Apic (41 50 49 43) e Image (69 6D 61 67 65), depois converter pra decimal
HeaderIni = InstrB(1, arrBuffer, ChrB(&H41) & ChrB(&H50) & ChrB(&H49) & ChrB(&H43), 0)+4 'APIC Header
HeaderFim = InstrB(HeaderIni, arrBuffer, ChrB(&H69) & ChrB(&H6D) & ChrB(&H61) & ChrB(&H67), 0)-5
Tam= HeaderFim-HeaderIni
'WScript.Echo "Header Ini: " & HeaderIni & " Fim: " & HeaderFim & " ,Tam: " & Tam

strBuffer = MidB(arrBuffer,HeaderIni,2*Tam)
Aux = Right("0000" & Hex(AscW(Mid(strBuffer,1,1))), 4)
Hex_Size = Mid(Aux,3,2) & Mid(Aux,1,2)
'WScript.Echo "1) i=" & 1 & ",Hex: " & Aux & " tam: " & Len(Aux)
For i = 2 To Len(strBuffer) Step 1
    Aux = Right("0000" & Hex(AscW(Mid(strBuffer,i,1))), 4) 
    Hex_Size = Hex_Size & Mid(Aux,3,2) & Mid(Aux,1,2)
    'WScript.Echo "1) i=" & i & " ,Unicode: " & Mid(strBuffer,i,1) & ",Ascii: " & AscW(Mid(strBuffer,i,1)) & ",Hex: " & Aux & " tam: " & Len(Aux)
Next
'WScript.Echo "Hex rep: " & strHex & " " & CLng("&H" & strHex)
Artsize_pmt = CLng("&H" & Hex_Size)-14

'GRAB A PIECE OF THE IMAGE
strHex = ""
If True Then
If HeaderIni = 0 Then HeaderIni = 1: exit sub 'PIC not found searching from start
If Format_pmt = "jpg" Then
   Inicio = InstrB(HeaderIni, arrBuffer, ChrB(&HFF) & ChrB(&HD8), 0)-1 'get FF D8 token position
   'Fim = InstrB(Artsize_pmt-5, arrBuffer, ChrB(&HFF) & ChrB(&HD9), 0) 'get FF D9 token position
   'Artsize_pmt = Fim-Inicio+1
Else
   Artsize_pmt = Artsize_pmt+1
   Inicio = InstrB(HeaderIni, arrBuffer, ChrB(&H89) & ChrB(&H50) & ChrB(&H4E), 0)-1 'get 89 50 4E token position
End If
'THE BELOW IS JUST FOR THE PURPOSE OF CREATING THE BYTE STRING 
Fim = Inicio+CLng("&H" & Hex_Size)

'WScript.Echo "Size: " & Artsize_pmt

'Saves the Hex representation
strBuffer = MidB(arrBuffer,Inicio,80)
strHex = Hex(Ascw(Mid(strBuffer,1,1)))
For i = 2 To Len(strBuffer) Step 1
    strHex = strHex & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
	'WScript.Echo Mid(strBuffer,i,1),Hex(Ascw(Mid(strBuffer,i,1)))
Next

strBuffer = MidB(arrBuffer,(Inicio+Fim)\2,80)
For i = 1 To Len(strBuffer) Step 1
    strHex = strHex & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
Next

'THIS IS FAILING JUST FOR ONE PAIR OF COVERS
strBuffer = MidB(arrBuffer,Fim-200,80)
For i = 1 To Len(strBuffer) Step 1
    strHex = strHex & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
Next
End If

objExcel.Cells(Row,14) = strHex
objExcel.Cells(Row,15) = Hex_Size
End Sub
'END OF FUNCTION
'END OF FUNCTION
'END OF FUNCTION


'MAIN PROGRAM
'MAIN PROGRAM
'MAIN PROGRAM
'MAIN PROGRAM
Set fso = CreateObject("Scripting.FileSystemObject")

ExtArray(0) = "unk"
ExtArray(1) = "jpg"
ExtArray(2) = "png"
ExtArray(3) = "bmp"

Simple_Fields = False
Art_Fields = False
Sort_Fields = False
Dim_Fields = False

Set Args = WScript.Arguments
'Scan command line arguments
For Each arg in args 
  'Is it a flag?
  If Instr(1,arg,"-",1) = 1 or Instr(1,arg,"/", 1) = 1 Then
    'Check for list flag
    If UCase(arg) = "-Y" or UCase(arg) = "/Y" then
       Art_Fields = True
    End If
    If UCase(arg) = "-S" or UCase(arg) = "/S" then
       Simple_Fields = True
    End If
    If UCase(arg) = "-N" or UCase(arg) = "/N" then
       Sort_Fields = True
    End If
    If UCase(arg) = "-A" or UCase(arg) = "/A" then
       Art_Fields = True
       Dim_Fields = True
    End If
  End If
Next

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

Marca=0
objExcel.Cells(1, 1) = "Art"
objExcel.Cells(1, 2) = "Title"
objExcel.Cells(1, 3) = "AA"
objExcel.Cells(1, 4) = "Album"
objExcel.Cells(1, 5) = "Year"
objExcel.Cells(1, 6) = "Location"
objExcel.Cells(1, 7) = "Bitrate"
objExcel.Cells(1, 8) = "Length"
objExcel.Cells(1, 9) = "Rating"

If Not Simple_Fields Then
   Marca=Marca+2
   objExcel.Cells(1, 10) = "Genre"
   objExcel.Cells(1, 11) = "Covers"
End If

If Art_Fields Then
   objExcel.Cells(1, 12) = "Art_Size"
   objExcel.Cells(1, 13) = "Format"
   objExcel.Cells(1, 14) = "Bytes"
   objExcel.Cells(1, 15) = "Hex_Size"
End If

If Dim_Fields Then
   objExcel.Cells(1, 16) = "Hei"
   objExcel.Cells(1, 17) = "Wid"
   objExcel.Cells(1, 18) = "Art_Size2"
End If

If Sort_Fields Then
   objExcel.Cells(1, 12) = "Art_Sort"
   objExcel.Cells(1, 13) = "AA_Sort"
   'objExcel.Cells(1, 14) = "PlayedCount"
   'objExcel.Cells(1, 15) = "SkippedCount"
   'objExcel.Cells(1, 16) = "Date_added"
   'objExcel.Cells(1, 17) = "Grouping"
End If

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

If Art_Fields Then On Error Resume Next

For i = 1 to sources.Count
	Set source = sources.Item(i)
	
	If source.Kind = 1 Then
		Set playlists = source.Playlists
		Wscript.Echo "Select from the following playlists" & chr(13) & chr(10)
		Wscript.Echo "Number of playlists: " & playlists.Count
		For j = 1 to playlists.Count
			Set playlist = playlists.Item(j)
			playlistName = playlist.Name
			Wscript.Echo j & ": " & playlistName
		Next
		Wscript.Echo ""
		Wscript.StdOut.Write "Enter comma-separated lists to process: "
		result = WScript.StdIn.ReadLine
		'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
		'result = 41
				
 		listarray = split(result, ",")
 		For k = 0 to UBound(listarray)
 			num = listarray(k)
 		   	Set playlist = playlists.Item(num)
 		   	playlistName = playlist.Name
 		   	Wscript.Echo ""
                        Wscript.Echo chr(9) & "Extra fields, art: " & Art_Fields & ", sort: " & Sort_Fields & ", dim: " & Dim_Fields
 		   	Wscript.Echo chr(9) & "Processing playlist " & Num & ": " & playlistName
 		   	
 		   	Set tracks = playlist.Tracks
 		   	numtracks = tracks.Count
 		   	Wscript.Echo chr(9) & "tracks: " & numtracks
 		   	NumRows = 1
             
 		   	For m = 1 to numtracks
 		   		If m > tracks.Count Then Exit For
 		   		Set track = tracks.Item(m)
 		   		
 		   		If track.Kind = 1 Then
 		   		   NumRows = NumRows + 1
 		   		   
 		   		   If Not Simple_Fields Then
 		   		      Art_size = Empty
 		   		      Formato = Empty
 		   		      Set Artobj = track.Artwork
 		   		      Artobj_Count = Artobj.Count
 		   		      If Artobj_Count>0 And Art_Fields And FSO.FileExists(track.Location) Then
                                         Formato = ExtArray(Artobj.Item(1).Format)
                                      If Formato="jpg" Or Formato="png" Then
                                         CoverSize NumRows, track.Location, Formato, Art_size
                                   End If

                      'ESSA INDENTACAO ESTA CORRETA
                      If Dim_Fields Then
                         Art_Size2 = Empty
                         Art_Wid = Empty
                         Art_Hei = Empty
 		   	 WScript.Echo "File " & NumRows-1 & ": " & track.Location
                         Art_Filename = "D:\Z-Covers\Check_size" & "." & Formato
                         Artobj.Item(1).SaveArtworkToFile(Art_Filename)
                         If FSO.FileExists(Art_filename) And (Formato="jpg" or Formato="png") Then
                            Set objFile = FSO.GetFile(Art_filename)
                            Art_Size2 = objFile.Size
                            Set objFile = Nothing
                            Set objLP = loadpicture(Art_Filename)
                            Art_Wid = round(objLP.width/26.4583)
                            Art_Hei = round(objLP.height/26.4583)
                            Set objLP = Nothing
                         End If
                      End If
                   End If
                   End if

 		   If track.Year <> Empty Then
 		      songYear = track.Year
 		   Else songYear = Empty
 		   End If

 		   'COLUNAS=ARTIST,ALBUM ARTIST,NAME,ALBUM,YEAR,LOCATION,HASART
                   objExcel.Cells(NumRows, 1) = track.Artist
                   objExcel.Cells(NumRows, 2) = track.Name
                   objExcel.Cells(NumRows, 3) = track.AlbumArtist
                   objExcel.Cells(NumRows, 4) = track.Album
                   objExcel.Cells(NumRows, 5) = songYear
                   objExcel.Cells(NumRows, 6) = track.Location
                   objExcel.Cells(NumRows, 7) = track.Bitrate
                   objExcel.Cells(NumRows, 8) = track.Time
                   objExcel.Cells(NumRows, 9) = track.Rating
                   If Not Simple_Fields Then
                      objExcel.Cells(NumRows, 10) = track.Genre
                      objExcel.Cells(NumRows, 11) = Artobj_Count
                   End if
                   If Art_Fields Then
                      objExcel.Cells(NumRows, 12) = Art_size
                      objExcel.Cells(NumRows, 13) = Formato
                      'objExcel.Cells(NumRows, 14) = Art_chars
                   End If
                   'O ABAIXO VEM DA LEITURA DIRETA DO ARQUIVO
                   If Dim_Fields Then
                      objExcel.Cells(NumRows, 16) = Art_Hei
                      objExcel.Cells(NumRows, 17) = Art_Wid
                      objExcel.Cells(NumRows, 18) = Art_Size2
                   End If
                   If Sort_Fields Then
                      objExcel.Cells(NumRows, 12) = track.SortArtist
                      objExcel.Cells(NumRows, 13) = track.SortAlbumArtist
                      'objExcel.Cells(NumRows, 14) = track.PlayedCount
                      'objExcel.Cells(NumRows, 15) = track.Skippedcount
                      'objExcel.Cells(NumRows, 16) = track.dateadded
                      'objExcel.Cells(NumRows, 17) = track.grouping
                   End If

                   If (numrows - 100*(numrows\100)) = 0 then WScript.Echo "Row. no: " & NumRows
                   End If
 		    Next
 	    Next
	End If
Next

'END OF THE SHEET EDITING, NOW SAVE THE FILE
'SAVE FILE
objExcel.DisplayAlerts = False

Wscript.StdOut.Write "Output name (file will be saved to D:\Python\Excel\all.xls): "
result = WScript.StdIn.ReadLine
'result = "xxx"
'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
my_sheet = "D:\Python\Excel\"& result &".xlsx"
objWorkbook.SaveAs(my_sheet)

'objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close
objExcel.Quit
