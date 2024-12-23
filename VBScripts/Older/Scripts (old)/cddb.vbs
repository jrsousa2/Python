Dim id3
Dim FS

Sub ListID3Tags(sFolder)
  'get FileSystemObject To enumerate files
  Set FS = CreateObject("Scripting.FileSystemObject")
  WScript.Echo "Test: " & sFolder
  'call ListID3TagsFS Function with a folder object
  ListID3TagsFS FS.GetFolder(sFolder)
End Sub

Sub ListID3TagsFS(Root)
  Dim SubFolder, File
  
  'enumerate all files In the folder
  For Each File In Root.Files
    'select only mp3 And wma files
    Select Case LCase(Right(File.Name, 4))
      Case ".mp3", ".wma": ListID3TagsFile File
    End Select
  Next

  'process all subfolders
  For Each SubFolder In Root.SubFolders
    ListID3TagsFS SubFolder
  Next
End Sub

Sub ListID3TagsFile(File)
  'Get id3 object To change data
  Set id3 = CreateObject("CDDBControl.CddbID3Tag")

  'load id3 data from a file, read only
  id3.LoadFromFile File.Path, True
  
  'print some of id3 tags
  WScript.Echo File.Name, id3.Album, id3.Title
End Sub

'This should call the func
sFolder = "D:\MP3_outros\Arrumadas"
ListID3Tags sFolder
  