'=========================================================================
'ESSE SCRIPT ME DA O ARTISTSORT AND ALBUMARTISTSORT

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
              
Dim result
Dim listarray
Dim match_row
Dim track
Dim songYear
Dim fso 
Dim num
Dim NumRows
Dim numtracks
'ARTWORK VARIABLES
Dim Artobj
Dim Artobj_Count


'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet
Dim objWorkbook

Set fso = CreateObject("Scripting.FileSystemObject")

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

objExcel.Cells(1, 1) = "Artist"
objExcel.Cells(1, 2) = "Album_Artist"
objExcel.Cells(1, 3) = "Title"
objExcel.Cells(1, 4) = "Year"
objExcel.Cells(1, 5) = "Album"
objExcel.Cells(1, 6) = "Location"
objExcel.Cells(1, 7) = "Covers"
objExcel.Cells(1, 8) = "Bitrate"
objExcel.Cells(1, 9) = "Length"
objExcel.Cells(1, 10) = "Rating"
objExcel.Cells(1, 11) = "sort_artist"
objExcel.Cells(1, 12) = "sort_albumart"

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

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
 		   		   'If TrackPath = "" Then 
 		   		   '   Artobj_Count = 0
 		   		   'End If
 		   			
 		   		   NumRows = NumRows + 1

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
                   objExcel.Cells(NumRows, 11) = track.sortartist
                   objExcel.Cells(NumRows, 12) = track.sortalbumartist
                   if (numrows - 100*(numrows\100)) = 0 then WScript.Echo "Row. no: " & NumRows
                   End If
 		    Next
 	    Next
	End If
Next

'END OF THE SHEET EDITING, NOW SAVE THE FILE
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
