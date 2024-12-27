#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#在 Python 中，如果文件中包含非 ASCII 字符（如注释中的中文字符），Python 需要知道如何解释这些字符。根据 PEP 263，您需要在 Python 源文件的开头添加一个特殊的注释来声明编码方式。
#对于您的情况，您可以在 Python 源文件的开头添加编码声明，以告诉 Python 如何解释包含非 ASCII 字符的内容。例如，您可以在文件的第一行或第二行添加类似以下形式的编码声明：

import string

import mysql.connector
from mysql.connector import Error
import random
from faker import Faker
import time
from datetime import datetime

# 初始化Faker对象，使用美国本地化设置
fake = Faker(['en_US'])

# 数据库连接配置
db_config = {
    'host': '192.168.110.150',
    'user': 'root',
    'password': 'Musem!@#20200217&*',
    'database': 'test'
}

# 定义美国家居名称列表
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
    return timestamp_prefix + random_suffix

def check_unique_order_id(cursor, order_id):
    """检查订单ID是否已经存在"""
    cursor.execute("SELECT COUNT(*) FROM customer_order WHERE order_id = %s", (order_id,))
    count = cursor.fetchone()[0]
    return count == 0

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

randomNumber = 50;

def insert_orders_and_details():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # 插入订单信息
            for j in range(randomNumber):
                order_id = generate_order_id()
                while not check_unique_order_id(cursor, order_id):
                    order_id = generate_order_id()  # 如果ID已存在，则重新生成

                email = fake.email()
                phone_number = fake.phone_number()
                status = random.choice(['Paid', 'Unpaid', 'Shipped', 'Completed'])
                total_amount = round(random.uniform(50, 500), 2)
                payment_method = random.choice(['Credit Card', 'PayPal', 'Apple Pay'])
                state = fake.state_abbr()  # 美国州的缩写
                city = fake.city()
                street = fake.street_address()

                order_query = """
                INSERT INTO customer_order (order_id, email, phone_number, order_date, status, total_amount, payment_method, province, city, street)
                VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)
                """
                order_values = (order_id, email, phone_number, status, total_amount, payment_method, state, city, street)

                cursor.execute(order_query, order_values)
                connection.commit()

                # 随机插入1到3个商品详情信息
                num_products = random.randint(1, 3)
                for k in range(num_products):
                    detail_id = get_random_string(20)
                    product_name = random.choice(home_items)  # 使用家居名称代替product_name
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

insert_orders_and_details()