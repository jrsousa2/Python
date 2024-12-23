'Creates and adds ID3V2.3 tags into MP3 files. Public Domain.
'
'This script was written to support creating and adding 
'to ID3V2.3 tags for MP3 files. It ignores ID3V1 tags.
'There is no provision for modifying an existing tag or 
'for reading existing tags. 
'Only one tag can be added at a time. Run the command 
'multiple times to add multiple tags.
'
'All "T", "U", and "W" tags are supported as well as
'tags IPLS, APIC, COMM, GEOB, PRIV, USER, UFID, USLT, and SYLT.
'For a list of valid tag names, see:
'http://id3.org/id3v2.3.0#Declared_ID3v2_frames
'
'To simplify use, some assumptions were made:
'All tags are created configured as US-English and ASCII.
'Multi-line text will be corrected by the script to use LF.
'Mime types for APIC and GEOB are looked up in the registry 
'and fall back to application/octet-stream if nothing is found.
'
'To support the common case of just adding a cover photo, we 
'support a "simple mode" where no switches are needed. If an 
'MP3 file is dropped on the script and a JPG file exists in the 
'same directory as the MP3, then the JPG will be added to the MP3 
'as cover art. If there are several JPG files, the newest one 
'will be used.

Option Explicit

'Names of command-line switches (arguments) are defined here so they can be changed easily.
'The arguments are used on the command line like "id3.vbs /mp3:somefile.mp3".
Const ARG_MP3 = "Mp3" 'Specifies the target MP3 file (the MP3 file can also be specified with no switch like "id3.vbs somefile.mp3").
Const ARG_REMOVE = "Remove" 'WARNING: If this tag is used, all ID3V2 data will be stripped from the MP3!!!
Const ARG_TAG = "Tag" 'Specifies four-character ID like APIC for picture, TOPE for artist name, etc.
Const ARG_VALUE = "Value" 'Either text (for T tags), URL (for W tags), contact info (for PRIV and UFID), file name (for GEOB) or picture type (for APIC)
Const ARG_DESCRIPTION = "Description" 'A description of the data. Quite often just an empty string.
Const ARG_FILE = "File" 'File name of a file with needed data (e.g., A JPG file for the APIC tag).
Const SIMPLE_MODE = True 'If this is True, you can add cover art without switch arguments.
Const DEBUG_LEVEL = 0 '0=off, 1=stdout, 2=logged and stdout, 3=logged, stdout, and paused
Const REMOVE_AGGRESSIVE = True 'False=Trim length specified by header, True=Trim to start of MP3 data
Main

