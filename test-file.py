# Basic check
print("GitHub code is running!")

# Create a tiny sample dataframe
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

pdf = pd.DataFrame({
    "name": ["diggy", "john", "maria"],
    "age": [28, 31, 27]
})

df = spark.createDataFrame(pdf)

display(df)

df.write.mode("overwrite").csv("/tmp/databricks_poc_output")
print("Write complete.")

df2 = spark.read.csv("/tmp/databricks_poc_output", header=False)
display(df2)

display(dbutils.fs.ls("/databricks-datasets/"))

df = spark.read.format("delta").load("/databricks-datasets/nyctaxi-with-zipcodes/subsampled")
df.show(5)

data = [
    ("diggy", "IN", 28),
    ("maria", "US", 27),
    ("lee", "SG", 31),
]

df = spark.createDataFrame(data, ["name", "country", "age"])

df.write.mode("overwrite").parquet("/tmp/poc/parquet_data")
print("Parquet written!")

df2 = spark.read.parquet("/tmp/poc/parquet_data")
df2.show()

df.write.format("delta").mode("overwrite").save("/tmp/poc/delta_data")
print("Delta written!")

df3 = spark.read.format("delta").load("/tmp/poc/delta_data")
df3.show()
