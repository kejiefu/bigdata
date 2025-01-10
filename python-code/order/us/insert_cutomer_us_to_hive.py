import time

import pymysql
from pyhive import hive
from datetime import datetime

# MySQL connection parameters
mysql_config = {
    'host': '192.168.110.150',
    'user': 'root',
    'password': 'Musem!@#20200217&*',
    'database': 'test',
    'port': 3306,
}

# Hive connection parameters
hive_config = {
    'host': '192.168.110.26',  # Replace with your Hive server host
    'port': 10000,  # Default HiveServer2 port
    'username': 'hadoop',  # Replace with your username
    'database':'test'
}

# Other configurations
columns = ['id', 'email', 'phone_number', 'create_time', 'province', 'city']
where_clause = "DATE(create_time) = %s"


def fetch_data_from_mysql(bizdate):
    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT {','.join(columns)} FROM customer WHERE {where_clause} limit 1"
            cursor.execute(sql, (bizdate,))
            return cursor.fetchall()
    finally:
        connection.close()


def format_value(value):
    """Format the value for inclusion in an SQL statement."""
    if isinstance(value, str):
        return f"'{value.replace('\'', '\\\'')}'"
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    else:
        return str(value)


def insert_into_hive_partitioned(data, bizdate):
    # Connect to Hive
    conn = hive.Connection(**hive_config)
    cursor = conn.cursor()

    # Prepare the data for insertion
    formatted_data = []
    for row in data:
        # Format each value based on its type
        formatted_row = [format_value(item) for item in row]
        formatted_data.append(f"({', '.join(formatted_row)})")

    # Insert data into Hive table partition
    values_str = ', '.join(formatted_data)
    # overwrite  将之前的数据覆盖
    insert_sql = f"""
    INSERT overwrite TABLE customer PARTITION(dt='{bizdate}')
    VALUES {values_str}
    """
    # 记录代码块执行之前的时间
    start_time = time.time()
    try:
        cursor.execute(insert_sql)
        print("Data inserted successfully.")
        # 记录代码块执行之后的时间
        end_time = time.time()

        # 计算并打印执行时间
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
    except Exception as e:
        print(f"Failed to insert data: {e}")
        print(f"Generated SQL: {insert_sql}")  # Debugging purposes


if __name__ == "__main__":
    bizdate = '2025-01-02'  # Example date, replace with actual business date
    # Fetch data from MySQL based on bizdate
    data = fetch_data_from_mysql(bizdate)

    if data:
        # Insert into Hive with partition
        insert_into_hive_partitioned(data, bizdate)
        print(f"Data for {bizdate} has been successfully written to Hive.")
    else:
        print("No data found for the given date.")


#sparkSession