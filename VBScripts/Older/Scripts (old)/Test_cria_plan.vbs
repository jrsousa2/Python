'TESTA COMO CRIAR UMA PLANILHA EXCEL DO ZERO

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
Dim objWorkbook


'CREATES AN EXCEL SHEET
Dim objExcel
Dim my_sheet

Set fso = CreateObject("Scripting.FileSystemObject")

Set iTunesApp  = CreateObject("iTunes.Application.1")
Set sources = iTunesApp.Sources

'TRIES TO CREATE AN INTERFACE WITH EXCEL
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = True

objExcel.Application.Visible = False

Set objWorkbook = objExcel.Workbooks.Add()

objExcel.Cells(1, 1) = "Artist"
objExcel.Cells(1, 2) = "AlbumArtist"
objExcel.Cells(1, 3) = "songName"
objExcel.Cells(1, 4) = "songYear"
objExcel.Cells(1, 5) = "TrackAlbum"
objExcel.Cells(1, 6) = "TrackPath"
objExcel.Cells(1, 7) = "Artobj_Count"
objExcel.Cells(1, 8) = "track_Bitrate"
objExcel.Cells(1, 9) = "track_time"

'SAVE FILE
my_sheet = "D:\Dummy\Excel\test.xls"
objWorkbook.SaveAs(my_sheet)

'objExcel.ActiveWorkbook.Save 'my_sheet
objExcel.ActiveWorkbook.Close

objExcel.Quit
