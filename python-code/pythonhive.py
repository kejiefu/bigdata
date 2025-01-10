import pymysql
from pyhive import hive

# python 读取 testtable2 的数据写入数据到hive先判断数据是否存在，不存在则插入

# MySQL connection details
mysql_host = '192.168.110.150'
mysql_user = 'root'
mysql_password = 'Musem!@#20200217&*'
mysql_db = 'test'

# Hive connection details
hive_host = '192.168.110.26'
hive_port = 10000  # Default Hive port
hive_user = 'hadoop'
hive_database = 'test4'

# Establish MySQL connection
mysql_connection = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db)
mysql_cursor = mysql_connection.cursor()

# Execute MySQL query to fetch data from testtable2
mysql_query = "SELECT * FROM test"
mysql_cursor.execute(mysql_query)
mysql_data = mysql_cursor.fetchall()
for x in mysql_data:
    print(x)

# Close MySQL connection
mysql_cursor.close()
mysql_connection.close()

# Establish Hive connection
hive_connection = hive.connect(host=hive_host, port=hive_port, username=hive_user, database=hive_database)
hive_cursor = hive_connection.cursor()

# Iterate over the MySQL data and insert/update into Hive
for row in mysql_data:
    id_value = row[0]
    value = row[1]

    # Check if data exists in Hive
    hive_query = f"SELECT id FROM test WHERE id = '{id_value}'"
    hive_cursor.execute(hive_query)
    hive_result = hive_cursor.fetchall()

    if len(hive_result) > 0:
        print("EXISTS start ")

        print("email=" + value + ",id=" + id_value)

        print("EXISTS over")
    else:
        print("INSERT start ")
        # Data doesn't exist, insert into Hive
        hive_insert_query = f"INSERT INTO test (id, value) VALUES ('{id_value}', '{value}')"
        hive_cursor.execute(hive_insert_query)
        print("INSERT over")

# Commit changes and close Hive connection
hive_connection.commit()
hive_cursor.close()
hive_connection.close()
print("over")
