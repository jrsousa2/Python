# CODE TAKES EXCEL FILE AS INPUT
import pandas as pd

def char_2_num(pmt):
    try:
       v = float(pmt)
    except Exception:
       v=0
    return v

df = pd.read_excel(r'D:\\Python\\File.xlsx')
#df = pd.DataFrame(df_rd, columns= ['id','detail'])

# SHOWS THE IMPORTED FILE 
print("First")
print(df)

# COMPREHENSION LISTS
ids = [x for x in df['order_id']]
dets = [x for x in df['order_detail']]


col1 = []
col2 = []
for i in range(0,len(dets)):
    count = dets[i].count(",")+1 
    recs1 = count * [ ids[i] ]
    col1 = col1 + recs1
    recs2 = dets[i].split(",")
    col2 = col2 + recs2

# CREATES COLS.
product =[]	
units = []	
price = []
for i in range(0,len(col2)):
    recs3 = col2[i].split(";")
    count = col2[i].count(";")
    if count==3:
        product.append(recs3[1])
        units.append(char_2_num(recs3[2]))
        price.append(char_2_num(recs3[3]))
    else:
        product.append(recs3[0])
        units.append(char_2_num(recs3[1]))
        price.append(char_2_num(recs3[2]))

# NEW DF
zipped = list(zip(col1, product, units, price))
new_df = pd.DataFrame(zipped, columns = ['order_id','product', 'units', 'price'])

print("Second")
print(new_df)


