'THIS CODE EXEMPLIFIES HOW TO CLEAR AN EXCEL SHEET


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
Dim songName
Dim songYear
Dim artist
Dim TrackAlbum
Dim AlbumArtist
Dim fso 
Dim num
Dim NumFiles
Dim numtracks
'ARTWORK VARIABLES
Dim Artobj
Dim Artobj_Count


'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet

Set fso = CreateObject("Scripting.FileSystemObject")

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
'READ ONLY IS FALSE
my_sheet = "D:\Python\Itunes DB.xls"
objExcel.Workbooks.Open (my_sheet),,False

objExcel.Application.Visible = False

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

objExcel.Range("2:20000").Clear

objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close
objExcel.Quit
