Option Explicit
Dim iTunesApp
Dim Tracks
Dim faixa1
Dim faixa2
Dim Artobj1
Dim Artobj2
Dim Artwork1
Dim Artwork2
Dim Playlist


'VARIABLES
Dim songName
Dim TrackPath
Dim Pos
Dim Filename
Dim Format
Dim FormatArray(4)

FormatArray(0) = "Unknown"
FormatArray(1) = "JPEG"
FormatArray(2) = "PNG"
FormatArray(3) = "BMP"

Set iTunesApp = CreateObject("iTunes.Application.1")
Set Tracks = iTunesApp.LibraryPlaylist

Set faixa1 = Tracks.AddFile("D:\MP3\L\Limp Bizkit - Faith.mp3").Tracks.Item(1)

songName = faixa1.Name
TrackPath = faixa1.Location

Wscript.Echo "Song name: " & songName

'IDENTIFICA O NOME DO ARQUIVO, POIS A CAPA SERA SALVA COM ESSE NOME
Pos = Instr(1, StrReverse(trackpath), "\", 1)
Pos = Len(trackpath) - pos + 2
Filename = Mid (TrackPath, pos)

Wscript.Echo "File: " & Filename

Set Artobj1 = faixa1.Artwork
'Artobj_Count = Artobj.Count
Set Artwork1 = Artobj1.Item(1)
Format = Artwork1.Format
Wscript.Echo "Format is " & FormatArray(Format)

'REMOVES .MP3 EXTENSION AND APPENDS IMAGE EXTENSION
Pos = Instr(1, LCase(Filename), ".mp3", 1)-1
Filename = Mid (Filename, 1,pos)

Filename = Filename & "." & LCase(FormatArray(Format))
Wscript.Echo "capa is: " & Filename

Artwork1.SaveArtworkToFile("D:\Z-Covers\Found Covers\" & Filename)

'HERE IS THE PART WHERE I READ THE NEXT TRACK (WITH ART)
Set faixa2 = Tracks.AddFile("D:\Z-Covers\Found Covers\Bee Gees - Emotion.mp3").Tracks.Item(1)

songName = faixa2.Name

Wscript.Echo "Location: " & faixa2.Location

'SAVES THE EXPORTED COVER INTO THE OTHER FILE
Set Artobj2 = faixa2.Artwork
'Artobj_Count = Artobj.Count
Set Artwork2 = Artobj2.Item(1)

If Artwork2 Is Nothing Then 
WScript.Echo "Ha um Erro"
Else
WScript.Echo "OK!"
End If

'Set Artwork2 = faixa2.Item(1).Artwork
'WScript.Echo "Numero de capas: " & Artwork2.Count

'faixa2.SetArtworkFromFile("D:\Z-Covers\Found Covers\Limp Bizkit - Faith.jpg")


'INSERTS NEWLY SAVED IMAGE INTO FILE
'Set teste = Artwork2.Item(0)

' Create playlist
Set playlist = iTunesApp.LibrarySource.Playlists.ItemByName("My Test")
if playlist is not Nothing then
playlist.delete
WScript.Echo "OK!"
end if

'If playlist is Nothing then
'   iTunesApp.CreatePlaylist("My Test")
'Set playlist = iTunesApp.LibrarySource.Playlists.ItemByName("My Test")
'End if

' Add file to playlist
'playlist.AddFile("D:\Z-Covers\Found Covers\Bee Gees - Emotion.mp3")
'Playlist.trackID


