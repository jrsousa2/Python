from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# Start Spark session (Databricks does this automatically)
spark = SparkSession.builder.getOrCreate()

# Load sample data (e.g., from a Delta table or CSV)
df = spark.read.csv("dbfs:/mnt/logistics/deliveries.csv", header=True, inferSchema=True)

# Let's say the dataset has: 'distance_km', 'delivery_time_min', 'weather_delay', 'is_late'
# A logistics regression usually uses categorical variables with multiple levels (levels with rare freqs can be grouped)

# Prepare features
assembler = VectorAssembler(
    inputCols=["distance_km", "delivery_time_min", "weather_delay"],
    outputCol="features"
)
data = assembler.transform(df)

# Train/test split
train, test = data.randomSplit([0.8, 0.2], seed=42)

# Fit logistic regression model
lr = LogisticRegression(featuresCol="features", labelCol="is_late")
model = lr.fit(train)

# Predict on test set
predictions = model.transform(test)

# Evaluate
evaluator = BinaryClassificationEvaluator(labelCol="is_late")
auc = evaluator.evaluate(predictions)
print(f"AUC: {auc:.3f}")
