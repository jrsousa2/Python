' ==============
' EmbedFolderArt
' ==============
' Version 1.0.0.1 - February 27h 2013
' Copyright © Steve MacGuire 2013
' http://samsoft.org.uk/iTunes/EmbedFolderArt.vbs
' Please visit http://samsoft.org.uk/iTunes/scripts.asp for updates

' =======
' Licence
' =======
' This program is free software: you can redistribute it and/or modify it under the terms
' of the GNU General Public License as published by the Free Software Foundation, either
' version 3 of the License, or (at your option) any later version.

' This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
' without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
' See the GNU General Public License for more details.

' Please visit http://www.gnu.org/licenses/gpl-3.0-standalone.html to view the GNU GPLv3 licence.

' ===========
' Description
' ===========
' Embed artwork stored in the same folder as the file

' Stores any iTunes downloaded artwork as iTunesArt in the folder 
' and will embed the same if the largest image

' Prompted by this Apple Support Communities thread: https://discussions.apple.com/thread/4832324

' =========
' ChangeLog
' =========
' Version 1.0.0.1 - Initial version

' ==========
' To-do List
' ==========
' Add more things to do

' =============================
' Declare constants & variables
' =============================
' Core values for reusable code
' Modified 2012-12-18
Option Explicit	        ' Declare all variables before use
Const Kimo=False        ' True if script expects "Keep iTunes Media folder organised" to be disabled
Const Min=0             ' Minimum number of tracks this script should work with
Const Max=0             ' Maximum number of tracks this script should work with, 0 for no limit
Const Warn=500          ' Warning level, require confirmation for procssing above this level
Dim Intro,Outro,Check   ' Manage confirmation dialogs
Dim PB,Prog,Debug       ' Control the progress bar
Dim Clock,T1,T2,Timing  ' The secret of great comedy
Dim Named,Source        ' Control use on named playlist
Dim Playlist,List       ' Name for any generated playlist, and the object itself
Dim iTunes              ' Handle to iTunes application
Dim Tracks              ' A collection of track objects
Dim Count               ' The number of tracks
Dim D,M,P,S,U,V         ' Counters
Dim nl,tab              ' New line/tab strings
Dim IDs                 ' A dictionary object used to ensure each object is processed once
Dim Rev                 ' Control processing order, usually reversed
Dim Quit                ' Used to abort script
Dim Title,Summary       ' Text for dialog boxes

' =======================
' Initialise user options
' =======================
' Custom values for this script
' Modified 2013-02-04
Intro=True              ' Set false to skip initial prompts, avoid if non-reversible actions
Outro=True              ' Produce summary report
Check=True              ' Track-by-track confirmation
Prog=True               ' Display progress bar
Debug=True              ' Include any debug messages in progress bar
Timing=True             ' Display running time in summary report
Named=False             ' Force script to process specific playlist rather than current selection or playlist
Source=""               ' Named playlist to process, use "Library" for entire library

Title="Embed Folder Art"
Summary="Embed largest image stored in the same folder as the file." & vbCrLf & vbCrLf _
  & "Do not use if tracks from different albums may be stored in the same folder."

Dim FSO,WIA
Set FSO=CreateObject("Scripting.FileSystemObject")      ' File System Object
Set WIA=CreateObject("WIA.ImageFile")                   ' Windows Image Acquisition


' ============
' Main program
' ============

GetTracks               ' Set things up
ProcessTracks 	        ' Main process 
Report                  ' Summary

' ===================
' End of main program
' ===================


' ===============================
' Declare subroutines & functions
' ===============================


' Note: The bulk of the code in this script is concerned with making sure that only suitable tracks are processed by
'       the following module and supporting numerous options for track selection, confirmation, progress and results.


