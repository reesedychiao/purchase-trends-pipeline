from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType

spark = SparkSession.builder\
    .appName("KafkaSparkStreaming")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")\
    .getOrCreate()

df = spark\
    .readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "orders")\
    .option("startingOffsets", "earliest")\
    .load()

schema = StructType()\
    .add("Invoice", IntegerType())\
    .add("StockCode", StringType())\
    .add("Description", StringType())\
    .add("Quantity", IntegerType())\
    .add("InvoiceDate", StringType())\
    .add("Price", FloatType())\
    .add("Customer ID", IntegerType())\
    .add("Country", StringType())

processed_df = df.selectExpr("CAST(value AS STRING)")\
.select(from_json(col("value"), schema).alias("data"))\
.select("data.*")

query = processed_df\
    .writeStream\
    .outputMode("append")\
    .format("console")\
    .start()

query.awaitTermination()