Sub Main
'Verify and retrieve all arguments, run other functions as needed.
Dim fs, strTest, blnValid, strTagBody
Dim strTagID, strDescription, strValue, strContact
Dim intPictureType, strName, strBinaryFileName, strMp3FileName
	Status vbCrLf & vbCrLf & "Main: " & Now()
	Set fs = CreateObject("Scripting.FileSystemObject")
	'We always have to have a supplied MP3 file. It can
	'be supplied as unnamed argument or by /MP3: argument
	strMp3FileName = ""
	If Wscript.Arguments.Named.Exists(ARG_MP3) Then
		strMp3FileName = WScript.Arguments.Named.Item(ARG_MP3)
	Else
		If WScript.Arguments.Unnamed.Count = 1 Then
			strMp3FileName = WScript.Arguments.Unnamed(0)
		Else
			If WScript.Arguments.Unnamed.Count > 1 Then
				ShowHelp "You seem to have multiple unnamed arguments! Please check for quotes around arguments and missing colons after switches."
				Exit Sub
			End If
		End If
	End If
	If strMp3FileName <> "" Then
		If Not fs.FileExists(strMp3FileName) Then
			ShowHelp "The MP3 file name """ & strMp3FileName & """ doesn't exist."
			Exit Sub
		End If
	Else
		ShowHelp "You have to supply an MP3 target file name either as an unnamed argument or through the /" & ARG_MP3 & ": argument."
		Exit Sub
	End If
	'Check for the /remove: argument which trumps everything else.
	If WScript.Arguments.Named.Exists(ARG_REMOVE) Then
		'Sanity check. There should be no other arguments!
		If Wscript.Arguments.Named.Exists(ARG_MP3) Then
			'Just /mp3: and /remove: arguments should exist.
			If WScript.Arguments.Named.Count > 2 Then
				ShowHelp "WARNING: The /" & ARG_REMOVE & " argument will completely strip all ID3V2 data from the MP3 file. You supplied additional arguments, so I think this isn't something you really wanted to do."
				Exit Sub
			End If
		Else
			'Just /remove: argument should exist since mp3 file was passed as unnamed argument.
			If WScript.Arguments.Named.Count > 1 Then
				ShowHelp "WARNING: The /" & ARG_REMOVE & " argument will completely strip all ID3V2 data from the MP3 file. You supplied additional arguments, so I think this isn't something you really wanted to do."
				Exit Sub
			End If
		End If
		'Jump immediately to the removal subroutine and exit.
		RemoveAllID3 strMp3FileName
		Exit Sub
	End If
	'Are we in SIMPLE_MODE?
	If SIMPLE_MODE Then
		'Simple mode presupposes no named arguments, so make sure there are none!
		If WScript.Arguments.Named.Count = 0 Then
			Status "Main: " & "in ""simple mode"" with no named arguments. Will look for picture."
			'In simple mode at this point we have an MP3 file specified, but we need a picture.
			'Maybe there's a JPG in the MP3 folder we can use? Get the most recent one.
			strBinaryFileName = ""
			For Each strTest In Split("jpg jpeg jpe pjpeg pjp jfif")
				strBinaryFileName = MostRecent(fs.GetParentFolderName(strMp3FileName), strTest)
				If strBinaryFileName <> "" Then Exit For
			Next
			Status "Main: " & "found picture " & strBinaryFileName
			'If we didn't find a picture, then we can't stay in simple mode!
			If strBinaryFileName <> "" Then
				'We have what we need. Go ahead and add the picture, then exit.
				strTagBody = Tag_APIC("APIC", 3, "", strBinaryFileName)
				If Not AddTag(strTagBody, strMp3FileName) Then
					WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
				End If
				Exit Sub
			End If
		End If
	End If
	'Everything from here on down depends on a Tag ID; make sure we have one!
	If Not Wscript.Arguments.Named.Exists(ARG_TAG) Then
		ShowHelp "Missing /" & ARG_TAG & ": 4-character tag ID argument."
		Exit Sub
	Else
		strTagID = Ucase(Wscript.Arguments.Named.Item(ARG_TAG))
		Status "Main: " & "TAG:" & UCase(strTagID)
		If Len(strTagID) <> 4 Then
			ShowHelp "The tag ID needs to be 4 characters long."
			Exit Sub
		End If
	End If
	'Make sure the 4-character tag ID is one we support.
	blnValid = False
	For Each strTest In Split("WCOM WCOP WOAF WOAR WOAS WORS WPAY WPUB IPLS TALB TBPM TCOM TCON TCOP TDAT TDLY TENC TEXT TFLT TIME TIT1 TIT2 TIT3 TKEY TLAN TLEN TMED TOAL TOFN TOLY TOPE TORY TOWN TPE1 TPE2 TPE3 TPE4 TPOS TPUB TRCK TRDA TRSN TRSO TSIZ TSRC TSSE TYER USER UFID PRIV TXXX WXXX COMM USLT SYLT APIC GEOB")
		If strTagID = strTest Then
			blnValid = True
			Exit For
		End If
	Next
	If Not blnValid Then 
		ShowHelp "Tags of type """ & strTagID & """ are not supported."
		Exit Sub
	End If
	'Check for and retrieve other arguments. Each argument is checked against the "tags" that require it.
	'###########  URL 
	For Each strTest In Split("WCOM WCOP WOAF WOAR WOAS WORS WPAY WPUB")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_VALUE) Then
				ShowHelp "Missing /" & ARG_VALUE & ": URL argument."
				Exit Sub
			Else
				strValue = Wscript.Arguments.Named.Item(ARG_VALUE)
				'Make sure the URL looks nominally like a URL
				If InStr(strValue, "://") = 0 Then
					ShowHelp "The /" & ARG_VALUE & ":" & Wscript.Arguments.Named.Item(ARG_VALUE) & " needs to be a URL, but it doesn't look like one to me!"
					Exit Sub
				End If
			End If
		End If
	Next
	'###########  SINGLE-LINE TEXT
	For Each strTest In Split("TALB TBPM TCOM TCON TCOP TDAT TDLY TENC TEXT TFLT TIME TIT1 TIT2 TIT3 TKEY TLAN TLEN TMED TOAL TOFN TOLY TOPE TORY TOWN TPE1 TPE2 TPE3 TPE4 TPOS TPUB TRCK TRDA TRSN TRSO TSIZ TSRC TSSE TYER")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_VALUE) Then
				ShowHelp "Missing /" & ARG_VALUE & ": argument."
				Exit Sub
			Else
				strValue = Wscript.Arguments.Named.Item(ARG_VALUE)
				'Don't tolerate multiline
				If ((InStr(strValue, vbCr) <> 0) Or (InStr(strValue, vbLf) <> 0)) Then
					ShowHelp "The /" & ARG_VALUE & ": argument should only be one line."
					Exit Sub
				End If
			End If
		End If
	Next
	'###########  DESCRIPTION
	For Each strTest In Split("TXXX WXXX COMM USLT SYLT APIC GEOB")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_DESCRIPTION) Then
				ShowHelp "Missing /" & ARG_DESCRIPTION & ": argument."
				Exit Sub
			Else
				strDescription = Wscript.Arguments.Named.Item(ARG_DESCRIPTION)
				'Don't tolerate multiline
				If ((InStr(strValue, vbCr) <> 0) Or (InStr(strValue, vbLf) <> 0)) Then
					ShowHelp "The /" & ARG_DESCRIPTION & ": description argument should only be one line."
					Exit Sub
				End If
			End If
		End If
	Next
	'###########  FILE
	For Each strTest In Split("IPLS USER COMM USLT SYLT PRIV UFID APIC GEOB")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_FILE) Then
				ShowHelp "Missing /" & ARG_FILE & ": file name argument."
				Exit Sub
			Else
				strBinaryFileName = Wscript.Arguments.Named.Item(ARG_FILE)
				If Not fs.FileExists(strBinaryFileName) Then
					ShowHelp "File """ & strBinaryFileName & """ doesn't exist."
					Exit Sub
				End If
			End If
		End If
	Next
	'###########  CONTACT
	For Each strTest In Split("PRIV UFID")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_VALUE) Then
				ShowHelp "Missing /" & ARG_VALUE & ": contact information argument."
				Exit Sub
			Else
				strContact = Wscript.Arguments.Named.Item(ARG_VALUE)
			End If
			'Don't tolerate multiline
			If ((InStr(strContact, vbCr) <> 0) Or (InStr(strContact, vbLf) <> 0)) Then
				ShowHelp "The /" & ARG_VALUE & ": contact information argument should only be one line."
				Exit Sub
			End If
		End If
	Next
	'###########  PICTURE TYPE
	For Each strTest In Split("APIC")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_VALUE) Then
				ShowHelp "Missing /" & ARG_VALUE & ": picture type argument (a number from 0-20, typically 3)."
				Exit Sub
			Else
				intPictureType = Wscript.Arguments.Named.Item(ARG_VALUE)
				If Not IsNumeric(intPictureType) Then
					ShowHelp "The /" & ARG_VALUE & ":" & intPictureType & " value must be a number from 0-20 (e.g., 3 for ""front cover"")"
					Exit Sub
				Else
					intPictureType = CInt(intPictureType)
					If ((intPictureType < 0) Or (intPictureType > 20)) Then
						ShowHelp "The /" & ARG_VALUE & ":" & intPictureType & " value must be a number from 0-20. (e.g., 3 for ""front cover"")"
						Exit Sub
					End If
				End If
			End If
		End If
	Next
	'###########  ORIGINAL FILE NAME
	For Each strTest In Split("GEOB")
		If strTest = strTagID Then
			If Not Wscript.Arguments.Named.Exists(ARG_VALUE) Then
				ShowHelp "Missing /" & ARG_VALUE & ": original file name argument."
				Exit Sub
			Else
				strName = Wscript.Arguments.Named.Item(ARG_VALUE)
			End If
			'Don't tolerate multiline
			If ((InStr(strName, vbCr) <> 0) Or (InStr(strName, vbLf) <> 0)) Then
				ShowHelp "The /" & ARG_VALUE & ": original file name argument should only be one line."
				Exit Sub
			End If
		End If
	Next
	
	'Pass the collected arguments to the appropriate tag-making and tag-embedding functions
	If (("TXXX" = strTagID) Or ("WXXX" = strTagID)) Then
		strTagBody = Tag_XXX(strTagID, strValue, strDescription)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If (("T" = Left(strTagID, 1)) Or ("IPLS" = strTagID)) Then
		strTagBody = Tag_T(strTagID, strValue)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If "W" = Left(strTagID, 1) Then
		strTagBody = Tag_W(strTagID, strValue)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If "USER" = strTagID Then
		strTagBody = Tag_USER(strTagID, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If (("UFID" = strTagID) Or ("PRIV" = strTagID)) Then
		strTagBody = Tag_PRIVUFID(strTagID, strContact, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If (("COMM" = strTagID) Or ("USLT" = strTagID)) Then
		strTagBody = Tag_COMMUSLT(strTagID, strDescription, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If "SYLT" = strTagID Then
		strTagBody = Tag_SYLT(strTagID, strDescription, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If "APIC" = strTagID Then
		strTagBody = Tag_APIC(strTagID, intPictureType, strDescription, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
	If "GEOB" = strTagID Then
		strTagBody = Tag_GEOB(strTagID, strName, strDescription, strBinaryFileName)
		If Not AddTag(strTagBody, strMp3FileName) Then
			WScript.Echo "FAIL! For some reason, I couldn't write the " & strTagID & " data to the file """ & strMp3FileName & """."
		End If
		Exit Sub
	End If
End Sub

Sub ShowHelp(strError)
Dim strMessage
	strMessage = strError
	If strMessage <> "" Then strMessage = strMessage & vbCrLf & vbCrLf
	strMessage = strMessage & "Adds new ID3V2 tags to MP3 files. Does not change existing tags. Usage:"
	strMessage = strMessage & vbCrLf & WScript.ScriptName & " [/" & ARG_MP3 & ":file.mp3 | file.mp3] [/" & ARG_TAG & ":ID | /" & ARG_REMOVE & "] [tag-specific args]"
	strMessage = strMessage & vbCrLf & "Tags and tag-specific arguments:"
	strMessage = strMessage & vbCrLf & "USER, IPLS		/" & ARG_FILE & ":"
	strMessage = strMessage & vbCrLf & "USLT, SYLT, COMM	/" & ARG_DESCRIPTION & ": /" & ARG_FILE & ":"
	strMessage = strMessage & vbCrLf & "PRIV, UFID		/" & ARG_VALUE & ": /" & ARG_FILE & ":"
	strMessage = strMessage & vbCrLf & "APIC, GEOB		/" & ARG_VALUE & ": /" & ARG_DESCRIPTION & ": /" & ARG_FILE & ":"
	strMessage = strMessage & vbCrLf & "TXXX, WXXX		/" & ARG_DESCRIPTION & ": /" & ARG_VALUE & ":"
	strMessage = strMessage & vbCrLf & "T???, W???		/" & ARG_VALUE & ":"
	WScript.Echo strMessage
End Sub

Function AddTag(strTagBody, strMP3FileName)
'Adds a pre-built tag to an MP3 file. Returns True on success.
'Can add to existing ID3 header or will create new ID3 header
Dim lngLength, strHeader, varNum, strMP3FileContents, fs
	Set fs = CreateObject("Scripting.FileSystemObject")
	Status "AddTag: " & strMP3FileName
	If Not fs.FileExists(strMP3FileName) Then
		Status "AddTag: " & "file doesn't exist"
		AddTag = False
		Exit Function
	End If
	If Len(strTagBody) < 10 Then
		Status "AddTag: " & "tag body is too small to be valid"
		AddTag = False
		Exit Function
	End If
	Status "AddTag: " & "tag length to be added is " & Len(strTagBody) & " bytes"
	strMP3FileContents = File2StringBinary(strMP3FileName)
	Status "AddTag: " & "file length is " & Len(strMP3FileContents) & " bytes"
	'Make the header
	strHeader = ""
	'Add ID3 identifier
	strHeader = strHeader & "ID3"
	'Version 3
	strHeader = strHeader & Chr(3) & Chr(0)
	'Flags
	strHeader = strHeader & Chr(0)
	'Header length is old size plus new data
	lngLength = RemoveID3Header(strMP3FileName)
	Status "AddTag: " & "old header length was " & lngLength & " bytes"
	lngLength = lngLength + Len(strTagBody)
	Status "AddTag: " & "new header length will be " & lngLength & " bytes"
	'Re-read the file since we just stripped the header
	strMP3FileContents = File2StringBinary(strMP3FileName)
	Status "AddTag: " & "new file length (with header removed) is " & Len(strMP3FileContents) & " bytes"
	'Total length of ID3 tags in SynchSafe bytes
	For Each varNum In Split(SyncSafe(lngLength))
    	strHeader = strHeader & Chr(varNum)
    Next
	'Write the changed file
	Status "AddTag: " & "writing..."
	AddTag = String2File(strHeader & strTagBody & strMP3FileContents, strMP3FileName)
End Function

Function RemoveID3Header(strMP3FileName)
'Removes the header. On success returns size value the old header specified or zero on fail
Dim fs, strMP3FileContents, strSyncSafe, intCount, lngHeader
	Status "RemoveID3Header: " & strMP3FileName
	Set fs = CreateObject("Scripting.FileSystemObject")
	If Not fs.FileExists(strMP3FileName) Then
		Status "RemoveID3Header: " & "file doesn't exist"
		RemoveID3Header = 0
		Exit Function
	End If
	strMP3FileContents = File2StringBinary(strMP3FileName)
	Status "RemoveID3Header: " & "read " & Len(strMP3FileContents) & " bytes"
	If "ID3" <> Left(strMP3FileContents, 3) Then
		Status "RemoveID3Header: " & "no ID3 header"
		RemoveID3Header = 0
		Exit Function
	End If
	strSyncSafe = Mid(strMP3FileContents, 7, 4)
	lngHeader = 0
	For intCount = 1 To 4
		lngHeader = lngHeader * 128
		lngHeader = lngHeader + Asc(Mid(strSyncSafe, intCount, 1))
	Next
	Status "RemoveID3Header: " & "old header size " & lngHeader
	strMP3FileContents = Mid(strMP3FileContents, 11)
	Status "RemoveID3Header: " & "new length without 11-byte header " & Len(strMP3FileContents) & " bytes"
	If String2File(strMP3FileContents, strMP3FileName) Then
		Status "RemoveID3Header: " & "file saved without 11-byte header"
		Status "RemoveID3Header: " & "length saved to disk is " & Len(File2StringBinary(strMP3FileName)) & " bytes"
		RemoveID3Header = lngHeader
	Else
		Status "RemoveID3Header: " & "error while saving file without 11-byte header"
		RemoveID3Header = 0
	End If
End Function

Function RemoveAllID3(strMP3FileName)
'Returns true on success (it found an ID3V2 tag and removed it)
'This removes the ID3V2 header and all tags, leaving a simple MP3 file.
Dim fs, strMP3FileContents, strSyncSafe, intCount, lngHeader, lngByte, lngSync, intVersion, intLayer, intProtection
	Set fs = CreateObject("Scripting.FileSystemObject")
	Status "RemoveAllID3: " & strMp3FileName
	If Not fs.FileExists(strMP3FileName) Then
		Status "RemoveAllID3: " & "file doesn't exist"
		RemoveAllID3 = False
		Exit Function
	End If
	strMP3FileContents = File2StringBinary(strMP3FileName)
	Status "RemoveAllID3: " & "file size " & Len(strMP3FileContents)
	If "ID3" <> Left(strMP3FileContents, 3) Then
		Status "RemoveAllID3: " & "no ID3 header"
		RemoveAllID3 = False
		Exit Function
	End If
	strSyncSafe = Mid(strMP3FileContents, 7, 4)
	lngHeader = 0
	For intCount = 1 To 4
		lngHeader = lngHeader * 128
		lngHeader = lngHeader + Asc(Mid(strSyncSafe, intCount, 1))
	Next
	Status "RemoveAllID3: " & "header says " & lngHeader & " bytes"
	strMP3FileContents = Mid(strMP3FileContents, lngHeader + 11)
	Status "RemoveAllID3: " & "new file size " & Len(strMP3FileContents)
	If REMOVE_AGGRESSIVE Then
		'Lots of bad headers out there. Look for the first MP3Sync bytes to try to recover from 
		'bad size bytes. There are 18 different different sync bytes, so look for all of them.
		'Pick the earliest location of a valid sync from the 18 possibilities.
		Status "RemoveAllID3: " & "aggressive search for start of MP3"
		lngSync = 0
		For Each intVersion In Array(0,2,3)
			For Each intLayer In Array(1,2,3)
				For Each intProtection In Array(0,1)
					lngByte = 224 + (8 * intVersion) + (2 * intLayer) + intProtection
					If InStr(strMP3FileContents, Chr(255) & Chr(lngByte)) <> 0 Then
						If lngSync = 0 Then 
							lngSync = InStr(strMP3FileContents, Chr(255) & Chr(lngByte))
						Else
							If lngSync > InStr(strMP3FileContents, Chr(255) & Chr(lngByte)) Then
								lngSync = InStr(strMP3FileContents, Chr(255) & Chr(lngByte))
							End If
						End If
					End If
				Next
			Next
		Next
		'If we found a valid MP3 sync, strip away all bytes before the sync
		If lngSync <> 0 Then
			Status "RemoveAllID3: " & "MP3 sync found at " & lngSync & " bytes"
			strMP3FileContents = Mid(strMP3FileContents, lngSync)
		End If
		Status "RemoveAllID3: " & "new file size " & Len(strMP3FileContents)
	End If
	RemoveAllID3 = String2File(strMP3FileContents, strMP3FileName)
End Function

Function MimeType(strFileName)
'Returns the mime type of a file if it's specified in the registry.
'If no registry entry, returns "application/octet-stream"
Dim ws, fs, strExt, strMime
	Set fs = CreateObject("Scripting.FileSystemObject")
	Set ws = CreateObject("Wscript.Shell")
	strExt = fs.GetExtensionName(strFileName)
	strMime = "application/octet-stream"
	On Error Resume Next
	strMime = ws.RegRead("HKEY_CLASSES_ROOT\." & strExt & "\Content Type")
	On Error Goto 0
	MimeType = strMime
End Function

Function Tag_APIC(strTagID, intPictureType, strDescription, strBinaryFileName)
'Creates a "picture" tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Mime	00	PictureTypeNumber	Description	00	Binary data
'Picture type is decimal 0-20 from http://id3.org/id3v2.3.0#Attached_picture
'Most common picture type is 3 for "front cover" or 1 
'for a 32x32 PNG icon. Only JPG or PNG pictures are supported.
Dim lngTag, strFileContents, strTagBody, strMime
	strFileContents = File2StringBinary(strBinaryFileName)
	'Mime Type (for either jpg, jpeg, or png files)
	strMime = MimeType(strBinaryFileName)
	'Make the APIC tag
	strTagBody = ""
	'The tag ID
	strTagBody = strTagBody & strTagID
	'Size of this tag (length of arguments + 4)
	lngTag = Len(strFileContents) + Len(strMime) + Len(strDescription) + 4
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
    'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Mime type
	strTagBody = strTagBody & Chr(0) & strMime & Chr(0)
	'Picture type
	strTagBody = strTagBody & Chr(intPictureType)
	'Description text encoding
	strTagBody = strTagBody & strDescription & Chr(0)
	'Add the actual picture
	strTagBody = strTagBody & strFileContents
	'Return value
	Tag_APIC = strTagBody
End Function

Function Tag_GEOB(strTagID, strName, strDescription, strBinaryFileName)
'Creates a GEOB (General encapsulated object) tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Mime	00	OriginalFileName	00	Description	00	BinaryData
Dim strMime, lngTag, strFileContents, strTagBody
	strFileContents = File2StringBinary(strBinaryFileName)
	'Mime Type
	strMime = MimeType(strBinaryFileName)
	'Make the tag
	strTagBody = ""
	'The tag ID
	strTagBody = strTagBody & strTagID
	'Size of this tag (length of arguments + 4)
	lngTag = Len(strFileContents) + Len(strMime) + Len(strDescription) + Len(strName) + 4
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
    'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Mime type
	strTagBody = strTagBody & Chr(0) & strMime & Chr(0)
	'File name
	strTagBody = strTagBody & strName & Chr(0)
	'Description text encoding
	strTagBody = strTagBody & strDescription & Chr(0)
	'Add the actual picture
	strTagBody = strTagBody & strFileContents
	'Return value
	Tag_GEOB = strTagBody
End Function

Function Tag_T(strTagID, strValue)
'Creates a text tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00 Text
Dim strTagBody, lngTag
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size of this tag (length of arguments + 1)
	lngTag = 1 + Len(strValue)
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
	'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Encoding
	strTagBody = strTagBody & Chr(0)
	'Data
	strTagBody = strTagBody & strValue
	'Done
	Tag_T = strTagBody
End Function

Function Tag_W(strTagID, strValue)
'Creates a URL tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	URL
Dim strTagBody, lngTag
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size is length of URL
	lngTag = Len(strValue)
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
	'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Data
	strTagBody = strTagBody & strValue
	'Done
	Tag_W = strTagBody
End Function

Function Tag_XXX(strTagID, strValue, strDescription)
'Creates a "user-defined" text or URL tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Description	00	Value
Dim strTagBody, lngTag
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size
	lngTag = 2 + Len(strValue) + Len(strDescription)
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
	'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Description
	strTagBody = strTagBody & strDescription & Chr(0)
	'Data (text or URL)
	strTagBody = strTagBody & strValue
	'Done
	Tag_XXX = strTagBody
End Function

Function Tag_USER(strTagID, strBinaryFileName)
'Creates a "terms of use" tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Language (eng)	Text
Dim strTagBody, strValue, lngTag
	'Read the text file containing the (potentially) multi-line terms of use
	strValue = File2StringBinary(strBinaryFileName)
	'Only linefeeds are allowed
	strValue = Replace(strValue, vbCrLf, vbLf)
	strValue = Replace(strValue, vbCr, vbLf)
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size
	lngTag = 1 + Len(strValue) + Len ("eng")
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
	'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Encoding
	strTagBody = strTagBody & Chr(0)
	'Language
	strTagBody = strTagBody & "eng"
	'Data
	strTagBody = strTagBody & strValue
	'Done
	Tag_USER = strTagBody
End Function

Function Tag_PRIVUFID(strTagID, strContact, strBinaryFileName)
'Creates a "private frame" or "unique file identifier" tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	Email-URL	00	BinaryData
Dim lngTag, strFileContents, strTagBody
	strFileContents = File2StringBinary(strBinaryFileName)
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size of this tag (length of arguments + 1)
	lngTag = Len(strFileContents) + Len(strContact) + 1
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
    'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Contact info
	strTagBody = strTagBody & strContact & Chr(0)
	'Add the binary data
	strTagBody = strTagBody & strFileContents
	'Return value
	Tag_PRIVUFID = strTagBody
End Function

Function Tag_COMMUSLT(strTagID, strDescription, strBinaryFileName)
'Creates a "comments" or "unsynced lyrics" tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Language(eng)	Description	00	Text
Dim lngTag, strValue, strTagBody
	strValue = File2StringBinary(strBinaryFileName)
	'Only linefeeds are allowed
	strValue = Replace(strValue, vbCrLf, vbLf)
	strValue = Replace(strValue, vbCr, vbLf)
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size of this tag
	lngTag = Len(strValue) + Len(strDescription) + Len("eng") + 2
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
    'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Encoding
	strTagBody = strTagBody & Chr(0)
	'Language
	strTagBody = strTagBody & "eng"
	'Description
	strTagBody = strTagBody & strDescription & Chr(0)
	'Add the binary data
	strTagBody = strTagBody & strValue
	'Return value
	Tag_COMMUSLT = strTagBody
End Function

Function Tag_SYLT(strTagID, strDescription, strBinaryFileName)
'Creates a "synced lyrics" tag. Returns the actual binary data for the tag.
'TagID	Size	Flags	00	Language(eng)	TimeStamp(02) ContentType(02)  Description	00	Text
Dim lngTag, strValue, strTagBody
	strValue = File2StringBinary(strBinaryFileName)
	'Only linefeeds are allowed
	strValue = Replace(strValue, vbCrLf, vbLf)
	strValue = Replace(strValue, vbCr, vbLf)
	'Start building the tag with the ID
	strTagBody = strTagID
	'Size of this tag
	lngTag = Len(strValue) + Len(strDescription) + Len("eng") + 4
	strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 1, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 3, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 5, 2))
    strTagBody = strTagBody & Chr("&H" & Mid(Right("00000000" & Hex(lngTag), 8), 7, 2))
    'Flags
	strTagBody = strTagBody & Chr(0) & Chr(0)
	'Encoding
	strTagBody = strTagBody & Chr(0)
	'Language
	strTagBody = strTagBody & "eng"
	'Time Stamp (01=frames 02=milliseconds)
	strTagBody = strTagBody & Chr(2)
	'Content Type (00=other 01=lyrics 02=transcription)
	strTagBody = strTagBody & Chr(1)
	'Description
	strTagBody = strTagBody & strDescription & Chr(0)
	'Add the binary data
	strTagBody = strTagBody & strValue
	'Return value
	Tag_SYLT = strTagBody
End Function

Function UnSyncSafe(lng1, lng2, lng3, lng4)
'Takes four SyncSafe byte values (where lng1 is 
'MSB, lng4 is LSB) and returns the actual value
Dim lngOut
	lngOut = 0
	lngOut = (lngOut * 128) + lng1
	lngOut = (lngOut * 128) + lng2
	lngOut = (lngOut * 128) + lng3
	lngOut = (lngOut * 128) + lng4
	UnSyncSafe = lngOut
End Function

Function SyncSafe(lngNumber)
'Returns space delimited byte values MSB first
Dim lngTemp
Dim lng1, lng2, lng3, lng4 'Where lng1 is MSB, lng4 is LSB
	lngTemp = lngNumber
	lng4 = (lngTemp Mod 128)
	lngTemp = lngTemp \ 128
	lng3 = (lngTemp Mod 128)
	lngTemp = lngTemp \ 128
	lng2 = (lngTemp Mod 128)
	lngTemp = lngTemp \ 128
	lng1 = (lngTemp Mod 128)
	SyncSafe = lng1 & " " &  lng2 & " " & lng3 & " " & lng4
End Function

Function File2StringBinary(strFile) 'As String
Dim fs, ts, strData, lngLength, lngTries
Const ForReading = 1
	strData = ""
	Set fs = CreateObject("Scripting.FileSystemObject")
	If fs.FileExists(strFile) Then
		On Error Resume Next
		lngLength = 0
		For lngTries = 1 To 10
			lngLength = fs.GetFile(strFile).Size
			If lngLength <> 0 Then Exit For
			WScript.Sleep 500
		Next
		If lngLength = 0 Then
			WScript.Echo "FATAL ERROR: File """ & strFile & """ seems to be zero length."
			WScript.Quit
		End If
		Set ts = Nothing
		For lngTries = 1 To 10
			Set ts = fs.OpenTextFile(strFile, ForReading, True)
			If Not ts Is Nothing Then Exit For
			WScript.Sleep 500
		Next
		If ts Is Nothing Then
			WScript.Echo "FATAL ERROR: File """ & strFile & """ can't be opened for reading. The error is:" & vbCrLf & Err.Description
			WScript.Quit
		End If
		strData = ts.Read(lngLength)
		ts.Close
		If Len(strData) = 0 Then
			WScript.Echo "FATAL ERROR: File """ & strFile & """ seems to be empty."
			WScript.Quit
		End If
		
		On Error Goto 0
	End If
	File2StringBinary = strData
End Function

Function String2File(strData, strFileName)
'Writes a string to a file. Returns True if success.
Dim fs 'As Scripting.FileSystemObject
Dim ts 'As Scripting.TextStream
Dim lngChar, strBlock, intChar, dtTimeStamp, lngTries
Const ForWriting = 2
	Set fs = CreateObject("Scripting.FileSystemObject")
	On Error Resume Next
	If fs.FileExists(strFileName) Then
		dtTimeStamp = FileModTimestamp(strFilename) 
	Else
		dtTimeStamp = "0"
	End If
	Err.Clear
	Set ts = Nothing
	For lngTries = 1 To 10
		Set ts = fs.OpenTextFile(strFileName, ForWriting, True)
		If Not ts Is Nothing Then Exit For
		WScript.Sleep 500
	Next
	If ts Is Nothing Then
		WScript.Echo "FATAL ERROR: File """ & strFile & """ can't be opened for writing. The error is:" & vbCrLf & Err.Description
		WScript.Quit
	End If
	Err.Clear
	For lngTries = 1 To 10
		ts.Write strData
		If Err.Number = 0 Then Exit For
		Err.Clear
		WScript.Sleep 500
	Next
	If Err.Number <> 0 Then
		'Must have hit one of the "problem characters" between 128 and 159
		For lngChar = 1 To Len(strData) Step 100
			Err.Clear
			ts.Write Mid(strData, lngChar, 100)
			If Err.Number <> 0 Then
				'This block of 100 must have the problem. Write them one-at-a-time
				Status "String2File: " & "hit a problem about " & lngChar & " bytes in"
				strBlock = Mid(strData, lngChar, 100)
				For intChar = 1 To Len(strBlock)
					ts.Write Chr(255 And AscW(Mid(strBlock, intChar)))
				Next
			End If
		Next
	End If
	ts.Close
	If fs.FileExists(strFileName) Then
		If dtTimeStamp = FileModTimestamp(strFilename) Then 
			Status "String2File: " & "timestamp wasn't changed after write"
			String2File = False
		Else
			Status "String2File: " & "timestamp was updated after write"
			String2File = True
		End If
	Else
		Status "String2File: " & "file doesn't exist after write"
		String2File = False
	End If
End Function

Function FileModTimestamp(strFilename)
'Returns a high-precision last-modified timestamp like 20140331211026.649060-420
Dim wmi, fil, fils, ts
	Set wmi = GetObject("winmgmts:\\.\root\CIMV2")
	Set fils = wmi.ExecQuery("Select * from CIM_DataFile where Name = '" & Replace(strFilename, "\", "\\") & "'", "WQL", 48)
	For Each fil in fils
		ts = fil.LastModified
	Next
	FileModTimestamp = ts
End Function

Function MostRecent(strFolderPath, strFileExtension)
'Returns the full path of the most recent file
	Dim fs, fol, fils, fil, strMostRecent
	Set fs = CreateObject("Scripting.FileSystemObject")
	Set fol = fs.GetFolder(strFolderPath)
	Set fils = fol.Files
	strMostRecent = ""
	For Each fil In fils
		If Lcase(fs.GetExtensionName(fil.Name)) = LCase(strFileExtension) Then
			If strMostRecent = "" Then 
				strMostRecent = fil.Path
			End If
			If fil.DateLastModified > fs.GetFile(strMostRecent).DateLastModified Then
				strMostRecent = fil.Path
			End If
		End If
	Next
	MostRecent = strMostRecent
End Function

Sub Status(strMessage)
	If DEBUG_LEVEL > 0 Then 
		If Lcase(Right(Wscript.FullName, 12)) = "\cscript.exe" Then
			Wscript.Echo strMessage
		End If
	End If
	If DEBUG_LEVEL > 1 Then
		WriteLog strMessage
	End If
	If DEBUG_LEVEL > 2 Then
		MsgBox "Message:" & vbCrLf & strMessage & vbCrLf & "Press OK to continue" 
	End If
End Sub

Sub WriteLog(strText)
Dim fs 'As Scripting.FileSystemObject
Dim ts 'As Scripting.TextStream
Const ForAppending = 8
	Set fs = CreateObject("Scripting.FileSystemObject")
	Set ts = fs.OpenTextFile(Left(Wscript.ScriptFullName, InstrRev(Wscript.ScriptFullName, ".")) & "log", ForAppending, True)
	ts.WriteLine strText
	ts.Close
End Sub
