# Spark bundles its own Hadoop dependencies by default, which overrides your local Hadoop installation (HADOOP_HOME).
# If the below Hadoop version doesn't match the installed version there could be problems
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

print("Spark version:", spark.version)
print("Hadoop version:", spark.sparkContext._jvm.org.apache.hadoop.util.VersionInfo.getVersion())