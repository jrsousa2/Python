# THIS IS MOSTLY TO TEST THE INPUT DATA AND THE SPEED / PERFORMANCE 
# ENSURE TO ENABLE ACCESS TO THE PYTHON INTEPRETER IN THE CFA (CONTROLLED FOLDER ACCESS)
# OTHERWISE FOLDER IS FOUND BUT ERROR MSG WILL SAY IT WASN'T (WHEN IN FACT IT'S THE WRITE PERMISSION)
# LAZY COMPUTATION CAN MAKE SPARK IN WINDOWS FULL OF BUGS
# UDF's (USER DEFINED FUNCTIONS TOO)
from pyspark.sql import SparkSession

from pyspark.sql.functions import when, col

import os

# BELOW ENSURES ALL LOCAL MACHINE CORES ARE USED
spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

# Load sample data (e.g., from a Delta table or CSV)
# df = spark.read.csv("dbfs:/mnt/logistics/deliveries.csv", header=True, inferSchema=True)

# CREATES A SPARK DF FROM A CSV FILE
df = spark.read.csv("D:\\Python\\PySpark\\Data\\Credit_Risk_trim.csv", header=True, inferSchema=True)

# CONVERTS DASHES IN COL. NAMES TO _
df = df.toDF(*[col.replace("-", "_") for col in df.columns])

# CONVERTS TO NUMERIC COLS
df = df.select([
    when(col(c) == "NA", None)
    .otherwise(col(c))
    .cast("double")
    .alias(c)
    for c in df.columns
])

# TAKE ONLY 10000 ROWS OF THE SPARK DF
# Convert to pandas DataFrame
pandas_df = df.limit(10000).toPandas()

# # Show top 5 rows (tail for bottom)
print(pandas_df.head(5))

# DISPLAYS SOME STATS ABOUT THE FILE
# new_df = df.describe().show()
# Save to Excel
file_nm = "D:\\Python\\PySpark\\Data\\Samples.xlsx"
if not os.path.exists(file_nm):
   pandas_df.to_excel(file_nm, index=False)

# SPARK df's CAN BE SHOWN BUT NOT PANDAS
# spark_df.show(5)

# IF A SINGLE FILE IS NEEDED THE MULTIPLE PARTS FROM THE MULTIPLE NODES CAN BE COMBINED 
# BUT BE CAREFUL, THIS CAN BE SLOW IF THERE'S TOO MUCH DATA
# spark_df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\output_csv", header=True)

# BELOW WOULD SAVE THE DF TO CSV FILES (number of file depends on the size of the cluster)
# spark_df.write.csv("output.csv", header=True)

# IF NEED TO SAVE THE FILE IN PARQUET FORMAT (COLUMNAR FORMAT)
# spark_df.write.mode("overwrite").parquet("D:\\Python\\PySpark\\output.parquet")

# input("Press Enter to exit...")
spark.stop()

os._exit(0)