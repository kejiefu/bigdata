import sys
from pyspark.sql import SparkSession

# Hive连接详情
hive_host = '192.168.110.26'
hive_port = 9083  # Hive Metastore默认端口是9083，不是10000
hive_user = 'hadoop'

# 创建启用了Hive支持的SparkSession对象，并配置Hive Thrift Server连接
spark = (SparkSession.builder
         .appName("Hive Table Query")
         .enableHiveSupport()
         .config("hive.metastore.uris", "thrift://{0}:{1}".format(hive_host, hive_port))
         .getOrCreate())

# 指定数据库（如果需要）
try:
    spark.sql("USE test4")
except Exception as e:
    print("Failed to use database 'test4': {}".format(e))
    spark.stop()
    raise

# 从系统脚本获取分区时间
dt = '20250210'

# 构建插入语句
insert_query = """
    INSERT OVERWRITE TABLE test
    VALUES ('8', 'h')
""".format(dt=dt)

try:
    # 执行插入语句
    spark.sql(insert_query)
    print("Successfully inserted data for partition dt={} into test.".format(dt))
except Exception as e:
    print("Failed to insert data for partition dt={}: {}".format(dt, e))

# 停止 SparkSession
spark.stop()
