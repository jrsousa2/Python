# READS THE ITUNES XML FILES TO OBTAIN INFO ON MISSING TRACKS LOCATION
# REASSIGNS THE TRACKS TO MOVE LIBRARY TO ANOTHER DRIVE
# IN THIS VERSION IT USES THE XLM FILE TO IDENTIFY MISSING ID'S
# IT DOESN'T MOVE THE FILES AS IT GOES

from os.path import exists

# from sys import path
# path.insert(0, r"D:\Python\iTunes")

from Read_PL import Init_iTunes, Create_PL, Add_track_to_PL, Read_xml, unpack_PID
from tkinter import StringVar, Button, Tk, Label
from tkinter import ttk, messagebox


# TO SHORTEN FUNCTION CALLS 
# Just replaces the current drive with the new one
def Cur_to_new(file,Cur_drive,Dest_drive):
    file = file[0].upper() + file[1:]
    return file.replace("/", "\\").replace(Cur_drive+":\\", Dest_drive+":\\")

def launch_iTunes():
    global App
    global PLs
    global lib_xml_path

    dict = Init_iTunes()
    App = dict['App']
    PLs = dict['PLs']
    lib_xml_path = dict['Lib_XML_path']

def Migrate(df,Old_drive,New_drive):
    # LIST CREATION (list comprehension) 
    Arq = [x for x in df["Location"]]

    # COUNTS HOW MANY FILES CAN BE UPDATED
    # THEY ARE NOT IN THE CURRENT DRIVE BUT ARE IN THE DESTINATION DRIVE 
    Check_drive = [i for i, file in enumerate(Arq) if exists(Cur_to_new(file,Old_drive,New_drive)) and not exists(Arq[i])]
    max_files = len(Check_drive)

    # GETS INPUT FROM USER
    nbr_files_label = ttk.Label(root, text=f"Number of files to update (max {max_files}) (Hit Enter):")
    nbr_files_label.pack(pady=5)

    nbr_files_var = StringVar()
    nbr_files_entry = ttk.Entry(root, textvariable=nbr_files_var)
    nbr_files_entry.pack(pady=5)
    root.update()

    # Bind Enter key press event to the Entry widget
    nbr_files_entry.bind('<Return>', lambda event: Updt_loc(df,Old_drive,New_drive,Check_drive,nbr_files_var))
    #nbr_files_entry.bind('<Return>', lambda event: Updt_loc(event, param1, param2))

def val_letter_input(char):
    # Return True if char is a letter (a-z or A-Z), otherwise False
    return char.isalpha()

# Define the function to be called when the button is clicked
def on_close():
    # App.Quit()
    App = None
    root.quit()

