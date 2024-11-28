import psycopg2

# 配置数据库连接信息
db_config = {
    'host': 'localhost',       # 数据库地址
    'port': 5432,              # 默认端口号
    'database': 'test',     # 数据库名称
    'user': 'xiamu',        # 用户名
    'password': '2000'  # 密码
}

try:
    # 连接 PostgreSQL 数据库
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # 执行 SQL 查询
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("PostgreSQL 版本:", version)

    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT
    );
    ''')

    # 插入数据
    cursor.execute("INSERT INTO test_table (name, age) VALUES (%s, %s)", ('Alice', 25))
    conn.commit()

    # 查询数据
    cursor.execute("SELECT * FROM test_table;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print("数据库操作失败:", e)

finally:
    # 关闭连接
    if conn:
        cursor.close()
        conn.close()
        print("数据库连接已关闭")