' Embed largest artwork found in local folder
' Modified 2013-02-26
Sub Action(T)
  Dim Art,iA
  With T
    StartEvent                  ' Time potentially slow event
    If .Artwork.Count=1 Then    ' Erase any downloaded artwork
      ' Begin error handler  
      On Error Resume Next
      If .Artwork.Item(1).IsDownloadedArtwork Then
        iA=FSO.GetParentFolderName(.Location) & "\iTunesArt"
        Select Case .Artwork.Item(1).Format
        Case 1
          iA=iA & ".jpg"
        Case 2
          iA=iA & ".png"
        Case 3
          iA=iA & ".bmp"
        Case Else
          iA=""
        End Select
        If iA<>"" Then .Artwork.Item(1).SaveArtworkToFile iA    ' Save any downloaded artwork as iTunesArt.ext
        .Artwork.Item(1).Delete
      End If
      If Err.Number<>0 Then 'Ignore error
        'R=MsgBox("Error: &" & Hex(Err.Number) & " " & Err.Description & nl & "while deleting image from:" & nl & T.Location,vbExclamation+vbOKCancel,Title)
        'If R=vbCancel Then wscript.quit
        Err.Clear
      End If
      On Error Goto 0
      ' End error handler             
    End If
    Art=GetFolderArt(FSO.GetParentFolderName(.Location))
    If .Artwork.Count=0 Then   ' Embed selected artwork file
      ' Begin error handler  
      On Error Resume Next
      .AddArtworkFromFile(Art)
      If Err.Number<>0 Then 'Ignore error
        R=MsgBox("Error: &" & Hex(Err.Number) & " " & Err.Description & nl & "while deleting image from:" & nl & T.Location,vbExclamation+vbOKCancel,Title)
        If R=vbCancel Then wscript.quit
        Err.Clear
      Else
        U=U+1                   ' Increment updated tracks
      End If
      On Error Goto 0
      ' End error handler             
    End If  
    StopEvent                   ' Show event time
  End With
End Sub


' Get largest artwork file in folder
' Modified 2013-02-26
Function GetFolderArt(Folder)
  Dim Ext,File,MaxPath,MaxSize,Name,S,Size
  MaxPath=""
  For Each File in FSO.GetFolder(Folder).Files
    S=InstrRev(File.Name,".")
    If S>0 Then
      Ext=LCase(Mid(File.Name,S))
      If Instr(".bmp.jpeg.jpg.png",Ext)>0 Then
        Name=LCase(File.Name)
        WIA.LoadFile File.Path
        Size=WIA.Width * WIA.Height
        If Size>MaxSize Or (Size=MaxSize And Name="folder.jpg") Then
          MaxPath=File.Path
          MaxSize=Size
        End If  
      End If
    End If
  Next
  GetFolderArt=MaxPath
End Function


' Custom info message for progress bar
' Modified 2012-09-11
Function Info(T)
  On Error Resume Next
  Dim A,B
  With T
    A=.AlbumArtist & "" : If A="" Then A=.Artist & "" : If A="" Then A="Unknown Artist"
    B=.Album & "" : If B="" Then B="Unknown Album"
    Info="Checking: " & A & " - " & B & " - " & .Name
    If Err.Number>0 Then
      MsgBox "Problem with item " & .Name,0,Title
    End If
  End With
End Function


' Custom prompt for track-by-track confirmation
' Modified 2013-02-05
Function Prompt(T)
  Dim AA,AL,DC,DN,TN,P
  With T
    AA=.AlbumArtist & "" : If AA="" Then AA=.Artist & "" : If AA="" Then AA="Unknown Artist"
    AL=.Album & "" : If AL="" Then AL="Unknown Album"
    DN=.DiscNumber
    DC=.DiscCount
    TN=.TrackNumber
    P="Export artwork data for:" & nl & AA & " - " & AL & nl
    If TN>0 Then
      If DN>1 Or (DN>0 And DC>1) Then P=P & DN & "-"
      P=P & TN & " "
    End If
    P=P & .Name & "?" & nl
  End With
  Prompt=P
End Function


' Custom status message for progress bar
' Modified 2011-10-21
Function Status(N)
  Status="Processing " & N & " of " & Count
End Function


