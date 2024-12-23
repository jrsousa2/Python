Set FSO = CreateObject("Scripting.FileSystemObject")
Set Folder=FSO.GetFolder("D:\Z-Covers\dupe_covers")

For Each Subfolder in Folder.SubFolders
    Wscript.Echo Subfolder.Path
    If subfolder.Files.Count<=1 Then subfolder.delete
Next


'dim filesys
'Set filesys = CreateObject("Scripting.FileSystemObject") 
'If filesys.FolderExists("c:\DevGuru\website\") Then  
'filesys.DeleteFolder "c:\DevGuru\website" 
'Response.Write("Folder deleted") 
'End If 