import pika
import json
import sys

# 配置 RabbitMQ 连接参数（与生产者保持一致）
rabbitmq_host = '192.168.10.106'
rabbitmq_port = 5672
rabbitmq_user = 'musem-dev'
rabbitmq_password = 'musem-dev'
rabbitmq_virtual_host = 'musem-test1'  # 确保与生产者虚拟主机一致
rabbitmq_queue = 'py_test_queue'

def main():
    try:
        # 连接到 RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password),
                virtual_host=rabbitmq_virtual_host
            )
        )
        channel = connection.channel()

        # 声明队列（与生产者一致）
        channel.queue_declare(queue=rabbitmq_queue, durable=True)

        # 定义消息处理回调函数
        def callback(ch, method_frame, header_frame, body):
            try:
                # 解析 JSON 消息
                message = json.loads(body)
                print(f" [x] Received message: {message}")

                # 手动发送消息确认（防止重复消费）
                ch.basic_ack(delivery_tag=method_frame.delivery_tag)
            except json.JSONDecodeError as e:
                print(f" [x] JSON 解析失败: {e}, 原始消息: {body}")
                # 可选择拒绝消息（根据业务需求）
                # ch.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            except Exception as e:
                print(f" [x] 处理消息时发生错误: {e}")
                # 可选择拒绝消息
                # ch.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)

        # 开始消费消息（设置 no_ack=False 手动确认）
        channel.basic_consume(
            queue=rabbitmq_queue,
            on_message_callback=callback,
            auto_ack=False  # 关闭自动确认
        )

        print(f" [x] Waiting for messages in queue '{rabbitmq_queue}'. To exit press CTRL+C")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f" [x] RabbitMQ 连接失败: {e}")
    except Exception as e:
        print(f" [x] 发生未知错误: {e}")
    finally:
        # 关闭连接（在异常或手动退出时执行）
        try:
            connection.close()
        except:
            pass


if __name__ == "__main__":
    main()