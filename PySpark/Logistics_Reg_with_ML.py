# Spark ML treats all numeric cols as continuous by default.
# If you want to treat a numeric column as discrete (categorical), you need to:
# Convert it to a categorical feature, often by converting it to a string type first, then using StringIndexer to create category indices.
# Or use OneHotEncoder on the indexed column to create dummy variables.
# Spark ML does not automatically treat numeric columns as discrete categories, even if they represent categories encoded as numbers.
# Summary:
# Numeric columns = continuous by default.
# For categorical behavior, explicitly index and encode them as categories.

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Start Spark session (Databricks does this automatically)
spark = SparkSession.builder.getOrCreate()

# Load sample data (e.g., from a Delta table or CSV)
# df = spark.read.csv("dbfs:/mnt/logistics/deliveries.csv", header=True, inferSchema=True)

# From a CSV file
df = spark.read.csv("D:\\Python\\PySpark\\Data\\Credit_Risk.csv", header=True, inferSchema=True)

# CONVERTS COL. NAMES DASHES TO _
df = df.toDF(*[col.replace("-", "_") for col in df.columns])


# Show top 5 rows
df.show(5) 

# DISPLAYS SOME STATS ABOUT THE FILE
df.describe().show()

# ALL THE ABOVE AND min, max, mean, stddev, count
df.summary().show()

# BELOW WOULD SAVE THE DF TO CSV FILES (number of file depends on the size of the cluster)
# df.write.csv("output.csv", header=True)

# IF A SINGLE FILE IS NEEDED THE MULTIPLE PARTS FROM THE MULTIPLE NODES CAN BE COMBINED 
# BUT BE CAREFUL, THIS CAN BE SLOW IF THERE'S TOO MUCH DATA
# df.coalesce(1).write.csv("output.csv", header=True)


# IF NEED TO SAVE THE FILE IN PARQUET FORMAT
# df.write.parquet("output.parquet")



# Let's say the dataset has: 'distance_km', 'delivery_time_min', 'weather_delay', 'is_late'
# A logistics regression usually uses categorical variables with multiple levels (levels with rare freqs can be grouped)

# Prepare features (creates a new column thru the concatenation of inputCols and saves it as new col called features
assembler = VectorAssembler(
    inputCols=["distance_km", "delivery_time_min", "weather_delay"],
    outputCol="features"
)

data = assembler.transform(df)

# Train/test split
train, test = data.randomSplit([0.8, 0.2], seed=42)

# Fit logistic regression model (labelCol is the response variable, featuresCol the predictors (a vector)
LR = LogisticRegression(featuresCol="features", labelCol="is_late")
model = LR.fit(train)

# Predict on test set
predictions = model.transform(test)

# Evaluate
evaluator = BinaryClassificationEvaluator(labelCol="is_late")
auc = evaluator.evaluate(predictions)
print(f"AUC: {auc:.3f}")
