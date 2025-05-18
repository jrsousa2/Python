# THIS IS MOSTLY TO TEST THE INPUT DATA
# AND THE SPEED / PERFORMANCE 
from pyspark.sql import SparkSession

from pyspark.sql.functions import when, col

from pyspark.ml.feature import VectorAssembler


import os

# Start Spark session (Databricks does this automatically)
spark = SparkSession.builder.getOrCreate()

# Load sample data (e.g., from a Delta table or CSV)
# df = spark.read.csv("dbfs:/mnt/logistics/deliveries.csv", header=True, inferSchema=True)

# From a CSV file
df = spark.read.csv("D:\\Python\\PySpark\\Data\\Credit_Risk.csv", header=True, inferSchema=True)

# CONVERTS COL. NAMES DASHES TO _
df = df.toDF(*[col.replace("-", "_") for col in df.columns])

# df = df.select([
#     when(col(c) == "NA", None).otherwise(col(c)).alias(c)
#     for c in df.columns
# ])

# CONVERTS TO NUMERIC COLS
df = df.select([
    when(col(c) == "NA", None)
    .otherwise(col(c))
    .cast("double")
    .alias(c)
    for c in df.columns
])

# DO A TEST WITH SOME COLS.
assembler = VectorAssembler(
    inputCols=["NumberOfOpenCreditLinesAndLoans", "NumberOfTimes90DaysLate", "NumberRealEstateLoansOrLines"],
    outputCol="features"
)

# TRANSFORMS DATA (SHOULD ADD ONE COL TO THE DATA)
data = assembler.transform(df)


# Convert first 100 rows to pandas DataFrame
new_df = data.limit(100).toPandas()

# # Save to Excel
new_df.to_excel("D:\\Python\\PySpark\\100_samples_new2.xlsx", index=False)

# IF NEED TO SAVE THE FILE IN PARQUET FORMAT (COLUMNAR FORMAT)
new_df.write.parquet("D:\\Python\\PySpark\\output.parquet")

# # Show top 5 rows
# df.show(5) 

# DISPLAYS SOME STATS ABOUT THE FILE
# new_df = df.describe().show()
# Save to Excel
# new_df.to_excel("D:\\Python\\PySpark\\Summary.xlsx", index=False)

# input("Press Enter to exit...")
spark.stop()

os._exit(0)