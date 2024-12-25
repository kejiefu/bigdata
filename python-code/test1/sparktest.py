from pyspark.sql import SparkSession

# https://juejin.cn/post/7072735458966372365?searchId=20231007102500108B7E6A9463E11DF577

# hdfs://192.168.110.26:9000/E_Commerce_Data.csv  这个路径对应着  http://192.168.110.26:50070/explorer.html#/ 这个路径的所看到的文件 E_Commerce_Data

# hdfs://192.168.110.26:9000/test/E_Commerce_Data.csv  这个路径对应着  http://192.168.110.26:50070/explorer.html#/ 这个路径的所看到的文件 test/E_Commerce_Data

# 创建SparkSession对象
spark = SparkSession.builder \
    .appName("Hadoop Connection") \
    .enableHiveSupport() \
    .getOrCreate()

# 连接Hadoop并加载数据
df = spark.read.format('com.databricks.spark.csv') \
    .options(header='true', inferschema='true') \
    .load('hdfs://192.168.110.26:9000/test/E_Commerce_Data.csv')

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