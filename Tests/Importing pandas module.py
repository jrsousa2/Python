# importing pandas module
import pandas as pd
  
# making data frame
data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")
  
# PRINT NUMBER OF ROWS
print("Number of recs",len(data.index),"number of cols",len(data.columns),"\n")

print("INFO SOBRE O ARQ \n")
# print("\n")
print(data.info())

# calling head() method 
# storing in new variable
data_top = data.head()
  
# display
data_top