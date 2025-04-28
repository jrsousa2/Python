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
Dim Album_name
Dim Alb_Artist
Dim result
Dim listarray
Dim num
Dim k

'My vars - Jose's
Dim track
Dim track_busca
Dim Artobj
Dim ArtObj_Busca
Dim Art
Dim Art_Busca
Dim Artobj_Count
Dim Artobj_Count_busca

Dim FormatArray(4)
Dim ExtArray(4)

Dim ArtDir
Dim Format
Dim BasePath
Dim fso 
Dim NumFiles
Dim KeepFiles
Dim args
Dim arg

'USADO NA BUSCA 
Dim Achou

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
		'result = WScript.StdIn.ReadLine
		'COLOCAR O NUMERO DA PLAYLIST DESEJADA AQUI
		result = 16
				
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
 		   		If m > numtracks Then Exit For
 		   		Set track = tracks.Item(m)
 		   		'Wscript.Echo " m: " & m
 		   		
 		   		If track.Kind = 1 And track.Location <> "" Then
 		   		Alb_Artist = track.AlbumArtist
 		   		Album_name = track.Album
 		   		TrackPath = track.Location
 		   		'LOOKS FOR ARTWORK
 		   		Set Artobj = track.Artwork.Item(1)
 		   		Artobj.SetArtworkFromFile("D:\Python\Adriana Calcanhoto - Coletanea Pessoal.jpg")
 		   		
 		   		Artobj_Count = Artobj.Count
 		   		
 		   		Set Art = Artobj.Item(1)
   		        'Set Artobj = track.Artwork'.Item(1)
	   		    'Artobj.SetArtworkFromFile(ArtPath)
	   		    'Artobj_Count = Artobj.Count
	   		    'Set Art = Artobj.Item(1)

                If Artobj_Count=0 Then 
                
                'THE LOOP BELOW WILL SEARCH FOR THE ABOVE ARTIST/ALBUM
                c=0
                Achou = False
                Artobj_Count_busca=0
                Do
                  c=c+1
                  Set track_busca = tracks.Item(c)
                  If track_busca.Kind = 1 And track_busca.Location <> "" And _
                     LCase(Alb_Artist) = LCase(track_busca.AlbumArtist) And _
                     LCase(Album_name) = LCase(track_busca.Album) Then Achou = True
                  If Achou Then
                     Set Artobj_busca = track_busca.Artwork
 		   		     Artobj_Count_busca = Artobj_busca.Count
 		   		     If Artobj_Count_busca=0 Then Achou=False
 		   		  End If
 		   		  'ACHOU?
 		   		  If Achou Then 
 		   		     Set Art_busca = Artobj_busca.Item(1)
 		   		     'WILL SAVE THE ART TO A FILE
 		   		     NumFiles = NumFiles+1
 		   		  	 Format = Art_busca.Format
                     ArtDir = "D:\Python" 
                     Dim RegX
                     Set RegX = new RegExp
                     RegX.Pattern = "[/:\\\*\?""""<>]"
                     RegX.Global = True
                     'THE BELOW NEEDS TO CHANGE
                     'Album_name = RegX.Replace(Album_name, "-")
                     ArtPath = fso.BuildPath(ArtDir, Alb_Artist & " - " & RegX.Replace(Album_name, "-") & "." & ExtArray(Format))
				     'save to file
					 Art_busca.SaveArtworkToFile(ArtPath)
					 'insert from file into track tag
					 
					 'RETORNANDO A TRACK INICIAL
 		   		     'SET ART
 		   		     Set track_busca = tracks.Item(m)
 		   		     Set Artobj_busca = track_busca.Artwork
 		   		     'Set Art_busca = ArtObj_Busca.Item(1)
 		   		     Art.SetArtworkFromFile(ArtPath)
 		   		     
 		   		     'Set track = tracks.Item(m)
 		   		     'Set Artobj = track.Artwork'.Item(1)
 		   		     'Artobj.SetArtworkFromFile(ArtPath)
 		   		     'Artobj_Count = Artobj.Count
 		   		     'Set Art = Artobj.Item(1)
					 
					 If (KeepFiles) Then
						'do nothing
					   Else
					   'fso.DeleteFile(ArtPath)
                     End If
                     WScript.Echo NumFiles & " covers embedded in playlist " & playlistName
 		   		  End If  
                Loop Until Achou Or c=m
                
 		   		'end below is for scan all tracks in playlist searching for artist
 		   		End If
 		   		'end below is the end of kind=1 filter	
 		   		End If
 		   	Next
                        'BELOW IS THE NUMBER OF FILES THAT THE SCRIPT WAS ABLE TO EMBED THE ART
 		   	Wscript.Echo NumFiles & " covers embedded in playlist " & playlistName
 		Next
		End If
Next
