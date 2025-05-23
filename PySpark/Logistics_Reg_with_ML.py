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

from pyspark.sql.functions import when, col
from pyspark.sql.types import IntegerType

# from os.path import exists

# Start Spark session (Databricks does this automatically)
# spark = SparkSession.builder.getOrCreate()
spark = SparkSession.builder.master("local[*]").appName("MyApp").getOrCreate()

# Load sample data (e.g., from a Delta table or CSV)
# df = spark.read.csv("dbfs:/mnt/logistics/deliveries.csv", header=True, inferSchema=True)

labelCol="SeriousDlqin2yrs"
outputCol="features"

# SUMMARIZES THE DF OVER ACTUAL AND PREDICTED 
# def actual_vs_pred_summary(df_predictions):
#     return (
#         df_predictions.groupBy(labelCol, "prediction")
#         .count()
#         .orderBy(labelCol, "prediction")
#     )

def actual_vs_pred_summary(df_predictions):
    return (
        df_predictions
        .withColumn(labelCol, col(labelCol).cast(IntegerType()))
        .withColumn("prediction", col("prediction").cast(IntegerType()))
        .groupBy(labelCol, "prediction")
        .count()
        .orderBy(labelCol, "prediction")
    )


# SUMMARIZES A SPARK DF AND SAVES TO
def sum_pdf(df):
    sum_pdf = df.describe().toPandas()

    # Format numeric columns to 2 decimal places
    for col in sum_pdf.columns[1:]:  # skip the 'summary' column
        sum_pdf[col] = sum_pdf[col].astype(float).round(2)

    # TRANSPOSES DF
    sum_pdf = sum_pdf.set_index('summary').T.reset_index()    

    # Save as CSV or Excel
    file_nm = "D:\\Python\\PySpark\\Data\\Describe_fmt.xlsx"
    sum_pdf.to_excel(file_nm, index=False)


# From a CSV file
df = spark.read.csv("D:\\Python\\PySpark\\Data\\Credit_Risk.csv", header=True, inferSchema=True)

# LIMIT DF TO 10000 ROWS
# df = df.limit(10000)

# CONVERTS COL. NAMES DASHES TO _
df = df.toDF(*[col.replace("-", "_") for col in df.columns])

# CONVERTS TO NUMERIC COLS
df = df.select([
    when(col(c) == "NA", None)
    .otherwise(col(c))
    .cast("double")
    .alias(c)
    for c in df.columns
])

# Show top 5 rows
# df.show(5) 

# DISPLAYS SOME STATS ABOUT THE FILE
# df.describe().show()
# df.describe().coalesce(1).write.csv("D:\\Python\\PySpark\\Data\\Describe", header=True, mode="overwrite")
sum_pdf(df)

# ALL THE ABOVE AND min, max, mean, stddev, count
# df.summary().show()

# Let's say the dataset has: 'distance_km', 'delivery_time_min', 'weather_delay', 'is_late'
# A logistics regression usually uses categorical variables with multiple levels (levels with rare freqs can be grouped)

inputCols = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30_59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60_89DaysPastDueNotWorse",
    "NumberOfDependents"
]

# Prepare features (creates a new column thru the concatenation of inputCols and saves it as new col called features
assembler = VectorAssembler(
    inputCols=inputCols,
    outputCol=outputCol,
    handleInvalid="skip"
)

# ADDS THE VECTOR COL. TO THE SPARK DF
data = assembler.transform(df)

# Convert to pandas DataFrame to check data
# pandas_df = data.toPandas()

# Save to Excel
file_nm = "D:\\Python\\PySpark\\Data\\Check_file.xlsx"
# if not exists(file_nm):
#    pandas_df.to_excel(file_nm, index=False)

# Train/test split (see is used for random split))
train, test = data.randomSplit([0.8, 0.2], seed=42)

# Fit logistic regression model
# labelCol is the response variable 
# featuresCol the predictors (a vector)
LR = LogisticRegression(featuresCol=outputCol, labelCol=labelCol)
model = LR.fit(train)

# Predict on test set
predictions = model.transform(test)

# Evaluate ROC curve 
# The iconic area under the ROC curve is a measure of the goodness-of-fit of the model
evaluator = BinaryClassificationEvaluator(labelCol=labelCol)
auc = evaluator.evaluate(predictions)
print(f"AUC: {auc:.3f}")

# Summary for train
train_summary = actual_vs_pred_summary(model.transform(train))
print("Train dataset")
train_summary.show()

# Summary for test
test_summary = actual_vs_pred_summary(model.transform(test))
print("Test dataset")
test_summary.show()
