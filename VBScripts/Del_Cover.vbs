'DELETES THE COVER OF FILES IN A PLAYLIST

Option Explicit

Dim TrackPath        ' The path to the track
Dim sources
Dim source
Dim playlists
Dim playlist
Dim playlistName
Dim List_pick
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
Dim NumFiles
Dim numtracks
'ARTWORK VARIABLES
Dim Artobj
Dim Art
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
            If playlistName="Dummy1" Then List_pick = j
			Wscript.Echo j & ": " & playlistName
		Next
		Wscript.Echo ""
		WScript.StdOut.Write "Enter comma-separated lists to process: "
		result = WScript.StdIn.ReadLine
		'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
		'result = List_pick
				
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
 		   	
 		   	'CONTROLE DE VERIFICACAO PARA NAO DELETAR CAPAS EM LISTAS ERRADAS
 		   	WScript.StdOut.Write chr(9) & "Hit enter to continue to delete"
		    WScript.StdIn.ReadLine
		    
 		   	NumFiles = 0
              
 		   	For m = 1 to numtracks
 		   	    'CODE WON'T EXECUTE IF MORE THAN 400 COVERS TO BE DELETED
 		   	    If numtracks>2900 Then Exit For
 		   		If m > tracks.Count Then Exit For
 		   		Set track = tracks.Item(m)
                
                On Error Resume Next		   		
 		   		If track.Kind = 1 Then
 		   		   Set Artobj = track.Artwork
 		   		   Artobj_Count = Artobj.Count
 		   		   TrackPath = track.Location
 		   		   If TrackPath = "" Then Artobj_Count = 0
 		   		   If Artobj_Count>0 Then
 		   		      For j = 1 to Artobj_Count
 		   		          Set Art = Artobj.Item(j)
                                          Not_attached_art = Art.IsDownloadedArtwork
                                          If Not_attached_art Then 
                                             Art.Delete
					     WScript.Echo "Deleted art of: " & TrackPath
					  End If
 		   		      Next
 		   		   End if
 		   		   NumFiles = NumFiles + 1
                   WScript.Echo "Arq. no: " & NumFiles & " Art count: " & Artobj_Count
                End If
 		    Next
 	    Next
	End If
Next
