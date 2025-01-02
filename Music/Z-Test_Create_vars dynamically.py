Pos = []
Arq = []
Art = []
Title = []
AA = []
Album = []
Year = []
Genre = []
Covers = []
# CREATES LISTS FROM THE COLUMNS OF THE DF DYNAMICALLY 
for col_name in col_names:
    exec(f"{col_name} = df['{col_name}'].tolist()")