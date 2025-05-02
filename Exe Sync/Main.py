# THIS IS THE MAIN CODE THAT CALLS THE FORM CODE
# WHICH WAS DESIGNED SEPARATELY IN WxFormBuilder
# IT WILL ALSO CALL THE OTHER CODES

import wx
from GUI_form import MainFrame1  # Import the generated GUI

from threading import Thread

import sys
sys.path.insert(0, "D:\\Python\\iTunes")
sys.path.insert(0, "D:\\Python\\WMP")

from Read_PL import Init_iTunes, Create_PL, Add_track_to_PL, Read_xml, unpack_PID, order_list
from WMP_Read_PL import Read_WMP_PL, Init_wmp, order_list_wmp, WMP_tag_dict

from os.path import exists

import pandas as pd

# COLS THAT MATTER FOR THIS PGM 
col_names =  ["Arq", "Plays", "ID"]

# RESIZES THE FORM: bSizer1.Add(self.OutputWindowCtrl, 1, wx.EXPAND | wx.ALL, 5)  (In case form code is overwritten)

# THIS MODULE SETS ARQ TO LOWER CASE FOR THE MERGER
# IT ALSO DEDUPES THE DUPLICATE RECORDS
def df_dedupe(source,df):
    # LOWERCASE THE FILE NAME
    #df["Arq"] = df["Arq"].str.lower()
    df.loc[:, "Arq"] = df["Arq"].str.lower()

    # ADDS KEY COL. TO DF
    # df["max_Plays_" + source]
    df.loc[:, "max_Plays_" + source] = df.groupby("Arq")["Plays"].transform("max")

    start_rows = df.shape[0]
    # Eliminate duplicate records based on "Arq" (subset=df["Arq"].str.lower() also works)
    df_dedupe = df.drop_duplicates(subset="Arq", keep="first")
    end_rows = df_dedupe.shape[0]
    print("\nThe",source,"df has",start_rows,"tracks before deduping (",end_rows,"after)")

    dict = {}
    dict["start_rows"] = start_rows
    dict["end_rows"] = end_rows
    dict["DF"] = df_dedupe
    return dict

