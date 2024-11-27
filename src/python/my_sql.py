import mysql.connector
from mysql.connector import Error
def connect_to_mysql(host, user, password, database):
    """连接 MySQL 数据库并返回连接对象和游标"""
    try:
        # 建立连接
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("成功连接到数据库")
            # 创建游标
            cursor = connection.cursor()
            return connection, cursor
    except Error as err:
        print(f"连接错误: {err}")
        return None, None

def close_connection(connection, cursor):
    """关闭数据库连接和游标"""
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        print("数据库连接已关闭")

def execute_query(cursor, query, params=None):
    """执行查询语句并返回结果"""
    try:
        cursor.execute(query, params)
        return cursor.fetchall()  # 返回查询结果
    except Error as err:
        print(f"查询错误: {err}")
        return None


import pymysql
from pymysql import MySQLError

def connect_to_mysql_bak(host, user, password, database):
    """连接 MySQL 数据库并返回连接对象和游标"""
    try:
        # 建立连接
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # 创建游标
        cursor = connection.cursor()
        print("成功连接到数据库")
        return connection, cursor
    except MySQLError as err:
        print(f"连接错误: {err}")
        return None, None

def close_connection(connection, cursor):
    """关闭数据库连接和游标"""
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("数据库连接已关闭")

def execute_query(cursor, query, params=None):
    """执行查询语句并返回结果"""
    try:
        cursor.execute(query, params)
        return cursor.fetchall()  # 返回查询结果
    except MySQLError as err:
        print(f"查询错误: {err}")
        return None


from dotenv import load_dotenv
import os



if __name__ == '__main__':

# 加载 .env 文件中的环境变量
 load_dotenv()

# 获取环境变量
 db_user = os.getenv('DB_USER')
 db_password = os.getenv('DB_PASSWORD')
 db_host = os.getenv('DB_HOST')
 db_name = os.getenv('DB_NAME')

# 使用这些信息
 print(f"Connecting to {db_name} at {db_host} with user {db_user}")


# 连接到 MySQL 数据库
connection, cursor = connect_to_mysql(db_host, db_user, db_password, db_name)

if connection and cursor:
    # 执行查询操作
    query = "SELECT * FROM u1"
    results = execute_query(cursor, query)

    if results:
        for row in results:
            print(row)

    # 关闭连接
    close_connection(connection, cursor)


