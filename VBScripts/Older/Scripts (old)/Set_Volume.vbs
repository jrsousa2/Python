'TESTE PARA SETAR VOLUME A 0

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
Dim track
Dim fso 
Dim num
Dim NumFiles 'No of files who missing tag were filled
Dim numtracks 'Counts total tracks in playlist

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
		WScript.StdOut.Write "Enter comma-separated lists to process: "
		result = WScript.StdIn.ReadLine
		'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
		'result = 15
		
	
				
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
 		   	NumFiles = 0
            
 		   	For m = 1 to numtracks
 		   		If m > tracks.Count Then Exit For
 		   		Set track = tracks.Item(m)
                                TrackPath = track.Location
                                track.VolumeAdjustment = 0
                                Wscript.Echo "Track: " & m & "-" & TrackPath
 		   		   
 		        Next
 	        Next
	End If
Next

Wscript.Echo "Number of files changed: " & NumFiles
