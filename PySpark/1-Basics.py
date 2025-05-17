from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()

# Access SparkContext from SparkSession
sc = spark.sparkContext

# Create a large list of numbers
nums = list(range(0,1001))

# Spark distributes the data across multiple machines or cluster

# Parallelize (take a python list and distribute into an rdd - resilient distributed dataset)
# sc is short for SparkContext

# The below syntax won't work with a serverless Notebook in Databricks
# In databricks with an attached cluster sc should be recognized right away
# Needs to create and attach a cluster for this to work
nums_rdd = sc.parallelize(nums)

# Using lambda functions with the list
rdd = sc.parallelize([1, 2, 3, 4])
rdd_squared = rdd.map(lambda x: x * x)
print(rdd_squared.collect())  # Output: [2, 4, 6, 8]


# Shows a subset of the RDD list
nums_rdd.take(5)

# Another example, with a tuple

pairs = rdd_squared.map(lambda x: (x, len(str(x))))

# Shows pairs
pairs.take(5)

# Filter certain elements from the list 
# Selects pairs where the number of digits of the first element is even
even_dig_pairs = pairs.filter(lambda x: x[1] % 2==0)

# Flip the created pairs
flip_pairs = pairs.map(lambda x: (x[1], x[0]))