# READS AN EXCEL SHEET WITH TEXTS TO CONVERT TO AUDIO
# THERE ARE 20 TEXTS TO BE CONVERTED TO AUDIO

# BELOW IS NEEDED BC 
import asyncio
import edge_tts

from os.path import exists
 
import sys
sys.path.insert(0, "D:\\Python\\Modules")

import Excel

async def main(Seq, text):
    output = "audio" + str(Seq) + ".mp3"
    path = "D:\\Videos\\n8n\\Sound\\" + output
    if not exists(path):
       tts = edge_tts.Communicate(text, voice="pt-BR-AntonioNeural", rate="+10%") # , rate="+50%"
       await tts.save(path)

# MAIN CODE
async def Creates_audio():

    # OPENS EXCEL FILE TO READ FROM (WRITES TO THE SAME FILE)
    Excel_infile = r"C:\Users\JR Sousa\Desktop\Rogue Earth.xlsx"
    # Excel_outfile = r"D:\Videos\Atrizes BR\Atrizes_out.xlsx"
    excelf = Excel.open_excel(Excel_infile,"Sheet1")
    workbook = excelf["file"]
    worksheet = excelf["sheet"]
    headers = excelf["headers"]
    rows = Excel.last_row(worksheet)-1

    # TEXT TO BE TRANSLATED
    Text_col = Excel.col_number(headers,"PT")
    Seq_col = Excel.col_number(headers,"SEQ")

    # LOOP        
    next_row = 1 # rows+1
    while next_row+1 <= rows + 1:
          next_row = next_row+1
          Text_value = worksheet.cell(row=next_row, column=Text_col).value
          Seq_value = worksheet.cell(row=next_row, column=Seq_col).value
          await main(Seq_value, Text_value)

             
# CALLS FUNC
asyncio.run(Creates_audio())

# asyncio.run(main())