'======================
'YEAR
'REMOVES INVALID YEARS, SUCH AS 9999
'ESSE SCRIPT CORRIGE A TAG YEAR DE FAIXAS QUE CONTENHAM VALORES
'EXTREMOS, COMO MENOS DO QUE 1900.
'QUANDO ACHA ESSES VALORES EXTREMOS, APENAS LIMPA O A TAG YEAR

Option Explicit

Dim TrackPath        ' The path to the track
Dim ArtPath	         ' The path to the artwork
Dim numtracks
Dim m
Dim Desc
Dim sources
Dim source
Dim playlists
Dim playlist
Dim playlistName
Dim f                ' A file object.
Dim j
Dim c
Dim iTunesApp        ' iTunes.Application object used to access the iTunes application.
Dim tracks           ' The tracks collection object of the Library object. 
Dim i                ' A counter variable.
Dim songName
Dim artist
Dim result
Dim listarray
Dim num
Dim k
Dim match_row
Dim track
Dim Artobj
Dim Art
Dim ArtDir
Dim TrackAlbum
Dim TrackYear
Dim fso 
Dim NumFiles

'My vars - Jose's
Dim Artobj_Count


Set fso = CreateObject("Scripting.FileSystemObject")


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
		'result = 9
				
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
 		   	
 		   	'INITIALIZE THE FILE COUNTER
 		   	NumFiles = 0

 		   	For m = 1 to numtracks
 		   		If m > tracks.Count Then Exit For
 		   		
 		   		Set track = tracks.Item(m)
 		   		If track.Kind = 1 Then
 		   		   'songName = track.Name
 		   		   'artist = track.Artist
 		   		   'TrackPath = track.Location
                   'TrackAlbum = track.Album
                   TrackYear = track.Year
                   
                   If TrackYear < 1900 And TrackYear > 0 Then 
                   NumFiles = NumFiles+1
                   track.Year = Empty
                   End If
                   
                   WScript.Echo "Arq. no: " & m & " Year=" & TrackYear & " Cleared Year: " & NumFiles               
                End If
 		    Next
 	    Next
	End If
Next


