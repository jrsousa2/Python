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
Dim fso 
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
Dim ExtraFields
Dim Args
Dim Arg
Dim ExtArray(4)
Dim Art_Size
Dim Art_Hei
Dim Art_Wid
Dim Art_filename
Dim Formato
Dim Test

'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet
Dim objWorkbook

Set fso = CreateObject("Scripting.FileSystemObject")

ExtArray(0) = "unk"
ExtArray(1) = "jpg"
ExtArray(2) = "png"
ExtArray(3) = "bmp"

ExtraFields = False

Set Args = WScript.Arguments
'Scan command line arguments
For Each arg in args 
  'Is it a flag?
  If Instr(1,arg,"-",1) = 1 or Instr(1,arg,"/", 1) = 1 Then
    'Check for list flag
    If UCase(arg) = "-Y" or UCase(arg) = "/Y" then
       ExtraFields = True
    End If
  End If
Next

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

objExcel.Cells(1, 1) = "Art"
objExcel.Cells(1, 2) = "AA"
objExcel.Cells(1, 3) = "Title"
objExcel.Cells(1, 4) = "Year"
objExcel.Cells(1, 5) = "Album"
objExcel.Cells(1, 6) = "Location"
objExcel.Cells(1, 7) = "Covers"
objExcel.Cells(1, 8) = "Bitrate"
objExcel.Cells(1, 9) = "Length"
objExcel.Cells(1, 10) = "Rating"
objExcel.Cells(1, 11) = "Genre"

If ExtraFields Then
   objExcel.Cells(1, 12) = "Art_Size"
   objExcel.Cells(1, 13) = "Format"
   objExcel.Cells(1, 14) = "Hei"
   objExcel.Cells(1, 15) = "Wid"
   
   'objExcel.Cells(1, 14) = "PlayedCount"
   'objExcel.Cells(1, 15) = "SkippedCount"
   'objExcel.Cells(1, 16) = "Date_added"
   'objExcel.Cells(1, 17) = "Grouping"
   'objExcel.Cells(1, 18) = "Art_Sort"
   'objExcel.Cells(1, 19) = "AA_Sort"
End If

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

On Error Resume Next
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
		'result = 26
				
 		listarray = split(result, ",")
 		For k = 0 to UBound(listarray)
 			num = listarray(k)
 		   	Set playlist = playlists.Item(num)
 		   	playlistName = playlist.Name
 		   	Wscript.Echo ""
            Wscript.Echo chr(9) & "Extra fields: " & ExtraFields
 		   	Wscript.Echo chr(9) & "Processing playlist " & num & ": " & playlistName
 		   	
 		   	Set tracks = playlist.Tracks
 		   	numtracks = tracks.Count
 		   	Wscript.Echo chr(9) & "tracks: " & numtracks
 		   	NumRows = 1

 		   	For m = 1 to numtracks
 		   		If m > tracks.Count Then Exit For
 		   		Set track = tracks.Item(m)
 		   		
 		   		If track.Kind = 1 Then
 		   		   Set Artobj = track.Artwork
 		   		   Artobj_Count = Artobj.Count
 		   		   Art_size = 0
 		   		   NumRows = NumRows + 1
 		   		   If Artobj.Count>0 And ExtraFields And FSO.FileExists(track.Location) Then
 		   		      WScript.Echo "File " & NumRows & ": " & track.Location
                      'Wscript.Echo "Exporting cover"
                      Formato = Artobj.Item(1).Format
                      'Wscript.Echo "Format is " & Formato
                      Art_filename = "D:\Z-Covers\Exported_from_iTunes\check_size" & "." & ExtArray(Formato)
                      Artobj.Item(1).SaveArtworkToFile(Art_filename)
                      If FSO.FileExists(Art_filename) And (ExtArray(Formato)="jpg" or ExtArray(Formato)="png") Then
                         Set objFile = FSO.GetFile(Art_filename)
                         Art_size = objFile.Size
                         Set objFile = Nothing
                         Set objLP = loadpicture(Art_filename)
                         Art_Wid = round(objLP.width / 26.4583)
                         Art_Hei = round(objLP.height / 26.4583)
                         Set objLP = Nothing
                         'wscript.echo "File Size: " &  & "Kb"
                      End If
                   End If
 		   		   'If TrackPath = "" Then 
 		   		   '   Artobj_Count = 0
 		   		   'End If
 		   			
 		   		   If track.Year <> Empty Then
 		   		      songYear = track.Year
 		   		   Else songYear = Empty
 		   		   End If

 		   		   'COLUNAS=ARTIST,ALBUM ARTIST,NAME,ALBUM,YEAR,LOCATION,HASART
 		   		   
                   objExcel.Cells(NumRows, 1) = track.Artist
                   objExcel.Cells(NumRows, 2) = track.AlbumArtist
                   objExcel.Cells(NumRows, 3) = track.Name
                   objExcel.Cells(NumRows, 4) = songYear
                   objExcel.Cells(NumRows, 5) = track.Album
                   objExcel.Cells(NumRows, 6) = track.Location
                   objExcel.Cells(NumRows, 7) = Artobj_Count
                   objExcel.Cells(NumRows, 8) = track.Bitrate
                   objExcel.Cells(NumRows, 9) = track.Time
                   objExcel.Cells(NumRows, 10) = track.Rating
                   objExcel.Cells(NumRows, 11) = track.Genre
                   If ExtraFields Then
                      objExcel.Cells(NumRows, 12) = Art_size
                      objExcel.Cells(NumRows, 13) = ExtArray(Formato)
                      objExcel.Cells(NumRows, 14) = Art_Hei
                      objExcel.Cells(NumRows, 15) = Art_Wid
                      
                      'objExcel.Cells(NumRows, 14) = track.PlayedCount
                      'objExcel.Cells(NumRows, 15) = track.Skippedcount
                      'objExcel.Cells(NumRows, 16) = track.dateadded
                      'objExcel.Cells(NumRows, 17) = track.grouping
                      'objExcel.Cells(NumRows, 18) = track.SortArtist
                      'objExcel.Cells(NumRows, 19) = track.SortAlbumArtist
                   End If

                   'If (numrows - 100*(numrows\100)) = 0 then WScript.Echo "Row. no: " & NumRows
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
'result = "all"
'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
my_sheet = "D:\iTunes\Excel\"& result &".xlsx"
objWorkbook.SaveAs(my_sheet)

'objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close

objExcel.Quit