' Test for tracks which can be usefully updated
' Modified 2013-02-27
Function Updateable(T)
  Dim ID
  ID=PersistentID(T)
  Updateable=False              ' Default position
  If IDs.Exists(ID) Then        ' Ignore tracks already processed
    D=D+1                       ' Increment duplicate tracks
  Else
    IDs.Add ID,0                ' Note ID to prevent reprocessing this track
    If T.Artwork.Count=1 Then
      If T.Artwork.Item(1).IsDownloadedArtwork Then Updateable=True
    Else
      If T.Artwork.Count=0 Then
        If LCase(Right(T.Location,4))<>".wav" Then Updateable=True
      End If
    End If
  End If
End Function


' ============================================
' Reusable Library Routines for iTunes Scripts
' ============================================
' Modified 2012-12-18


' Format time interval from x.xxx seconds to hh:mm:ss
' Modified 2011-11-07
Function FormatTime(T)
  If T<0 Then T=T+86400         ' Watch for timer running over midnight
  If T<2 Then
    FormatTime=FormatNumber(T,3) & " seconds"
  ElseIf T<10 Then
    FormatTime=FormatNumber(T,2) & " seconds"
  ElseIf T<60 Then
    FormatTime=Int(T) & " seconds"
  Else
    Dim H,M,S
    S=T Mod 60
    M=(T\60) Mod 60             ' \ = Div operator for integer division
    'S=Right("0" & (T Mod 60),2)
    'M=Right("0" & ((T\60) Mod 60),2)  ' \ = Div operator for integer division
    H=T\3600
    If H>0 Then
      FormatTime=H & Plural(H," hours "," hour ") & M & Plural(M," mins"," min")
      'FormatTime=H & ":" & M & ":" & S
    Else
      FormatTime=M & Plural(M," mins "," min ") & S & Plural(S," secs"," sec")
      'FormatTime=M & " :" & S
      'If Left(FormatTime,1)="0" Then FormatTime=Mid(FormatTime,2)
    End If
  End If
End Function


' Initialise track selections, quit script if track selection is out of bounds or user aborts
' Modified 2012-12-18
Sub GetTracks
  Dim Q,R
  ' Initialise global variables
  nl=vbCrLf : tab=Chr(9) : Quit=False
  D=0 : M=0 : P=0 : S=0 : U=0 : V=0
  ' Initialise global objects
  Set IDs=CreateObject("Scripting.Dictionary")
  Set iTunes=CreateObject("iTunes.Application")
  Set Tracks=iTunes.SelectedTracks      ' Get current selection
  If iTunes.BrowserWindow.SelectedPlaylist.Source.Kind<>1 And Source="" Then Source="Library" : Named=True      ' Ensure section is from the library source
  'If iTunes.BrowserWindow.SelectedPlaylist.Name="Ringtones" And Source="" Then Source="Library" : Named=True    ' and not ringtones (which cannot be processed as tracks???)
  If iTunes.BrowserWindow.SelectedPlaylist.Name="Radio" And Source="" Then Source="Library" : Named=True        ' or radio stations (which cannot be processed as tracks)
  If iTunes.BrowserWindow.SelectedPlaylist.Name=Playlist And Source="" Then Source="Library" : Named=True       ' or a playlist that will be regenerated by this script
  If Named Or Tracks Is Nothing Then    ' or use a named playlist
    If Source<>"" Then Named=True
    If Source="Library" Then            ' Get library playlist...
      Set Tracks=iTunes.LibraryPlaylist.Tracks
    Else                                ' or named playlist
      On Error Resume Next              ' Attempt to fall back to current selection for non-existent source
      Set Tracks=iTunes.LibrarySource.Playlists.ItemByName(Source).Tracks
      On Error Goto 0
      If Tracks is Nothing Then         ' Fall back
        Named=False
        Source=iTunes.BrowserWindow.SelectedPlaylist.Name
        Set Tracks=iTunes.SelectedTracks
        If Tracks is Nothing Then
          Set Tracks=iTunes.BrowserWindow.SelectedPlaylist.Tracks
        End If
      End If
    End If
  End If  
  If Named And Tracks.Count=0 Then      ' Quit if no tracks in named source
    If Intro Then MsgBox "The playlist " & Source & " is empty, there is nothing to do.",vbExclamation,Title
    WScript.Quit
  End If
  If Tracks.Count=0 Then Set Tracks=iTunes.LibraryPlaylist.Tracks
  If Tracks.Count=0 Then                ' Can't select ringtones as tracks?
    MsgBox "This script cannot process " & iTunes.BrowserWindow.SelectedPlaylist.Name & ".",vbExclamation,Title
    WScript.Quit
  End If
  ' Check there is a suitable number of suitable tracks to work with
  Count=Tracks.Count
  If Count<Min Or (Count>Max And Max>0) Then
    If Max=0 Then
      MsgBox "Please select " & Min & " or more tracks in iTunes before calling this script!",0,Title
      WScript.Quit
    Else
      MsgBox "Please select between " & Min & " and " & Max & " tracks in iTunes before calling this script!",0,Title
      WScript.Quit
    End If
  End If
  ' Check if the user wants to proceed and how
  Q=Summary
  If Q<>"" Then Q=Q & nl & nl
  If Warn>0 And Count>Warn Then
    Intro=True
    Q=Q & "WARNING!" & nl & "Are you sure you want to process " & Count & " tracks"
    If Named Then Q=Q & nl
  Else
    Q=Q & "Process " & Count & " track" & Plural(Count,"s","")
  End If
  If Named Then Q=Q & "from the " & Source & " playlist"
  Q=Q & "?"
  If Intro Or (Prog And UAC) Then
    If Check Then
      Q=Q & nl & nl 
      Q=Q & "Yes" & tab & "Process track" & Plural(Count,"s","") & " automatically" & nl
      Q=Q & "No" & tab & "Preview & confirm each action" & nl
      Q=Q & "Cancel" & tab & "Abort script"
    End If
    If Kimo Then Q=Q & nl & nl & "NB: Disable ''Keep iTunes Media folder organised'' preference before use."
    If Prog And UAC Then
      Q=Q & nl & nl & "NB: Disable User Access Control to allow progess bar to operate" & nl
      Q=Q & "or change the declaration ''Prog=True'' to ''Prog=False''."
      Prog=False
    End If
    If Check Then
      R=MsgBox(Q,vbYesNoCancel+vbQuestion,Title)
    Else
      R=MsgBox(Q,vbOKCancel+vbQuestion,Title)
    End If
    If R=vbCancel Then WScript.Quit
    If R=vbYes or R=vbOK Then
      Check=False
    Else
      Check=True
    End If
  End If 
  If Check Then Prog=False      ' Suppress progress bar if prompting for user input
