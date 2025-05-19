from pyspark.sql import SparkSession
import os

# Setup the Configuration from code
# import pyspark
# conf = pyspark.SparkConf()
# conf.set("spark.driver.port", "56010")
# conf.set("spark.blockManager.port", "56020")

# Not needed anymore
# os.environ["JAVA_HOME"] = "C:/Program Files/Eclipse Adoptium/jdk-11.0.27.6-hotspot"
# os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"  # Force localhost


# BELOW ENSURES ALL LOCAL MACHINE CORES ARE USED 
# Here it can be local[1] for 1 core (N for N cores, * for ALL)
spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

# Create a SparkSession
# spark = SparkSession.builder.master("local[*]").config("spark.hadoop.fs.defaultFS", "file:///").getOrCreate()

# ONLY DISPLAY ERRORS (OFF FOR NOTHING)
spark.sparkContext.setLogLevel("ERROR")

# DEBUG 
# spark.sparkContext.setLogLevel("DEBUG")


# CHECK CONFIGS
conf = spark.sparkContext.getConf()
list = conf.getAll()
for i in range(len(list)):
    print(i, list[i])

print("\n\n")    
#print(spark.sparkContext.getConf().getAll())

# DOES IT WORK?
# df = spark.createDataFrame([(1, "test")], ["id", "value"])
# df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\Output\\AAA_csv")

# Syntax below is spark.createDataFrame(data, schema)
df = spark.createDataFrame([(1, "test")], ["id", "value"])

# Show top 5 rows
# df.show(5) 
print("\n\nNUMBER OF ROWS",df.count())

# df.coalesce(1).write.mode("overwrite").csv("D:\\Python\\PySpark\\output_csv")

# sample_data = [{"name": "John    D.", "age": 30},
#   {"name": "Alice   G.", "age": 25},
#   {"name": "Bob  T.", "age": 35},
#   {"name": "Eve   A.", "age": 28}]

# df = spark.createDataFrame(sample_data)
# df.show()

# Add Data
# data = ([(1580, "John", "Doe", "Mars" ),
# (5820, "Jane", "Doe", "Venus"),
# (2340, "Kid1", "Doe", "Jupyter"),
# (7860, "Kid2", "Doe", "Saturn")
# ])

# Setup the Data Frame / Display the Data Frame
# user_data_df = spark.createDataFrame(data, ["id", "first", "last", "planet"])
# user_data_df.show()

# input("Press Enter to exit...")
spark.stop()

os._exit(0)