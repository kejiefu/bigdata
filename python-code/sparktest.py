from pyspark.sql import SparkSession

# 创建SparkSession对象
spark = SparkSession.builder \
    .appName("Hadoop Connection") \
    .enableHiveSupport() \
    .getOrCreate()

# 连接Hadoop并加载数据
df = spark.read.format('com.databricks.spark.csv') \
    .options(header='true', inferschema='true') \
    .load('hdfs://192.168.110.26:9000/user/hadoop/E_Commerce_Data.csv')

# 执行其他操作...
# 例如，显示DataFrame的前几行数据
df.show()

count = df.count()
print("Number of rows: ", count)

clean=df.filter(df["CustomerID"]!=0).filter(df["Description"]!="")

data = clean.count()
print("Number of data: ", data)

# 关闭SparkSession连接
spark.stop()