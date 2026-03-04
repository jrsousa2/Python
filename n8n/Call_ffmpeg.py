# READS AN EXCEL FILE 
# RUNS CMDS WITH INPUTS FROM THE EXCEL FILE
# THIS WILL MERGE THE VIDEOS WITH THE AUDIOS AND ADD A TITLE AT THE SAME TIME
# ONLY RUNS FFMPEG FOR VIDEOS NOT PRODUCED BEFORE

from os.path import exists
import subprocess

import sys
sys.path.insert(0, "D:\\Python\\Modules")

import Excel

# MAIN CODE
def Runs_cmd(PL_name=None,PL_nbr=None):
    # OPENS EXCEL FILE
    Excel_file = r"C:\Users\JR Sousa\Desktop\Rogue Earth.xlsx"
    # Excel_file = "D:\\Videos\\Novelas\\House\\House.xlsx"
    excelf = Excel.open_excel(Excel_file,"Sheet1")

    worksheet = excelf["sheet"]
    headers = excelf["headers"]

    rows = Excel.last_row(worksheet)-1

    # Artist	Title	Type
    SEQ_col = Excel.col_number(headers,"SEQ")
    CMD_col = Excel.col_number(headers,"CMD")

    next_row = 1
    while next_row+1 <= rows+1:
          next_row = next_row+1
          SEQ_value = worksheet.cell(row=next_row, column=SEQ_col).value
          CMD_value = worksheet.cell(row=next_row, column=CMD_col).value

          output = "D:\\Videos\\n8n\\Video_ext\\Out" + str(SEQ_value) + ".mp4"
          if not exists(output): 
             
             print("\nRunning video:",output)

             # Run the command
             process = subprocess.run(CMD_value, shell=True, capture_output=True, text=True)

             # Print the output and any errors
             print(process.stdout)
             #print(process.stderr)

# CALLS FUNC
Runs_cmd()
 
                   






