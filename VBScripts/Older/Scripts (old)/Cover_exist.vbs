'==========================================================
'COVER EXIST
'GIVES INFORMATION ABOUT THE NUMBER OF ARTWORK COVERS
'TELLS WHETHER AN ITUNES TRACK HAS ART

Option Explicit

Dim TrackPath        ' The path to the track
Dim ArtPath	         ' The path to the artwork
Dim erro_desc
Dim numtracks
Dim IsDownlArtw_value
Dim erro_no
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
Dim Msg              ' A string for a message.
Dim songName
Dim artist
Dim result
Dim listarray
Dim num
Dim k
Dim track
Dim FormatArray(4)
Dim ExtArray(4)
Dim Artobj
Dim Art
Dim ArtDir
Dim Format
Dim BasePath
Dim fso 
Dim NumFiles
Dim KeepFiles
Dim args
Dim arg
'My vars - Jose's
Dim Artobj_Count

Set fso = CreateObject("Scripting.FileSystemObject")

FormatArray(0) = "Unknown"
FormatArray(1) = "JPEG"
FormatArray(2) = "PNG"
FormatArray(3) = "BMP"
ExtArray(0) = "unk"
ExtArray(1) = "jpg"
ExtArray(2) = "png"
ExtArray(3) = "bmp"

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

Dim vers
vers = iTunesApp.Version

Dim Reg1
Set Reg1 = new RegExp
Reg1.Pattern = "^10"
if Reg1.Test(vers) Then
	' yay
Else
	Wscript.Echo "This script requires iTunes 7"
	Wscript.Quit
End If

'THE BELOW VARIABLE SPECIFIES WHETHER TO KEEP OR DELETE THE ART FILE
KeepFiles = False

Set args = WScript.Arguments
' Scan command line arguments
For Each arg in args 
  ' Is it a flag.
  If Instr(1, arg, "-", 1) = 1 or Instr(1, arg, "/", 1) = 1 Then
    ' Check for list flag
    If UCase(arg) = "-K" or UCase(arg) = "/K" then
 KeepFiles = True
    End If
  End If
Next

For i = 1 to sources.Count
	Set source = sources.Item(i)
	
	IF source.Kind = 1 Then
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
		'result = 5
				
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
 		   		'Wscript.Echo "num: " & numtracks & " Count: " & tracks.Count & " m: " & m
 		   		
 		   		If track.Kind = 1 Then
 		   			songName = track.Name
 		   			artist = track.Artist
 		   			TrackPath = track.Location
                                        Wscript.Echo "Track path= " & TrackPath
 		   			Set Artobj = track.Artwork
 		   			Artobj_Count = Artobj.Count
                                        Wscript.Echo "Art obj count= " & Artobj_Count
 		   			If TrackPath = "" Then 
 		   			   Artobj_Count = 0
 		   			End if

					For c = 1 to Artobj_Count
						Set Art = Artobj.Item(c)
						desc = Art.Description
						IsDownlArtw_value = False
						On Error Resume Next
						IsDownlArtw_value = Art.IsDownloadedArtwork
						erro_no = Err.Number
						'Err.Clear
						erro_desc = Err.Description
						If Err.number <> 0 Then 
						   IsDownlArtw_value = False
						End If
                                                Wscript.Echo "Arq. no= " & m & " Location:" & TrackPath & " Art_obj: " & Artobj_Count & " IsDownlArtw=" & _
                                                IsDownlArtw_value & " Error_code=" & erro_no
						
					Next
 		   			
 		   		End If
 		   	Next
 		Next
		End If
Next
