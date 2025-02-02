#!/usr/bin/env python3

#在 Python 中，如果文件中包含非 ASCII 字符（如注释中的中文字符），Python 需要知道如何解释这些字符。根据 PEP 263，您需要在 Python 源文件的开头添加一个特殊的注释来声明编码方式。

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

# 定义家居名称列表
home_items = [
    "Sofas", "Armchairs", "Coffee Tables", "Dining Tables", "Bookcases", "TV Stands",
    "Beds", "Mattresses", "Wardrobes", "Cabinets", "Shelves", "Desks", "Chairs",
    "Rugs", "Curtains", "Lamps", "Mirrors", "Decorative Pillows", "Throw Blankets",
    "Wall Art", "Floor Lamps", "Table Lamps", "Ceiling Fans", "Outdoor Furniture",
    "Bar Stools", "Storage Boxes", "Console Tables", "Sideboards", "Office Chairs"
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
                product_name = random.choice(home_items)
                quantity = random.randint(1, 5)
                price = round(random.uniform(10, 100), 2)
                discount = round(random.uniform(0, 0.3), 2) if random.random() > 0.5 else None

                detail_query = """
                INSERT INTO customer_order_detail (detail_id, order_id, product_name, quantity, price, discount)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                detail_values = (detail_id, order_id, product_name, quantity, price, discount)

                cursor.execute(detail_query, detail_values)
                connection.commit()

            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 已插入订单及其详情")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#  生成数据
insert_orders_and_details()