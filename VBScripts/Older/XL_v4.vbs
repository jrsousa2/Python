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
Dim Art_Filename
Dim Formato

'LEITURA DAS TAGS
Dim Art_Size
Dim strHex
Dim Hex_Size

'LEITURA DIRETA DA ARTWORK
Dim Art_Size2
Dim Art_Hei
Dim Art_Wid


'PARAMETROS DE CHAMADA DO PROGRAMA
Dim Art_Fields
Dim Sort_Fields
Dim Dim_Fields
Dim Hex_Fields

Dim Args
Dim Arg
Dim ExtArray(4)

'INCREMENTOS PARA OS NUMEROS DAS COLUNAS
Dim Marca
Dim Marca_Hex
Dim Marca_Dim
Dim Marca_Sort

'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet
Dim objWorkbook

'FUNCTION
Sub CoverSize (ByVal strSourceFile, ByVal Format_pmt, ByRef Artsize_pmt, ByRef Hex_Size_pmt, ByRef strHex_Pmt)
'remove duplicate space from the Target file name
Dim strBuffer
Dim arrBuffer
Dim HeaderPos
Dim HeaderIni
Dim HeaderFim
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
Hex_Size_Pmt = Mid(Aux,3,2) & Mid(Aux,1,2)
'WScript.Echo "1) i=" & 1 & ",Hex: " & Aux & " tam: " & Len(Aux)
For i = 2 To Len(strBuffer) Step 1
    Aux = Right("0000" & Hex(AscW(Mid(strBuffer,i,1))), 4) 
    Hex_Size_Pmt = Hex_Size_Pmt & Mid(Aux,3,2) & Mid(Aux,1,2)
    'WScript.Echo "1) i=" & i & " ,Unicode: " & Mid(strBuffer,i,1) & ",Ascii: " & AscW(Mid(strBuffer,i,1)) & ",Hex: " & Aux & " tam: " & Len(Aux)
Next
'WScript.Echo "Hex rep: " & strHEX_Pmt & " " & CLng("&H" & strHEX_Pmt)
Artsize_pmt = CLng("&H" & Hex_Size_Pmt)-14

'GRAB A PIECE OF THE IMAGE
strHEX_Pmt = ""
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
Fim = Inicio+CLng("&H" & Hex_Size_Pmt)

'WScript.Echo "Size: " & Artsize_pmt

'Saves the Hex representation
strBuffer = MidB(arrBuffer,Inicio,80)
strHEX_Pmt = Hex(Ascw(Mid(strBuffer,1,1)))
For i = 2 To Len(strBuffer) Step 1
    strHEX_Pmt = strHEX_Pmt & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
	'WScript.Echo Mid(strBuffer,i,1),Hex(Ascw(Mid(strBuffer,i,1)))
Next

strBuffer = MidB(arrBuffer,(Inicio+Fim)\2,80)
For i = 1 To Len(strBuffer) Step 1
    strHEX_Pmt = strHEX_Pmt & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
Next

'THIS IS FAILING JUST FOR ONE PAIR OF COVERS
strBuffer = MidB(arrBuffer,Fim-200,80)
For i = 1 To Len(strBuffer) Step 1
    strHEX_Pmt = strHEX_Pmt & "-" & Hex(Ascw(Mid(strBuffer,i,1)))
Next
End If

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

Art_Fields = False
Hex_Fields = False
Dim_Fields = False
Sort_Fields = False

Set Args = WScript.Arguments
'Scan command line arguments
For Each Arg in Args 
  'Is it a flag?
  If Instr(1,arg,"-",1) = 1 or Instr(1,arg,"/", 1) = 1 Then
    'Check for list flag
    If UCase(arg) = "-A" or UCase(arg) = "/A" then
       Art_Fields = True
    End If
    If UCase(arg) = "-H" or UCase(arg) = "/H" then
       Hex_Fields = True
    End If
    If UCase(arg) = "-D" or UCase(arg) = "/D" then
       Dim_Fields = True
    End If
    If UCase(arg) = "-S" or UCase(arg) = "/S" then
       Sort_Fields = True
    End If
  End If
Next

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

Marca = 10

objExcel.Cells(1, 1) = "Art"
objExcel.Cells(1, 2) = "Title"
objExcel.Cells(1, 3) = "AA"
objExcel.Cells(1, 4) = "Album"
objExcel.Cells(1, 5) = "Year"
objExcel.Cells(1, 6) = "Location"
objExcel.Cells(1, 7) = "Bitrate"
objExcel.Cells(1, 8) = "Length"
objExcel.Cells(1, 9) = "Rating"
objExcel.Cells(1, 10) = "Genre"

If Art_Fields Then
   objExcel.Cells(1, 11) = "Covers"
   objExcel.Cells(1, 12) = "Format"
   Marca = Marca+2
