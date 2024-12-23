# READS AN EXCEL FILE 
# RUNS CMDS WITH INPUTS FROM THE EXCEL FILE

from os.path import exists, isfile
import subprocess
import Excel


# MAIN CODE
def Runs_cmd(PL_name=None,PL_nbr=None):
    # OPENS EXCEL FILE
    Excel_file = "D:\\Videos\\Novelas\\2o_video\\Novelas80s-2o video.xlsx"
    # Excel_file = "D:\\Videos\\Novelas\\House\\House.xlsx"
    excelf = Excel.open_excel(Excel_file,"iTunes")

    worksheet = excelf["sheet"]
    headers = excelf["headers"]

    rows = Excel.last_row(worksheet)-1

    # Artist	Title	Type
    Path_col = Excel.col_number(headers,"Tema")
    Time_col = Excel.col_number(headers,"Time")
    #Novela_col = col_number(headers,"Novela")

    next_row = 1
    nbr = 0
    while next_row+1 <= rows+1:
          next_row = next_row+1
          Path_value = worksheet.cell(row=next_row, column=Path_col).value
          Time_value = worksheet.cell(row=next_row, column=Time_col).value
          if exists(Path_value): 
             nbr = nbr+1
             
             # D:\Videos\Novelas\2o_video\Audios
             output = "D:\\Videos\\Novelas\\2o_video\\Audios\\" + str(nbr) + ".mp3"
             print("\nFile",Path_value,"\\ Output:",output)

             # TIME
             if Time_value is None:
                time_str = ""
             else:
                 time_str = "-ss " + Time_value   

             # CHECK IF ALREADY EXISTS #and nbr not in [64]
             if not exists(output):
                cmd = "C:\\ffmpeg\\bin\\ffmpeg.exe -i \""+ Path_value +"\" " + time_str + " -t 20 -y \"" + output + "\""
                print("\nRunning:",cmd)

                # Run the command
                process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                # Print the output and any errors
                print(process.stdout)
                print(process.stderr)
             
   
# CALLS FUNC
Runs_cmd()
 
                   






