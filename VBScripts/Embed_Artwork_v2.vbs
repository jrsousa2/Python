'===========================================
'EMBED
'EMBEDS THE ITUNES ARTWORK INTO THE METADATA
'OF THE FILES.

' ###############################################################################
' #
' # itunes_insert_artwork.vbs
' #
' # This script will tag your files using artwork downloaded using iTunes 7
' #
' # written by: Robert Jacobson (http://teridon.googlepages.com/itunesscripts)
' # Last Updated: 03 Jan 2007
' # Version 1.0
' #
' # This script is GPL v2.  see http://www.gnu.org/copyleft/gpl.html
' #
' # Use option "-k" to keep the artwork files extracted 
' # (in the same location as the song file)
' # (the default is to remove the files)
' ###############################################################################

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
	'Wscript.Quit
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
		Wscript.Echo "Select from the following to embed artwork" & chr(13) & chr(10)
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
 		   		'Wscript.Echo " m: " & m
 		   		
 		   		If track.Kind = 1 Then
 		   			songName = track.Name
 		   			artist = track.Artist
 		   			TrackPath = track.Location
 		   			Set Artobj = track.Artwork
 		   			Artobj_Count = Artobj.Count
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
                                               'Wscript.Echo "Arq. no= " & m & " IsDownlArtw=" & IsDownlArtw_value & " Error_code=" & erro_no
						If IsDownlArtw_value Then
						  'If track.Comment = "Risomar" Then track.Comment =
						   Format = Art.Format
						  'Wscript.Echo "Format is " & FormatArray(Format)
						   ArtDir = fso.GetParentFolderName(TrackPath)
						   Wscript.Echo "Artdir: " & ArtDir
						   'ArtDir = fso.GetBaseName(ArtDir)
						   'Wscript.Echo "Artdir is " & ArtDir
						   Dim RegX
						   Set RegX = new RegExp
						   RegX.Pattern = "[/:\\\*\?""""<>]"
						   RegX.Global = True
						   songName = RegX.Replace(songName, "-")
                                                   artist = RegX.Replace(artist, "-")
						   'songName = Replace(songName, "/", "-")
						   ArtPath = fso.BuildPath(ArtDir, artist & " - " & songName & "." & ExtArray(Format))
						   ' save to file
						   Art.SaveArtworkToFile(ArtPath)
						   ' insert from file into track tag
						   Art.SetArtworkFromFile(ArtPath)
						   If (KeepFiles) Then
						   'Do nothing
						    Else
						     fso.DeleteFile(ArtPath)
						   End If
						   NumFiles = NumFiles + 1
                                                   Wscript.Echo "Track#: " & m & " Embedded covers: " & NumFiles & " Artpath: " & ArtPath
						   ArtPath = ""
						End If
					Next
 		   			
 		   		End If
                        If (m - 100*(m\100)) = 0 then WScript.Echo "Track no: " & m
 		   	Next
                        'BELOW IS THE NUMBER OF FILES THAT THE SCRIPT WAS ABLE TO EMBED THE ART
 		   	Wscript.Echo NumFiles & " covers embedded in playlist " & playlistName
 		Next
		End If
Next
       
Wscript.StdOut.Write vbNewLine & "Press ENTER to continue"
Do While Not WScript.StdIn.AtEndOfLine       
   Input = WScript.StdIn.Read(1)
Loop