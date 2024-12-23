Sub ListID3TagsFS(Root)
Dim SubFolder, File
  
'*** enumerate all files In the folder
For Each File In Root.Files
 Select Case LCase(Right(File.Name, 4))
       Case ".mp3"
  ListID3TagsFile File
 End Select
Next


'*** process all subfolders
For Each SubFolder In Root.SubFolders
 ListID3TagsFS SubFolder
Next


End Sub


Sub ListID3TagsFile(File)
'*** Get id3 object To change data
Dim id3
Set id3 = CreateObject("CDDBControl.CddbID3Tag")


'*** load id3 data from a file, read only
id3.LoadFromFile File.Path, True
  
'*** print some of id3 tags
WScript.Echo File.Path & chr(9) & id3.LeadArtist & Chr(9) & id3.Title & Chr(9) & id3.Album & Chr(9) & id3.Year & Chr(9) & id3.Genre


End Sub


'******************************************************************
'*** Main Procedure                                             ***
'******************************************************************

'*** Get Arguments
set oArgs = wscript.arguments
'sFolder = oArgs(0)
sFolder = "D:\MP3_outros\Arrumadas"

'*** get FileSystemObject To enumerate files
Dim oFS
Set oFS = CreateObject("Scripting.FileSystemObject")


'*** call ListID3TagsFS Function with a folder object
ListID3TagsFS oFS.GetFolder(sFolder)


'The output of the script is a single text file (tab delimited) that contains 
'the entire MP3 collection.  This can be edited in Excel or Access for consistency 
'and used as an input file for the following script that will individually update 
'each MP3 file (note however, that Excel will add quotes to some of these fields if 
'saved as a text file - tab delimited.  I found it better to actually copy the entire 
'spreadsheet and paste it into notepad to get a "clean" text file for input.  
'Once the output file has been cleaned up, the following script can be used to read the 
'information from the output file back into the individual ID3 tags.


On Error Resume Next
set oArgs = wscript.arguments
sFolder = oArgs(0)


'*** get FileSystemObject To enumerate files
Dim oFS
Set oFS = CreateObject("Scripting.FileSystemObject")
Set iFile = oFS.OpenTextFile(sFolder, 1)


Do Until iFile.AtEndofStream


 LineA = iFile.Readline
 Values = Split(LineA, Chr(9))
 EditID3Tags Values(0), Values(1), Values(2), Values(3)
Loop


Sub EditID3Tags(File,Artist,SongTitle,Album)
'*** Get id3 object To change data
Dim id3
Set id3 = CreateObject("CDDBControl.CddbID3Tag")


'*** load id3 data from a file, read only
id3.LoadFromFile File, True

WScript.Echo File.Name, id3.Album, id3.Title, id3.LeadArtist
  
'*** Save the id3 tags
'id3.Album = Album
'id3.Title = SongTitle
'id3.LeadArtist = Artist


'id3.SaveToFile File
'If Err <> 0 Then
' wScript.Echo "Error: " & Artist & ": " & SongTitle & "[" & Album & "]"
' Err.Clear
'Else
' wscript.echo "Completed " & Artist & ": " & SongTitle & "[" & Album & "]"
'End If


End Sub