from pyhdfs import HdfsClient
import json

#版本不兼容

# Hadoop连接配置
hadoop_host = '192.168.110.26'
hadoop_port = 9000
hadoop_user = 'hadoop'

# 新文件路径
hadoop_file_path = '/path/to/hadoop/new_file.txt'

# 要写入的数据
data = [
    {
        "code": "memberorder",
        "label": "for 1 item",
        "discountType": 2,
        "discountAmount": 20.0000,
        "startTime": "09/21/2023",
        "endTime": "09/28/2023",
        "detail": "Become a member available",
        "isLogin": 0
    },
    {
        "code": "PD420",
        "label": "For orders over $3500",
        "discountType": 1,
        "discountAmount": 420.0000,
        "startTime": "07/11/2023",
        "endTime": "07/12/2023",
        "detail": "For POVISON Day Sale items",
        "isLogin": 0
    }
]

def write_to_hadoop():
    try:
        # 连接Hadoop集群
        client = HdfsClient(hosts=f"{hadoop_host}:{hadoop_port}", user_name=hadoop_user)

        # 将数据转换为JSON字符串
        data_json = json.dumps(data)

        # 将数据写入新文件
        client.create(hadoop_file_path, data_json, overwrite=True)

        print("Data written to Hadoop file successfully.")
    except Exception as e:
        print("Error: ", e)

# 执行将数据写入Hadoop文件
write_to_hadoop()