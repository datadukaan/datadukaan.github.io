"""Day 9 - The problem: reading columns by position.

The son copies "the third column". It worked in October.
In November the supplier added a 'discount' column before 'price',
so column 3 is now the discount - and nothing fails.
"""
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[1]").appName("day09-position").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

for month in ("october", "november"):
    df = spark.read.csv(f"data/bill_{month}.csv", header=True, inferSchema=True)
    third = df.columns[2]                                    # "the third column"
    total = df.agg(F.sum(F.col(third))).first()[0]
    print(f"{month:<9} columns={df.columns}  -> column 3 is '{third}', total Rs {total:,}")

# A fixed positional schema is just as fragile: the names are forced onto the wrong data
fixed = "item STRING, qty STRING, price INT"
nov = spark.read.csv("data/bill_november.csv", header=True, schema=fixed)
print("november read with the October schema:")
nov.show()
spark.stop()
