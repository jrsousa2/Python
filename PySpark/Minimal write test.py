from pyspark.sql import SparkSession
import os

# BELOW ENSURES ALL LOCAL MACHINE CORES ARE USED
# spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

spark = SparkSession.builder.master("local[*]").config("spark.hadoop.fs.defaultFS", "file:///").getOrCreate()

# DOES IT WORK?
df = spark.createDataFrame([(1, "test")], ["id", "value"])
df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\output_csv")


# input("Press Enter to exit...")
spark.stop()

os._exit(0)