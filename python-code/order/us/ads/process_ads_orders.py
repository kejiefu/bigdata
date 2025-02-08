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
    INSERT OVERWRITE TABLE ads_customer_order PARTITION (dt='{dt}')
    SELECT 
        o.order_id,
        o.email,
        o.phone_number,
        o.create_time,
        o.status,
        o.total_amount,
        o.payment_method,
        o.province,
        o.city,
        o.street,
        SUM(od.quantity) AS quantity,
        CONCAT_WS('#', COLLECT_SET(od.product_name)) AS product_name
    FROM 
        ods_customer_order o
    JOIN 
        ods_customer_order_detail od
    ON 
        o.order_id = od.order_id
    WHERE 
        o.dt = '{dt}' AND od.dt = '{dt}'
    GROUP BY 
        o.order_id,
        o.email,
        o.phone_number,
        o.create_time,
        o.status,
        o.total_amount,
        o.payment_method,
        o.province,
        o.city,
        o.street
""".format(dt=dt)

try:
    # 执行插入语句
    spark.sql(insert_query)
    print("Successfully inserted data for partition dt={} into ads_customer_order.".format(dt))
except Exception as e:
    print("Failed to insert data for partition dt={}: {}".format(dt, e))

# 停止 SparkSession
spark.stop()
