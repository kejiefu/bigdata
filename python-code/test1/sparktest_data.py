from pyspark.sql import SparkSession

# Hive连接详情
hive_host = '192.168.110.26'
hive_port = 10000  # 默认Hive端口
hive_user = 'hadoop'

# 创建启用了Hive支持的SparkSession对象，并配置Hive Thrift Server连接
spark = SparkSession.builder \
    .appName("Hive Table Query") \
    .enableHiveSupport() \
    .config("hive.metastore.uris", f"thrift://{hive_host}:{hive_port}") \
    .getOrCreate()

# 验证是否启用了Hive支持
print("Hive support is enabled:", ("hive" in spark.sparkContext.getConf().getAll()))

# 如果需要，可以验证是否成功连接到Hive Metastore
try:
    spark.sql("SHOW DATABASES").show()
    print("Successfully connected to Hive Metastore.")
except Exception as e:
    print(f"Failed to connect to Hive Metastore: {e}")

# 指定数据库（如果需要）
spark.sql(f"USE test")

# 查询Hive表中的数据
df = spark.sql("""
    SELECT *
    FROM ods_customer_order
    WHERE dt = '20250126'
""")

# 显示DataFrame的前几行数据
df.show()

count = df.count()
print("Number of rows: ", count)

# 数据清洗：过滤掉CustomerID为0以及Description为空的数据
clean_df = df.filter(df["CustomerID"] != 0).filter(df["Description"] != "")

clean_count = clean_df.count()
print("Number of cleaned data: ", clean_count)

# 如果需要保存清洗后的数据到新的Hive表或覆盖现有表
# clean_df.write.mode("overwrite").saveAsTable("cleaned_ods_customer_order")

# 关闭SparkSession连接
spark.stop()