End Sub


' Return the persistent object representing the track from its ID as a string
' Modified 2012-09-05
Function ObjectFromID(ID)
  Set ObjectFromID=iTunes.LibraryPlaylist.Tracks.ItemByPersistentID(Eval("&H" & Left(ID,8)),Eval("&H" & Right(ID,8)))
End Function


' Create a string representing the 64 bit persistent ID of an iTunes object
' Modified 2012-08-24
Function PersistentID(T)
  PersistentID=Right("0000000" & Hex(iTunes.ITObjectPersistentIDHigh(T)),8) & "-" & Right("0000000" & Hex(iTunes.ITObjectPersistentIDLow(T)),8)
End Function


' Return the persistent object representing the track, with exceptions for apps/games, streams & ringtones
' Keeps hold of an object that might vanish from a smart playlist as it is updated
' Modified 2012-10-17
Function PersistentObject(T)
  Dim K
  K=T.KindAsString
  If Instr(K," app") Or Instr("Internet audio stream/iPod game/Ringtone",K) Then  ' Ringtones seem to be invisible to scripts!
    Set PersistentObject=T
  Else
    Set PersistentObject=iTunes.LibraryPlaylist.Tracks.ItemByPersistentID(iTunes.ITObjectPersistentIDHigh(T),iTunes.ITObjectPersistentIDLow(T))
  End If  
End Function


' Return relevant string depending on whether value is plural or singular
' Modified 2011-10-04
Function Plural(V,P,S)
  If V=1 Then Plural=S Else Plural=P
End Function


' Format a list of values for output
' Modified 2012-08-25
Function PrettyList(L,N)
  If L="" Then
    PrettyList=N & "."
  Else
    PrettyList=Replace(Left(L,Len(L)-1)," and" & nl,"," & nl) & " and" & nl & N & "."
  End If
