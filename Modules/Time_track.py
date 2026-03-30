from timeit import default_timer
from datetime import datetime

# START OF THE CODE
elapsed_time = 0
start_time = default_timer()

start_time_act = datetime.now()
print("\nStart time:", start_time_act)

# TIME FINAL
end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time,"\n")  