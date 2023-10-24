import mysql.connector

mydb = mysql.connector.connect(
    host="local.musem.com",
    user="root",
    passwd="root",
    database="m20230810",
    port="13306"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM eav_attribute")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)