End If
   
If Hex_Fields Then 
   Marca_Hex = Marca  
   objExcel.Cells(1, Marca_Hex+1) = "Art_Size"
   objExcel.Cells(1, Marca_Hex+2) = "Hex_Size"
   objExcel.Cells(1, Marca_Hex+3) = "Bytes"
   Marca = Marca+3
End If

If Dim_Fields Then
   Marca_Dim = Marca
   objExcel.Cells(1, Marca_Dim+1) = "Hei"
   objExcel.Cells(1, Marca_Dim+2) = "Wid"
   objExcel.Cells(1, Marca_Dim+3) = "Art_Size2"
   Marca = Marca+3
End If

If Sort_Fields Then
   Marca_Sort = Marca
   objExcel.Cells(1, Marca_Sort+1) = "Art_Sort"
   objExcel.Cells(1, Marca_Sort+2) = "AA_Sort"
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
                        Wscript.Echo chr(9) & "Fields: Art: " & Art_Fields & ", Hex: " & Hex_Fields & ", Dim: " & Dim_Fields & ", Sort: " & Sort_Fields
 		   	Wscript.Echo chr(9) & "Processing playlist " & Num & ": " & playlistName

                       Wscript.Echo ""
                       Wscript.Echo ""

 		   	Set tracks = playlist.Tracks
 		   	numtracks = tracks.Count
 		   	Wscript.Echo chr(9) & "tracks: " & numtracks
 		   	NumRows = 1
             
 		   	For m = 1 to numtracks
 		   		If m > tracks.Count Then Exit For
 		   		Set track = tracks.Item(m)
 		   		
 		   		If track.Kind = 1 Then
 		   		   NumRows = NumRows + 1
 		   		   
 		   		   If Art_Fields Or Hex_Fields Or Dim_Fields Then
 		   		      Formato = Empty
 		   		      Set Artobj = track.Artwork
 		   		      Artobj_Count = Artobj.Count
 		   		      If Artobj_Count>0 And FSO.FileExists(track.Location) Then
                         Formato = ExtArray(Artobj.Item(1).Format)
                      End If  
                   End If   
                   
 		   		   If Hex_Fields Then
 		   		      Art_size = Empty
 		   		      Hex_Size = Empty
 		   		      strHex = Empty
                      If Formato="jpg" Or Formato="png" Then
                         CoverSize track.Location, Formato, Art_Size, Hex_Size, strHex
                      End If
                   End If                      

                   'ESSA INDENTACAO ESTA CORRETA
                   'AQUI PRECISA VER SE FORMATO TEM QUE SER LIDO OU SE PODE SER QQ UM
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
                   objExcel.Cells(NumRows, 10) = track.Genre

                   If Art_Fields Then
                      objExcel.Cells(NumRows, 11) = Artobj_Count
                      objExcel.Cells(NumRows, 12) = Formato
                   End If   

                   If Hex_Fields Then
                      objExcel.Cells(NumRows, Marca_Hex+1) = Art_size
                      objExcel.Cells(NumRows, Marca_Hex+2) = Hex_Size 
                      objExcel.Cells(NumRows, Marca_Hex+3) = strHex
                   End If

                   'O ABAIXO VEM DA LEITURA DIRETA DO ARQUIVO
                   If Dim_Fields Then
                      objExcel.Cells(NumRows, Marca_Dim+1) = Art_Hei
                      objExcel.Cells(NumRows, Marca_Dim+2) = Art_Wid
                      objExcel.Cells(NumRows, Marca_Dim+3) = Art_Size2
                   End If

                   If Sort_Fields Then
                      objExcel.Cells(NumRows, Marca_Sort+1) = track.SortArtist
                      objExcel.Cells(NumRows, Marca_Sort+2) = track.SortAlbumArtist
                      'objExcel.Cells(NumRows, 14) = track.PlayedCount
                      'objExcel.Cells(NumRows, 15) = track.Skippedcount
                      'objExcel.Cells(NumRows, 16) = track.dateadded
                      'objExcel.Cells(NumRows, 17) = track.grouping
                   End If

                   If (numrows - 100*(numrows\100)) = 0 Then WScript.Echo "Row. no: " & NumRows
                   End If
 		    Next
 	    Next
	End If
Next

'END OF THE SHEET EDITING, NOW SAVE THE FILE
'SAVE FILE
objExcel.DisplayAlerts = False

Wscript.StdOut.Write "Output name (file will be saved to D:\iTunes\Excel\all.xls): "
result = WScript.StdIn.ReadLine
'result = "xxx"
'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
my_sheet = "D:\iTunes\Excel\"& result &".xlsx"
objWorkbook.SaveAs(my_sheet)

'objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close
objExcel.Quit
