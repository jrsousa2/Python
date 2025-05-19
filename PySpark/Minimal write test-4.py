# Import Libraries
import pyspark
from pyspark.sql import SparkSession

# Setup the Configuration
conf = pyspark.SparkConf()
sc = SparkSession.builder.getOrCreate()

# Add Data
data = ([(1580, "John", "Doe", "Mars" ),
(5820, "Jane", "Doe", "Venus"),
(2340, "Kid1", "Doe", "Jupyter"),
(7860, "Kid2", "Doe", "Saturn")
])

# Setup the Data Frame
user_data_df = sc.createDataFrame(data, ["id", "first", "last", "planet"])

# Display the Data Frame
user_data_df.show()