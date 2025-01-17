from pyhive import hive
import sys

#python create_hive_partition ods_customer dt 2025-01-14
#python直接执行的右键 modify run configuration 参数在 在 Sciript parameters 填入 ods_customer dt 2025-01-16 就像

hive_config = {
    'host': '192.168.110.26',
    'port': 10000,
    'username': 'hadoop',
    'database': 'test'
}

# 获取传入的参数
if len(sys.argv) < 4:
    print("Usage: python script.py <table_name> <partition_column> <partition_value>")
    sys.exit(1)

table_name = sys.argv[1]
partition_column = sys.argv[2]
partition_value = sys.argv[3]

# 连接到 Hive
conn = hive.Connection(**hive_config)
cursor = conn.cursor()

# 查询是否存在指定分区
query = f"SHOW PARTITIONS {table_name} PARTITION ({partition_column}='{partition_value}')"
cursor.execute(query)
result = cursor.fetchall()

# 如果分区不存在，则创建分区
if not result:
    create_partition_query = f"ALTER TABLE {table_name} ADD PARTITION ({partition_column}='{partition_value}')"
    cursor.execute(create_partition_query)
    print(f"Partition ({partition_column}='{partition_value}') created successfully")
else:
    print(f"Partition ({partition_column}='{partition_value}') already exists")

# 关闭连接
cursor.close()
conn.close()