End Function


' Loop through track selection processing suitable items
' Modified 2012-12-18
Sub ProcessTracks
  Dim C,I,N,Q,R,T
  Dim First,Last,Steps
  If IsEmpty(Rev) Then Rev=True
  If Rev Then
    First=Count : Last=1 : Steps=-1
  Else
    First=1 : Last=Count : Steps=1
  End If
  N=0
  If Prog Then                  ' Create ProgessBar
    Set PB=New ProgBar
    PB.SetTitle Title
    PB.Show
  End If
  Clock=0 : StartTimer
  For I=First To Last Step Steps        ' Usually work backwards in case edit removes item from selection
    N=N+1                 
    If Prog Then
      PB.SetStatus Status(N)
      PB.Progress N-1,Count
    End If
    Set T=Tracks.Item(I)
    Set T=PersistentObject(T)   ' Attach to object in library playlist
    If Prog Then PB.SetInfo Info(T)
    If T.Kind=1 Then            ' Ignore tracks which can't change
      If Updateable(T) Then     ' Ignore tracks which won't change
        If Check Then           ' Track by track confirmation
          Q=Prompt(T)
          StopTimer             ' Don't time user inputs 
          R=MsgBox(Q,vbYesNoCancel+vbQuestion,Title)
          StartTimer
          Select Case R
          Case vbYes
            C=True
          Case vbNo
            C=False
            S=S+1               ' Increment skipped tracks
          Case Else
            Quit=True
            Exit For
          End Select          
        Else
          C=True
        End If
        If C Then               ' We have a valid track, now do something with it
          Action T
        End If
      End If
    End If 
    P=P+1                       ' Increment processed tracks
    If Quit Then Exit For       ' Abort loop on user request
  Next
  StopTimer
  If Prog And Not Quit Then
    PB.Progress Count,Count
    WScript.Sleep 250
  End If
  If Prog Then PB.Close
End Sub


' Output report
' Modified 2012-08-25
Sub Report
  If Not Outro Then Exit Sub
  Dim L,T
  L=""
  If Quit Then T="Script aborted!" & nl & nl Else T=""
  T=T & P & " track" & Plural(P,"s","")
  If P<Count Then T=T & " of " & Count
  T=T & Plural(P," were"," was") & " processed of which " & nl
  If D>0 Then L=PrettyList(L,D & Plural(D," were duplicates"," was a duplicate") & " in the list")
  If V>0 Then L=PrettyList(L,V & " did not need updating")
  If U>0 Or V=0 Then L=PrettyList(L,U & Plural(U," were"," was") & " updated")
  If S>0 Then L=PrettyList(L,S & Plural(S," were"," was") & " skipped")
  If M>0 Then L=PrettyList(L,M & Plural(M," were"," was") & " missing")
  T=T & L
  If Timing Then 
    T=T & nl & nl
    If Check Then T=T & "Processing" Else T=T & "Running"
    T=T & " time: " & FormatTime(Clock)
  End If
  MsgBox T,vbInformation,Title
End Sub


' Start timing event
' Modified 2011-10-08
Sub StartEvent
  T2=Timer
End Sub


' Start timing session
' Modified 2011-10-08
Sub StartTimer
  T1=Timer
End Sub


' Stop timing event and display elapsed time in debug section of Progress Bar
' Modified 2011-11-07
Sub StopEvent
  If Prog Then
    T2=Timer-T2
    If T2<0 Then T2=T2+86400            ' Watch for timer running over midnight
    If Debug Then PB.SetDebug "<br>Last iTunes call took " & FormatTime(T2) 
  End If  
End Sub


' Stop timing session and add elapased time to running clock
' Modified 2011-10-08
Sub StopTimer
  Clock=Clock+Timer-T1
  If Clock<0 Then Clock=Clock+86400     ' Watch for timer running over midnight
End Sub


