from pyhive import hive

#因为dataX没法创建分区，所以先创建分区，再执行dataX导入数据

hive_config = {
    'host': '192.168.110.26',  # Replace with your Hive server host
    'port': 10000,  # Default HiveServer2 port
    'username': 'hadoop',  # Replace with your username
    'database': 'test'
}

# 连接到 Hive
conn = hive.Connection(**hive_config)
cursor = conn.cursor()

# 要创建的分区信息
table_name = 'ods_customer'
partition_column = 'dt'
partition_value = '2025-01-14'

# 查询是否存在指定分区
query = f"SHOW PARTITIONS {table_name} PARTITION ({partition_column}='{partition_value}')"
cursor.execute(query)
result = cursor.fetchall()

# 如果分区不存在，则创建分区
if not result:
    create_partition_query = f"ALTER TABLE {table_name} ADD PARTITION ({partition_column}='{partition_value}')"
    cursor.execute(create_partition_query)
    print(f"分区 ({partition_column}='{partition_value}') 创建成功")
else:
    print(f"分区 ({partition_column}='{partition_value}') 已经存在")

# 关闭连接
cursor.close()
conn.close()