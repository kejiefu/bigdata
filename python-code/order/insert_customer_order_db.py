from datetime import datetime

import mysql.connector
from mysql.connector import Error
import random
import string
from faker import Faker
import time

# 初始化Faker对象
fake = Faker(['zh_CN'])

# 数据库连接配置
db_config = {
    'host': '192.168.110.150',
    'user': 'root',
    'password': 'Musem!@#20200217&*',
    'database': 'test'
}

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# 定义手机品牌列表
phone_brands = [
    "Apple", "Samsung", "Huawei", "Xiaomi", "Vivo", "Oppo", "OnePlus",
    "Realme", "iQOO", "Google", "Sony", "Nokia", "LG", "Motorola"
]

def generate_order_id():
    """生成由年月日时分秒（24小时制）加随机数组成的订单ID"""
    timestamp_prefix = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"{timestamp_prefix}{random_suffix}"

def check_unique_order_id(cursor, order_id):
    """检查订单ID是否已经存在"""
    cursor.execute("SELECT COUNT(*) FROM customer_order WHERE order_id = %s", (order_id,))
    count = cursor.fetchone()[0]
    return count == 0

#插入多少条数据
randomNumber = 50

def insert_orders_and_details():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # 插入订单信息
            for _ in range(randomNumber):
                order_id = generate_order_id()
                while not check_unique_order_id(cursor, order_id):
                    order_id = generate_order_id()  # 如果ID已存在，则重新生成
                email = fake.email()
                phone_number = fake.phone_number()
                status = random.choice(['已支付', '未支付', '已发货', '已完成'])
                total_amount = round(random.uniform(50, 500), 2)
                payment_method = random.choice(['信用卡', '支付宝', '微信支付'])
                province = fake.province()
                city = fake.city()
                street = fake.street_address()

                order_query = """
                INSERT INTO customer_order (order_id, email, phone_number, order_date, status, total_amount, payment_method, province, city, street)
                VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)
                """
                order_values = (order_id, email, phone_number, status, total_amount, payment_method, province, city, street)

                cursor.execute(order_query, order_values)
                connection.commit()

                # 插入订单详情信息
                detail_id = get_random_string(20)
                sku = random.choice(phone_brands)  # 使用手机品牌名称代替SKU
                quantity = random.randint(1, 5)
                price = round(random.uniform(10, 100), 2)
                discount = round(random.uniform(0, 0.3), 2) if random.random() > 0.5 else None

                detail_query = """
                INSERT INTO customer_order_detail (detail_id, order_id, sku, quantity, price, discount)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                detail_values = (detail_id, order_id, sku, quantity, price, discount)

                cursor.execute(detail_query, detail_values)
                connection.commit()

            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 已插入10条订单及其详情")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#  生成数据
insert_orders_and_details()