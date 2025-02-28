from datetime import datetime

import pika
import json

# 配置 RabbitMQ 连接参数
rabbitmq_host = '192.168.10.106'
rabbitmq_port = 5672
rabbitmq_user = 'musem-dev'
rabbitmq_password = 'musem-dev'
rabbitmq_virtual_host = 'musem-test1'  # 使用根路径或自定义虚拟主机

rabbitmq_exchange = 'py_test_exchange'
rabbitmq_queue = 'py_test_queue'

# 连接到 RabbitMQ（包含 virtual_host）
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password),
            virtual_host=rabbitmq_virtual_host
        )
    )
    channel = connection.channel()
except Exception as e:
    print(f" [x] RabbitMQ 连接失败: {e}")
    exit()

# 声明持久化交换机和队列
channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='direct', durable=True)
channel.queue_declare(queue=rabbitmq_queue, durable=True)

# 绑定队列到交换机
channel.queue_bind(
    queue=rabbitmq_queue,
    exchange=rabbitmq_exchange,
    routing_key=rabbitmq_queue,
)

# 创建包含时间戳的 JSON 数据
data = {
    "data": "hello world",
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

message = json.dumps(data)

properties = pika.BasicProperties(delivery_mode=2)  # 消息持久化
channel.basic_publish(
    exchange=rabbitmq_exchange,
    routing_key=rabbitmq_queue,
    body=message,
    properties=properties
)

print(f" [x] Sent '{message}' to {rabbitmq_queue}")

connection.close()