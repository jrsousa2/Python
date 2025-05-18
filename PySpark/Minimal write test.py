from pyspark.sql import SparkSession
import os

import os

# BELOW ENSURES ALL LOCAL MACHINE CORES ARE USED
# spark = SparkSession.builder.master("local").appName("MyApp").getOrCreate()

spark = SparkSession.builder.master("local[*]").config("spark.hadoop.fs.defaultFS", "file:///").getOrCreate()

# spark = SparkSession.builder \
#     .master("local[*]") \
#     .appName("MyApp") \
#     .config("spark.executor.memory", "1g") \
#     .getOrCreate()

# DEBUG 
spark.sparkContext.setLogLevel("DEBUG")

# DOES IT WORK?
# Syntax below is spark.createDataFrame(data, schema)
df = spark.createDataFrame([(1, "test")], ["id", "value"])

# Show top 5 rows
# df.show(5) 
print("NUMBER OF ROWS",df.count())


# df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\output_csv")

# input("Press Enter to exit...")
spark.stop()

os._exit(0)