def Updt_loc(df,Old_drive,New_drive,Check_drive,nbr_files_var):
    # LIST CREATION (list comprehension) 
    Arq = [x for x in df["Location"]]
    Art = [x for x in df['Artist']]
    Title = [x for x in df['Name']]
    PID = [x for x in df["Persistent ID"]]

    max_files = len(Check_drive)

    nbr_files = max_files
    #nbr_files_var = input(f"\nNumber of files to update (max {max_files}) (blank for ALL): ")
    if nbr_files_var != "":
       try:
          nbr_files = max(int(nbr_files_var), max_files)
       except:
          nbr_files = max_files

    # PLAYLIST WITH MIGRATED FILES
    if nbr_files>0:
       migrated_PL = "Updt_location"
       call_PL = Create_PL(migrated_PL,recreate="n")

       # Aqui ja nao esta aparecendo
       message_label = ttk.Label(root, text=f"Updating track location from {Old_drive} to {New_drive}:")
       message_label.pack(pady=10)
       root.update()
       # Update root window size based on current content
       #root.update_idletasks()  # Ensure all widgets are updated
       #root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}")  # Adjust root window size

    # LOOP
    cnt = 0
    miss = 0
    #up_to_date = 0
    for j in range(nbr_files): 
        i = Check_drive[j]
        New_loc = Cur_to_new(Arq[i],Old_drive,New_drive)
        # m = unpack('!ii', a2b_hex(PID[i]))
        m = unpack_PID(PID[i])
        track = App.LibraryPlaylist.Tracks.ItemByPersistentID(*m)
        if exists(New_loc) and not exists(Arq[i]) and Art[i]==track.Artist and Title[i]==track.Name:
           # -> {New_drive} :\\
           message_label.config(text=f"Updating {j+1} of {nbr_files}: {Arq[i]}", wraplength=400)
           root.update()  # Optionally update the root to immediately display changes
    
           track.location = New_loc
           Add_track_to_PL(PLs,migrated_PL,track)
           cnt = cnt + 1
        elif not exists(New_loc):
             miss = miss+1
    
    #print("\n\nUpdated {cnt} of {nbr_files} ({miss} not found)")
    message_label = ttk.Label(root, text=f"{cnt} updated tracks added to playlist Updt_loc")
    message_label.pack(pady=10)
    root.update()

    # Create the "Migrate" button
    End_button = Button(root, text="Close", command=on_close)
    End_button.pack(pady=10)
    # Quit or close the iTunes application
    # Display a message box and wait for user to press "OK"
    #messagebox.showinfo("Press OK to finish...")
    #root.quit()  # Close the Tkinter main loop


# MAIN PROGRAM THAT'S CALLING FUNCTIONS
# Create the main window
root = Tk()
root.title("iTunes Library Drive Migration Tool")
#root.update()

# Set root to automatically resize based on content
#root.pack_propagate(True)

# Set the size of the window (width x height)
root.geometry("400x600")

# ANTES DE INICIAR ITUNES
# messagebox.showinfo("Press Enter to Continue", "Press OK to finish...")
message_label = ttk.Label(root, text="Launching iTunes...")
message_label.pack(pady=10)
root.update()

# Create a Label widget to place at the bottom
bottom_label = Label(root, text="\u00A9 JR Sousa. All rights reserved.", bg="lightgray", fg="black", height=1)

# Pack the Label widget at the bottom of the window
bottom_label.pack(side="bottom", fill="x")

# LAUCH ITUNES
launch_iTunes()

if exists(lib_xml_path):
   message_label = ttk.Label(root, text="Reading XML (this may take a while...)")
   message_label.pack(pady=10)
   root.update()
   # READ XML
   df = Read_xml()

   # Display the first source that was read, the XML file
   message_label = ttk.Label(root, text=f"The XML has {df.shape[0]} tracks")
   message_label.pack(pady=10)
   root.update()
else:
    message_label = ttk.Label(root, text="XML file doesn't exist")
    message_label.pack(pady=10)
    root.update()

# Register validation function
vcmd = (root.register(val_letter_input), '%S')

# Label and Entry for "Old Drive"
old_drive_label = ttk.Label(root, text="Enter Old Drive:")
old_drive_label.pack(pady=5)

old_drive_var = StringVar()
old_drive_entry = ttk.Entry(root, validate="key", validatecommand=vcmd, textvariable=old_drive_var)
#ew_drive_entry = ttk.Entry(root, validate="key", validatecommand=vcmd)
old_drive_entry.pack(pady=5)

# Label and Entry for "New Drive"
new_drive_label = ttk.Label(root, text="Enter New Drive:")
new_drive_label.pack(pady=5)

new_drive_var = StringVar()
new_drive_entry = ttk.Entry(root, validate="key", validatecommand=vcmd, textvariable=new_drive_var)
new_drive_entry.pack(pady=5)
root.update()

# Create the "Migrate" button
migrate_button = Button(root, text="Update track location", command=lambda: Migrate(df,old_drive_var.get().upper(),new_drive_var.get().upper()))
# migrate_button = tk.Button(root, text="Migrate", command=migrate_action)
migrate_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
