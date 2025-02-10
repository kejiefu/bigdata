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
    spark.sql("USE test")
except Exception as e:
    print("Failed to use database 'test': {}".format(e))
    spark.stop()
    raise


# 从系统脚本获取分区时间
if len(sys.argv) != 2:
    print("Usage: python script.py <partition_date>")
    spark.stop()
    sys.exit(1)

dt = sys.argv[1]

# 构建插入语句
insert_query = """
    INSERT OVERWRITE TABLE ads_customer PARTITION (dt='{dt}')
    VALUES (1338426288783753216, 'adriana83@example.org', '+1-980-632-4907x5077', CAST('2025-02-10 08:28:14' AS TIMESTAMP), 'NH', 'Jacquelinefurt')
""".format(dt=dt)

try:
    # 执行插入语句
    spark.sql(insert_query)
    print("Successfully inserted data for partition dt={} into ads_customer.".format(dt))
except Exception as e:
    print("Failed to insert data for partition dt={}: {}".format(dt, e))

# 停止 SparkSession
spark.stop()