' Detect if User Access Control is enabled, UAC prevents use of progress bar
' Modified 2011-10-18
Function UAC
  Const HKEY_LOCAL_MACHINE=&H80000002
  Const KeyPath="Software\Microsoft\Windows\CurrentVersion\Policies\System"
  Const KeyName="EnableLUA"
  Dim Reg,Value
  Set Reg=GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\default:StdRegProv") 	  ' Use . for local computer, otherwise could be computer name or IP address
  Reg.GetDWORDValue HKEY_LOCAL_MACHINE,KeyPath,KeyName,Value	  ' Get current property
  If IsNull(Value) Then UAC=False Else UAC=(Value<>0)
End Function


' Wrap & tab long strings, break string S after at least B characters on next character C adding T tabs to each new line
' Modified 2012-12-18
Function Wrap(S,B,C,T)
  Dim P
  P=Instr(B,S,C)
  If P Then Wrap=Left(S,P) & nl & String(T,tab) & Wrap(Mid(S,P+1),B,C,T) Else Wrap=S
End Function


' ==================
' Progress Bar Class
' ==================

' Progress/activity bar for vbScript implemented via IE automation
' Can optionally rebuild itself if closed or abort the calling script
' Modified 2012-10-17
Class ProgBar
  Public Cells,Height,Width,Respawn,Title,Version
  Private Active,Blank,Dbg,Filled(),FSO,IE,Info,NextOn,NextOff,Status,SHeight,SWidth,Temp

' User has closed progress bar, abort or respwan?
' Modified 2011-10-09
  Public Sub Cancel()
    If Respawn And Active Then
      Active=False
      If Respawn=1 Then
        Show                    ' Ignore user's attempt to close and respawn
      Else
        Dim R
        StopTimer               ' Don't time user inputs 
        R=MsgBox("Abort Script?",vbExclamation+vbYesNoCancel,Title)
        StartTimer
        If R=vbYes Then
          On Error Resume Next
          CleanUp
          Respawn=False
          Quit=True             ' Global flag allows main program to complete current task before exiting
        Else
          Show                  ' Recreate box if closed
        End If  
      End If        
    End If
  End Sub

' Delete temporary html file  
' Modified 2011-10-04
  Private Sub CleanUp()
    FSO.DeleteFile Temp         ' Delete temporary file
  End Sub
  
' Close progress bar and tidy up
' Modified 2011-10-04
  Public Sub Close()
    On Error Resume Next        ' Ignore errors caused by closed object
    If Active Then
      Active=False              ' Ignores second call as IE object is destroyed
      IE.Quit                   ' Remove the progess bar
      CleanUp
    End If    
 End Sub
 
' Initialize object properties
' Modified 2012-09-05
  Private Sub Class_Initialize()
    Dim I,Items,strComputer,WMI
    ' Get width & height of screen for centering ProgressBar
    strComputer="."
    Set WMI=GetObject("winmgmts:\\" & strComputer & "\root\cimv2")
    Set Items=WMI.ExecQuery("Select * from Win32_OperatingSystem",,48)
    'Get the OS version number (first two)
    For Each I in Items
      Version=Left(I.Version,3)
    Next
    Set Items=WMI.ExecQuery ("Select * From Win32_DisplayConfiguration")
    For Each I in Items
      SHeight=I.PelsHeight
      SWidth=I.PelsWidth
    Next
    If Debug Then
      Height=160                ' Height of containing div
    Else
      Height=120                ' Reduce height if no debug area
    End If
    Width=300                   ' Width of containing div
    Respawn=True                ' ProgressBar will attempt to resurect if closed
    Blank=String(50,160)        ' Blanks out "Internet Explorer" from title
    Cells=25                    ' No. of units in ProgressBar, resize window if using more cells
    ReDim Filled(Cells)         ' Array holds current state of each cell
    For I=0 To Cells-1
      Filled(I)=False
    Next
    NextOn=0                    ' Next cell to be filled if busy cycling
    NextOff=Cells-5             ' Next cell to be cleared if busy cycling
    Dbg="&nbsp;"                ' Initital value for debug text
    Info="&nbsp;"               ' Initital value for info text
    Status="&nbsp;"             ' Initital value for status text
    Title="Progress Bar"        ' Initital value for title text
    Set FSO=CreateObject("Scripting.FileSystemObject")          ' File System Object
    Temp=FSO.GetSpecialFolder(2) & "\ProgBar.htm"               ' Path to Temp file
  End Sub

