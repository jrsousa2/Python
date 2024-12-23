# READS AN EXCEL FILE 
# RUNS CMDS WITH INPUTS FROM THE EXCEL FILE

from os.path import exists, isfile
import subprocess
import Excel
from genderize import Genderize
import time


# MAIN CODE
def Runs_cmd(PL_name=None,PL_nbr=None):
    # OPENS EXCEL FILE
    Excel_file = "D:\\Videos\\Atrizes BR\\Actor list.xlsx"
    # Excel_file = "D:\\Videos\\Novelas\\House\\House.xlsx"
    excelf = Excel.open_excel(Excel_file,"Atores")

    worksheet = excelf["sheet"]
    headers = excelf["headers"]

    rows = Excel.last_row(worksheet)-1

    # Artist	Title	Type
    Ator_col = Excel.col_number(headers,"Ator")
    Gender_col = Excel.col_number(headers,"Gender")
    Prob_col = Excel.col_number(headers,"Prob")
    #Novela_col = col_number(headers,"Novela")

    next_row = 1
    nbr = 0
    while next_row+1 <= rows+1:
          next_row = next_row+1
          Ator_nm = worksheet.cell(row=next_row, column=Ator_col).value
          gender_value = worksheet.cell(row=next_row, column=Gender_col).value
          print("Checking",next_row-1,"of",rows-1,":",Ator_nm)
          if gender_value is None and Ator_nm !="":
            try:
                check0 = Genderize().get([Ator_nm]) # , country_id="BR"
                time.sleep(2)
            except:
                pass  
            else:  
                if check0[0]['gender']=="female":
                    gender = "F"
                else:
                    gender = "M"   
                prob = check0[0]['probability']
                print("Actor:",Ator_nm,"Gender:",gender,"Prob:",prob)
                worksheet.cell(row=next_row, column=Gender_col, value=gender)
                worksheet.cell(row=next_row, column=Prob_col, value=prob)
                if next_row % 20==0:
                    excelf["file"].save(Excel_file) 
   
# CALLS FUNC
Runs_cmd()
 
                   






