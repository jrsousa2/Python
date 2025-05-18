# THIS IS MOSTLY TO TEST THE INPUT DATA
# AND THE SPEED / PERFORMANCE 
# LAZY COMPUTATION CAN MAKE DSPARK IN WINDOWS FULL OF BUGS
# UDF's (USER DEFINED FUNCTIONS TOO)
from pyspark.sql import SparkSession

from pyspark.sql.functions import when, col

from pyspark.ml.feature import VectorAssembler


import os

# Start Spark session (Databricks does this automatically)
# spark = SparkSession.builder.getOrCreate()

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

# TAKE ONLY 100 ROWS OF THE SPARK DF
# new_spark_df = df.limit(100)
# SPARK df's CAN BE SHOWN BUT NOT PANDAS
# new_spark_df.show(5)

# # DOES IT WORK?
# new_spark_df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\output_csv")

# # IF NEED TO SAVE THE FILE IN PARQUET FORMAT (COLUMNAR FORMAT)
# new_spark_df.write.mode("overwrite").parquet("D:\\Python\\PySpark\\output.parquet")

# DO A TEST WITH SOME COLS.
# assembler = VectorAssembler(
#     inputCols=["NumberOfOpenCreditLinesAndLoans", "NumberOfTimes90DaysLate", "NumberRealEstateLoansOrLines"],
#     outputCol="features"
# )

# # TRANSFORMS DATA (SHOULD ADD ONE COL TO THE DATA)
# spark_data = assembler.transform(df)


# Convert first 100 rows to pandas DataFrame
# new_pandas_df = spark_data.limit(100).toPandas()

# # # Save to Excel
# new_pandas_df.to_excel("D:\\Python\\PySpark\\100_samples_new2.xlsx", index=False)


# # Show top 5 rows
# Convert first 100 rows to pandas DataFrame
new_pandas_df = df.limit(100).toPandas()
print(new_pandas_df.head(5))

# DISPLAYS SOME STATS ABOUT THE FILE
# new_df = df.describe().show()
# Save to Excel
# new_pandas_df.to_excel("D:\\Python\\PySpark\\Summary.xlsx", index=False)

# input("Press Enter to exit...")
spark.stop()

os._exit(0)