' Tidy up if progress bar object is destroyed
' Modified 2011-10-04
  Private Sub Class_Terminate()
    Close
  End Sub
 
' Display the bar filled in proportion X of Y
' Modified 2011-10-18
  Public Sub Progress(X,Y)
    Dim F,I,L,S,Z
    If X<0 Or X>Y Or Y<=0 Then
      MsgBox "Invalid call to ProgessBar.Progress, variables out of range!",vbExclamation,Title
      Exit Sub
    End If
    Z=Int(X/Y*(Cells))
    If Z=NextOn Then Exit Sub
    If Z=NextOn+1 Then
      Step False
    Else
      If Z>NextOn Then
        F=0 : L=Cells-1 : S=1
      Else
        F=Cells-1 : L=0 : S=-1
      End If
      For I=F To L Step S
        If I>=Z Then
          SetCell I,False
        Else
          SetCell I,True
        End If
      Next
      NextOn=Z
    End If
  End Sub

' Clear progress bar ready for reuse  
' Modified 2011-10-16
  Public Sub Reset
    Dim C
    For C=Cells-1 To 0 Step -1
      IE.Document.All.Item("P",C).classname="empty"
      Filled(C)=False
    Next
    NextOn=0
    NextOff=Cells-5   
  End Sub
  
' Directly set or clear a cell
' Modified 2011-10-16
  Public Sub SetCell(C,F)
    On Error Resume Next        ' Ignore errors caused by closed object
    If F And Not Filled(C) Then
      Filled(C)=True
      IE.Document.All.Item("P",C).classname="filled"
    ElseIf Not F And Filled(C) Then
      Filled(C)=False
      IE.Document.All.Item("P",C).classname="empty"
    End If
  End Sub 
 
' Set text in the Dbg area
' Modified 2011-10-04
  Public Sub SetDebug(T)
    On Error Resume Next        ' Ignore errors caused by closed object
    Dbg=T
    IE.Document.GetElementById("Debug").InnerHTML=T
  End Sub

' Set text in the info area
' Modified 2011-10-04
  Public Sub SetInfo(T)
    On Error Resume Next        ' Ignore errors caused by closed object
    Info=T
    IE.Document.GetElementById("Info").InnerHTML=T
  End Sub

' Set text in the status area
' Modified 2011-10-04
  Public Sub SetStatus(T)
    On Error Resume Next        ' Ignore errors caused by closed object
    Status=T
    IE.Document.GetElementById("Status").InnerHTML=T
  End Sub

' Set title text
' Modified 2011-10-04
  Public Sub SetTitle(T)
    On Error Resume Next        ' Ignore errors caused by closed object
    Title=T
    IE.Document.Title=T & Blank
  End Sub
  
