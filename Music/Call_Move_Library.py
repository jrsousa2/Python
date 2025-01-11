# READS THE ITUNES XML LIBRARY FILE TO OBTAIN INFO ON MISSING TRACKS LOCATION
# REASSIGNS THE TRACKS TO MOVE LIBRARY TO ANOTHER DRIVE
# IN THIS VERSION IT USES THE XLM FILE TO IDENTIFY MISSING ID'S
# IT DOESN'T MOVE THE FILES AS IT GOES

import xml.etree.ElementTree as ET
from pandas import DataFrame
from urllib.parse import unquote
from os.path import exists
from struct import unpack
from binascii import a2b_hex
import Read_PL

# XML COLS THAT WE WANT TO KEEP 'Track ID' "Total Time"
keep_lst = ["Location","Artist","Name","Persistent ID"]

# READS XML LIBRARY
def parse_itunes_library_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    tracks = []
    for dict_entry in root.findall("./dict/dict/dict"):
        track = {}
        iter_elem = iter(dict_entry)
        for elem in iter_elem:
            if elem.tag == "key":
                key = elem.text
                next_elem = next(iter_elem)
                if key in keep_lst:
                   if key == "Location":
                       # Extract only the file path from the location URL
                       location = next_elem.text.split("file://localhost")[1]
                       location = location.lstrip("/")
                       track[key] = unquote(location)
                   else:
                       track[key] = next_elem.text
        tracks.append(track)
    
    return tracks

def xml_to_dataframe(xml_file):
    tracks = parse_itunes_library_xml(xml_file)
    return DataFrame(tracks)

# TO SHORTEN FUNCTION CALLS 
# Just replaces the current drive with the new one
def Cur_to_new(file,Cur_drive,Dest_drive):
    file = file[0].upper() + file[1:]
    return file.replace("/", "\\").replace(Cur_drive+":\\", Dest_drive+":\\")

dict = Read_PL.Init_iTunes()
App = dict['App']
#Sources = dict['Sources'] 
#Lib = dict["Lib"]
PLs = dict['PLs']

# Get the path to the iTunes Library XML file
lib_xml_path = App.LibraryXMLPath
# The iTunes folder is the parent directory of the Library XML file
iTunes_folder = lib_xml_path.rsplit('\\', 1)[0]

if exists(lib_xml_path):
   # THIS PART READS THE XML FILE
   print("Reading XML (this may take a while...)")
   df = xml_to_dataframe(lib_xml_path)
    # Keep only columns on the list
   df = df.reindex(columns=keep_lst)

   # Display the first source that was read, the XML file
   print("\nThe XML df has",df.shape[0],"tracks")

   # PRINT
   print("\nXML samples...first 5 files")
   print(df.head())

   # LIST CREATION (list comprehension) 
   Arq = [x for x in df["Location"]]
   Art = [x for x in df['Artist']]
   Title = [x for x in df['Name']]
   PID = [x for x in df["Persistent ID"]]

    # GETS INPUT FROM USER
   Cur_drive = input("\nEnter the old drive: ")
   Cur_drive = Cur_drive.upper().strip()
   Dest_drive = input("\nEnter the new drive: ")
   Dest_drive = Dest_drive.upper().strip()

   # COUNTS HOW MANY FILES CAN BE UPDATED
   # THEY ARE IN NOT THE CURRENT DRIVE BUT ARE IN THE DESTINATION DRIVE 
   Check_drive = [i for i, file in enumerate(Arq) if exists(Cur_to_new(file,Cur_drive,Dest_drive)) and not exists(Arq[i])]
   max_files = len(Check_drive)

   nbr_files = max_files
   nbr_files_inp = input(f"\nNumber of files to update (max {max_files}) (blank for ALL): ")
   if nbr_files_inp != "":
      try:
         nbr_files = max(int(nbr_files_inp), max_files)
      except:
         nbr_files = max_files

   # PLAYLIST WITH MIGRATED FILES
   if nbr_files>0:
      migrated_PL = "Updt_location"
      call_PL = Read_PL.Create_PL(migrated_PL,recreate="n")
      print("\nUpdating file location from drive",Cur_drive,"to",Dest_drive)

   # LOOP
   cnt = 0
   miss = 0
   up_to_date = 0
   found = [1] * len(Arq)
   for j in range(nbr_files):
       i = Check_drive[j]
       New_loc = Cur_to_new(Arq[i],Cur_drive,Dest_drive)
       m = unpack('!ii', a2b_hex(PID[i]))
       track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
       if exists(New_loc) and not exists(Arq[i]) and Art[i]==track.Artist and Title[i]==track.Name:
          print("Updating",j+1,"of",nbr_files,":",Arq[i],"-> ",Dest_drive + ":\\")
          track.location = New_loc
          Read_PL.Add_track_to_PL(PLs,migrated_PL,track)
          cnt = cnt + 1
       elif exists(New_loc):
          up_to_date = up_to_date+1
       else:
          miss = miss+1
          found[i] = 0

   print("\n\nUpdated",cnt,"of",nbr_files,"(",miss,"not found)")
   print(up_to_date,"files already up-to-date")
   input("Press Enter to continue...")
   #df["Found"] = found

   # TO SAVE DEAD TRACKS TO EXCEL
#    print("\nSaving dead tracks to Excel...")
#    if exists("D:\\iTunes\\Excel"):
#       file_nm = "D:\\iTunes\\Excel\\Dead_tracks.xlsx"
#    else:  
#        file_nm = iTunes_folder + "\\Dead_tracks.xlsx"

   # save the dataframe to an Excel file
   # df_dead = df[ df["Found"] == 0]
   # UNCOMMENT IF YOU WANT TO SAVE DEAD TRACKS INFO
   # df_dead.to_excel(file_nm, index=False)