# MAIN CODE
def read_iTunes(rows=None):
    # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
    iTu_col_names = col_names[:]
    iTu_col_names.append("PID")
    iTu_dict = Read_xml(iTu_col_names,rows=rows)
    
    # ASSIGNS VARS
    iTu_App = iTu_dict["App"]
    iTu_df = iTu_dict["DF"]
    # MAKES A COPY OF THE ORIGINAL PATH LIST ("ARQ")
    iTu_df["Location"] = iTu_df["Arq"].copy()
    # LOWERCASE THE FILE NAME
    iTu_df["Arq"] = iTu_df["Arq"].str.lower()

    plus_miss_rows = iTu_df.shape[0]
    
    Found = [exists(x) for x in iTu_df["Location"]]
    iTu_df["Found"] = Found

    print("\nThe iTunes df has",Found.count(False),"missing tracks")

    # SEL ONLY FOUND FILES
    iTu_df = iTu_df[iTu_df["Found"] == True]
    
    # DROPS DUPES
    print("\nDeduping iTunes df, this may take a while...")
    dict = df_dedupe("iTunes", iTu_df)
    iTu_df = dict["DF"]
    iTu_start_rows = dict["start_rows"]
    iTu_end_rows = dict["end_rows"]


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame1(None)
        self.frame.Show()
        # Add this flag
        self.iTunes_launched = False  
        # ADDS A DICTIONARY TO THE CLASS THAT WILL BE USED TO RETURN VALUES (IN ONE OF THE FUNCTIONS)
        self.result = {}
        
        # Bind button click
        self.frame.btn_Sync.Bind(wx.EVT_BUTTON, self.on_button_click)
        return True

    # THE PURPOSE OF HAVING THE FUNCTION HERE IS SO THE GUI DOESN'T FREEZE
    # WHEN IT'S RUNNING AND MESSAGES ARE DISPLAYED IN THE GUI AS IT RUNS
    # SINCE THIS FUNCTION WILL EXECUTE FROM A THREAD, IT CAN'T RETURN VALUES
    # RETURNED VALUES WILL BE IN THE CLASS
    def Read_WMP_library(self, rows):
        # INIT WMP
        dict = Init_wmp()
        wmp = dict['WMP']
        library = dict['Library']

        # THIS IS THE LIBRARY
        numtracks = len(library) 
        PL_name = "library"
        PL_nbr = 0

        # PROCESS SPECIFIED NUMBER OF ROWS
        if rows is None:
           numtracks = len(library)   
        else:
            numtracks = min(rows, len(library))
        
        # data IS A LIST OF LISTS
        data = []
        wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Reading the WMP music library")
        wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"\ntracks: ",library.Count,"(processing",numtracks,")")

        # LOGIC TO DISPLAY IN THE LOG
        tam = max(numtracks // 20, 1)
        
        # ORDER LIST SO COLUMN HEADERS ALWAYS MATCH THEIR VALUES
        col_names = order_list(col_names,order_list=order_list_wmp)
        # THE RANGE FOR ITEMS IN A WMP PL IS 0 TO (N-1)
        for m in range(numtracks):
            track = library[m]    
            
            # ONLY DOES AUDIO
            if track.getiteminfo("MediaType")=="audio":
                # THE SOURCE (PLAYLIST/LIBRARY)
                tag_list = [PL_nbr,PL_name]
                # THE TRACK POSITION
                tag_list.append(m)
                dict = WMP_tag_dict(track,col_names)
                for key in col_names:
                    value = dict[key]
                    tag_list.append(value)
                #ADD ROW TO LIST, BEFORE CREATING DF
                data.append(tag_list)
                if (m+1) % tam==0:
                    # print("Row no: ",m+1)
                    wx.CallAfter(self.frame.OutputWindowCtrl.SetValue, f"Processed {m} of {numtracks} files...")

        # DATAFRAME
        # ADDS COL. PL IF IT WASN'T INCLUDED JUST SO ALL COLS. ALIGN
        if "PL_nbr" not in col_names:
            col_names.append("PL_nbr") 
        if "PL_name" not in col_names:
            col_names.append("PL_name")
        if "Pos" not in col_names:
            col_names.append("Pos")    
        # ORDER THE LIST SO COLUMN HEADERS MATCH THEIR VALUES
        col_names = order_list(col_names,order_list=order_list_wmp)
        df = pd.DataFrame(data, columns=col_names)

        # RETURN ALL RELEVANT OBJS
        self.result['WMP'] = wmp
        self.result['Lib'] = library
        self.result['DF'] = df
        # dict = {"WMP": wmp, "Lib": library, "DF": df}
        # return dict

    def on_button_click(self, event):
        # Assuming OutputWindowCtrl is a wx.TextCtrl, access it and set the message
        output_text_ctrl = self.frame.OutputWindowCtrl  # Replace with the correct reference to your TextCtrl

        # RADIO BOX: Get the selected radio box index and value (string)
        selected_index = self.frame.RadioBoxOptions.GetSelection()
        selected_radio = self.frame.RadioBoxOptions.GetStringSelection()

        # Display the message
        message = f"\nRadio Box Selected: {selected_radio} (Index: {selected_index})"

        # Now write to the output_text_ctrl
        output_text_ctrl = self.frame.OutputWindowCtrl  # Reference to the TextCtrl
        output_text_ctrl.AppendText(message)  # Display the message

        # DON'T DO ANYTHING IF iTunes ALREADY LAUNCHED
        if self.iTunes_launched:
           output_text_ctrl.SetValue("iTunes already launched.")
        
        # Only launch try iTunes once
        if not self.iTunes_launched:        
           output_text_ctrl.SetValue("Launching iTunes...")  # This writes the message into the TextCtrl

           # LAUCH ITUNES (THIS IS JUST TO TEST IF iTunes CAN BE LAUNCHED
           dict = Init_iTunes() 
           success = dict["Success"]

           # THE WHOLE iTunes PROCESS HAS TO HAPPEN HERE 
           if success:
              self.iTunes_launched = True
              iTu_col_names = col_names[:]
              iTu_col_names.append("PID")

              output_text_ctrl.SetValue("Parsing the iTunes XML...")
              iTu_dict = Read_xml(iTu_col_names,rows=None)

              # ASSIGNS VARS
              iTu_App = iTu_dict["App"]
              iTu_df = iTu_dict["DF"]
              # MAKES A COPY OF THE ORIGINAL PATH LIST ("ARQ")
              iTu_df["Location"] = iTu_df["Arq"].copy()
              # LOWERCASE THE FILE NAME
              iTu_df["Arq"] = iTu_df["Arq"].str.lower()

              # FILES COUNT  
              iTunes_tracks = iTu_df.shape[0]
              output_text_ctrl.SetValue(f"iTunes has {iTunes_tracks} tracks")

              # CHECKING DEAD TRACKS
              output_text_ctrl.SetValue("Checking for missing iTunes tracks")               
              Found = [exists(x) for x in iTu_df["Location"]]
              iTu_df["Found"] = Found

              miss_tracks = Found.count(False)
              output_text_ctrl.SetValue(f"iTunes has {miss_tracks} missing tracks")

              # SELECTS ONLY FOUND FILES
              iTu_df = iTu_df[iTu_df["Found"] == True]
                
              # DROPS DUPES
              output_text_ctrl.SetValue("Deduping iTunes tracks (this may take a while)")
              dict = df_dedupe("iTunes", iTu_df)
              output_text_ctrl.SetValue("Deduping iTunes finished...")
              iTu_df = dict["DF"]
              iTu_start_rows = dict["start_rows"]
              iTu_end_rows = dict["end_rows"]

              # THIS PART IS MORE COMPLICATED BECAUSE I NEED TO SHOW PROGRESS
              thread = Thread(target=self.Read_WMP_library, args=(100,))
              thread.start()  # Starts the task only at this point

               # Wait for the thread to finish before getting the returned values
              thread.join()

              # WMP ASSIGNING
              wmp_df = self.result["DF"]
              # USED IF INPUT IS THE WHOLE LIBRARY
              WMP_lib = self.result["Lib"]
              # USED IF INPUT IS A PLAYLIST (BASED ON iTunes)
              WMP_player = self.result["WMP"]
            
              # CHANGE DF-ELIMINATE DUPES
              print("\nDeduping WMP df, this may take a while...")
              dict = df_dedupe("WMP",wmp_df)
              wmp_df = dict["DF"]
              wmp_start_rows = dict["start_rows"]
              wmp_end_rows = dict["end_rows"]

              wmp_df = wmp_df.rename(columns={"Pos": "WMP_Pos"})
        
              # JOIN THE DATAFRAMES [["Arq", "max_Plays_iTunes", "ID", "Location"]]
              df = iTu_df.merge(wmp_df[["Arq", "max_Plays_WMP", "WMP_Pos"]], on="Arq", how="inner")  
           
           
           if not success:
              output_text_ctrl.SetValue("Can't launch iTunes...(close it and retry)")
               

           # CALLS Read_PL FUNCTION ,Do_lib=True,rows=10
        
# START OF THE CODE
app = MyApp()
app.MainLoop()
