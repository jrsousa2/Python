import os
os.environ["JAVA_HOME"] = "C:/Program Files/Eclipse Adoptium/jdk-11.0.27.6-hotspot"
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"  # Force localhost

from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .master("local[1]") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

# DOES IT WORK?
df = spark.createDataFrame([(1, "test")], ["id", "value"])
df.coalesce(1).write.mode("overwrite").csv("D:/AAA_csv")

print("Success!")