' Create and display the progress bar  
' Modified 2012-10-17
  Public Sub Show()
    Const HKEY_CURRENT_USER=&H80000001
    Const KeyPath="Software\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_LOCALMACHINE_LOCKDOWN"
    Const KeyName="iexplore.exe"
    Dim File,I,Reg,State,Value
    Set Reg=GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\default:StdRegProv") 	' Use . for local computer, otherwise could be computer name or IP address
    'On Error Resume Next        ' Ignore possible errors
    ' Make sure IE is set to allow local content, at least while we get the Progress Bar displayed
    Reg.GetDWORDValue HKEY_CURRENT_USER,KeyPath,KeyName,Value	' Get current property
    State=Value	 							  ' Preserve current option
    Value=0		    							' Set new option 
    Reg.SetDWORDValue HKEY_CURRENT_USER,KeyPath,KeyName,Value	' Update property
    'If Version<>"5.1" Then Prog=False : Exit Sub      ' Need to test for Vista/Windows 7 with UAC
    Set IE=WScript.CreateObject("InternetExplorer.Application","Event_")
    Set File=FSO.CreateTextFile(Temp, True)
    With File
      .WriteLine "<!doctype html>"
      '.WriteLine "<!-- saved from url=(0014)about:internet -->"       ' Old "Mark of the web"
      .WriteLine "<!-- saved from url=(0016)http://localhost -->"      ' New "Mark of the web"
      .WriteLine "<html><head><title>" & Title & Blank & "</title>"
      .WriteLine "<style type='text/css'>"
      .WriteLine ".border {border: 5px solid #DBD7C7;}"
      .WriteLine ".debug {font-family: Tahoma; font-size: 8.5pt;}"
      .WriteLine ".empty {border: 2px solid #FFFFFF; background-color: #FFFFFF;}"
      .WriteLine ".filled {border: 2px solid #FFFFFF; background-color: #00FF00;}"
      .WriteLine ".info {font-family: Tahoma; font-size: 8.5pt;}"
      .WriteLine ".status {font-family: Tahoma; font-size: 10pt;}"
      .WriteLine "</style>"
      .WriteLine "</head>"
      .WriteLine "<body scroll='no' style='background-color: #EBE7D7'>"
      .WriteLine "<div style='display:block; height:" & Height & "px; width:" & Width & "px; overflow:hidden;'>"
      .WriteLine "<table border-width='0' cellpadding='2' width='" & Width & "px'><tr>"
      .WriteLine "<td id='Status' class='status'>" & Status & "</td></tr></table>"
      .WriteLine "<table class='border' cellpadding='0' cellspacing='0' width='" & Width & "px'><tr>"
      ' Write out cells
      For I=0 To Cells-1
	      If Filled(I) Then
          .WriteLine "<td id='p' class='filled'>&nbsp;</td>"
        Else
          .WriteLine "<td id='p' class='empty'>&nbsp;</td>"
        End If
      Next
	    .WriteLine "</tr></table>"
      .WriteLine "<table border-width='0' cellpadding='2' width='" & Width & "px'><tr><td>"
      .WriteLine "<span id='Info' class='info'>" & Info & "</span><br>"
      .WriteLine "<span id='Debug' class='debug'>" & Dbg & "</span></td></tr></table>"
      .WriteLine "</div></body></html>"
    End With
    ' Create IE automation object with generated HTML
    With IE
      .width=Width+30           ' Increase if using more cells
      .height=Height+55         ' Increase to allow more info/debug text
      If Version>"5.1" Then     ' Allow for bigger border in Vista/Widows 7
        .width=.width+10
        .height=.height+10
      End If        
      .left=(SWidth-.width)/2
      .top=(SHeight-.height)/2
      .navigate "file://" & Temp
      '.navigate "http://samsoft.org.uk/progbar.htm"
      .addressbar=False
      .menubar=False
      .resizable=False
      .toolbar=False
      On Error Resume Next      
      .statusbar=False          ' Causes error on Windows 7 or IE 9
      On Error Goto 0
      .visible=True             ' Causes error if UAC is active
    End With
    Active=True
    ' Restore the user's property settings for the registry key
    Value=State		    					' Restore option
    Reg.SetDWORDValue HKEY_CURRENT_USER,KeyPath,KeyName,Value	  ' Update property 
    Exit Sub
  End Sub
 
' Increment progress bar, optionally clearing a previous cell if working as an activity bar
' Modified 2011-10-05
  Public Sub Step(Clear)
    SetCell NextOn,True : NextOn=(NextOn+1) Mod Cells
    If Clear Then SetCell NextOff,False : NextOff=(NextOff+1) Mod Cells
  End Sub

' Self-timed shutdown
' Modified 2011-10-05 
  Public Sub TimeOut(S)
    Dim I
    Respawn=False                ' Allow uninteruppted exit during countdown
    For I=S To 2 Step -1
      SetDebug "<br>Closing in " & I & " seconds" & String(I,".")
      WScript.sleep 1000
    Next
      SetDebug "<br>Closing in 1 second."
      WScript.sleep 1000
    Close
  End Sub 
    
End Class


' Fires if progress bar window is closed, can't seem to wrap up the handler in the class
' Modified 2011-10-04
Sub Event_OnQuit()
  PB.Cancel
End Sub


' ==============
' End of listing
' ==============