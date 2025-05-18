from pyspark.sql import SparkSession

from pyspark.sql.functions import when, col


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


# Convert first 100 rows to pandas DataFrame
new_df = df.limit(100).toPandas()

# # Save to Excel
new_df.to_excel("D:\\Python\\PySpark\\100_samples_new.xlsx", index=False)

# # Show top 5 rows
# df.show(5) 

# DISPLAYS SOME STATS ABOUT THE FILE
# new_df = df.describe().show()
# Save to Excel
# new_df.to_excel("D:\\Python\\PySpark\\Summary.xlsx", index=False)

# input("Press Enter to exit...")
spark.stop()

os._exit(0)