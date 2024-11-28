import sqlite3

# 连接数据库
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS 客户表 (
    customer_id INTEGER PRIMARY KEY,
    姓名 TEXT,
    联系方式 TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS 保单表 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    保单类型 TEXT,
    保单日期 TEXT,
    金额 REAL
)
''')

# 插入数据
# cursor.execute('INSERT INTO 客户表 (customer_id, 姓名, 联系方式) VALUES (1, "张三", "123456789")')
# cursor.execute('INSERT INTO 保单表 (customer_id, 保单类型, 保单日期, 金额) VALUES (1, "车险", "2023-05-01", 1000.50)')

# 查询数据
cursor.execute('SELECT * FROM 客户表')
print("客户表数据:", cursor.fetchall())

cursor.execute('SELECT * FROM 保单表')
print("保单表数据:", cursor.fetchall())

# 提交更改并关闭
conn.commit()
conn.close()
