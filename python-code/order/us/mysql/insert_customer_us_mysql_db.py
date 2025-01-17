#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import mysql.connector
from mysql.connector import Error
import random
from faker import Faker
import time

# 获取命令行参数
try:
    random_number = int(sys.argv[1]) if len(sys.argv) > 1 else random.randint(1000, 3000)  # 默认值随机数
except IndexError:
    random_number = 50
print("Will insert {} customers.".format(random_number))

# 初始化Faker对象，使用美国本地化设置
fake = Faker(['en_US'])

# 数据库连接配置
db_config = {
    'host': '192.168.110.150',
    'user': 'root',
    'password': 'Musem!@#20200217&*',
    'database': 'test'
}

def get_random_city_and_state(fake):
    """获取一个随机但相互对应的美国城市和州"""
    state_abbr = fake.state_abbr()
    city = fake.city()
    # 使用 zip code 来保证城市和州之间的对应关系
    zip_code = fake.zipcode_in_state(state_abbr=state_abbr)
    # 解析出城市部分（有时可能不完全准确）
    # 注意：Faker 生成的城市和州之间的关联不是严格的官方数据，仅用于测试目的。
    return city, state_abbr


class SimpleSnowflakeIDGenerator(object):
    """一个简化的雪花算法ID生成器"""

    def __init__(self, worker_id=0, data_center_id=0):
        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = 0
        self.last_timestamp = -1

    def _current_time_millis(self):
        return int(time.time() * 1000)

    def generate_id(self):
        current_time = self._current_time_millis()

        if current_time < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id")

        if current_time == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                current_time = self._wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = current_time

        id = ((current_time - 1420070400000) << 22) | (self.data_center_id << 17) | (
                self.worker_id << 12) | self.sequence
        return id

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_time_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_time_millis()
        return timestamp


def insert_customers():
    try:
        #**db_config 将这个字典解包，相当于将字典中的键值对作为关键字参数传递给函数
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            id_generator = SimpleSnowflakeIDGenerator()
            success_count = 0  # 成功插入的记录计数

            # 插入客户信息
            for _ in range(random_number):
                customer_id = id_generator.generate_id()
                email = fake.email()
                phone_number = fake.phone_number()
                # 美国州的缩写
                city, province = get_random_city_and_state(fake)

                customer_query = """
                # IGNORE 数据存在的就忽略
                INSERT IGNORE INTO customer (id, email, phone_number, province,city)
                VALUES ({}, '{}', '{}', '{}', '{}')
                """.format(customer_id, email, phone_number, province, city)

                cursor.execute(customer_query)
                connection.commit()
                success_count += cursor.rowcount  # 如果插入成功，则增加计数

            print("{} - 已插入{}个客户".format(time.strftime('%Y-%m-%d %H:%M:%S'), success_count))

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    insert_customers()
