from mysql.connector import MySQLConnection
connect=MySQLConnection(
    user='root',
    password='',
    host='127.0.0.1',
)

cursor=connect.cursor()
cursor.execute("show databases;")
dbs=cursor.fetchall()
connect.close()

for i in range(0,len(dbs)):
    print(dbs[i][0])
