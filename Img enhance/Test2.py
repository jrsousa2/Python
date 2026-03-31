from datetime import datetime
import os

now = datetime.now()

mask = "%Y-%m-%d_%H-%M-%S"
str_now = now.strftime(mask)

test = datetime.strptime(str_now, mask)

print(str_now,test)

file = "F:\\Videos\\Pobres\\Test\\Test1.png"

TS = os.path.getmtime(file)

mod_time = datetime.fromtimestamp(TS)

Hora = datetime.strptime('2026-03-30_15-07-51', "%Y-%m-%d_%H-%M-%S")

print(TS,mod_time,Hora)