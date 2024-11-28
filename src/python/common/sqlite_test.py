import sqlite3
import pandas as pd
import common_utils as cm

# 创建数据库连接（如果文件不存在，会自动创建）
conn = sqlite3.connect('test-exam.db')

# # 创建客户表
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS customers (
#     customer_id INTEGER PRIMARY KEY,
#     customer_name TEXT
# );
# ''')
#
# # 创建保单表
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS policies (
#     policy_id INTEGER PRIMARY KEY,
#     customer_id INTEGER,
#     policy_type TEXT,
#     start_date TEXT,
#     end_date TEXT,
#     premium REAL,
#     FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
# );
# ''')
#
# # 生成随机客户数据
# def generate_customers(num_customers):
#     customer_names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Ivy", "Jack"]
#     for i in range(num_customers):
#         name = random.choice(customer_names)
#         cursor.execute("INSERT INTO customers (customer_name) VALUES (?)", (name,))
#     conn.commit()
#
# # 生成随机保单数据
# def generate_policies(num_policies):
#     policy_types = ["车险", "非车险"]
#     for i in range(num_policies):
#         customer_id = random.randint(1, 10)  # 随机选择一个客户
#         policy_type = random.choice(policy_types)
#         start_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1200))  # 随机起保日期
#         end_date = start_date + timedelta(days=random.randint(30, 365))  # 随机终保日期（1个月到1年）
#         premium = round(random.uniform(100, 1000), 2)  # 随机保费
#         cursor.execute("""
#             INSERT INTO policies (customer_id, policy_type, start_date, end_date, premium)
#             VALUES (?, ?, ?, ?, ?)
#         """, (customer_id, policy_type, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), premium))
#     conn.commit()
#
# # 生成数据
# generate_customers(10)  # 创建10个客户
# generate_policies(30)   # 创建30个保单
#
# # 查看数据
# # cursor.execute("SELECT * FROM customers")
# # print("Customers:")
# # for row in cursor.fetchall():
#     print(row)
sql_customers="select * from customers"
print(cm.print_dataframe(pd.read_sql_query(sql_customers, conn).head(3)))
sql_policies="select * from policies"
print(cm.print_dataframe(pd.read_sql_query(sql_policies, conn).head(3)))
# cursor.execute("SELECT * FROM policies")
# print("\nPolicies:")
# for row in cursor.fetchall():
#     print(row)




sql2='''

select c.customer_id,c.customer_name  
from 
policies p
inner join
customers c
on 
p.customer_id=c.customer_id
group by c.customer_id
having count(distinct p.policy_type)=1
and sum(case when p.policy_type='车险' then 1 else 0 end)>0
'''
print(pd.read_sql_query(sql2, conn))
sql22='''
select p.customer_id,c.customer_name  
from policies p
inner join
customers c
on 
p.customer_id=c.customer_id
group by p.customer_id
having count(distinct p.policy_type)<>1
and sum(case when p.policy_type='车险' then 1 else 0 end)>0
and sum(case when p.policy_type='非车险' then 1 else 0 end)>0
'''
print(pd.read_sql_query(sql22, conn))


sql3='''
select p.customer_id,
c.customer_name,
p.policy_type,
p.policy_id,
julianday(lag(start_date,1) over(partition by p.customer_id,p.policy_type order by start_date desc ,end_date desc))- julianday(end_date) as diff_date,
lag(start_date,1) over(partition by p.customer_id order by start_date desc ,end_date desc) as new_start_date,
start_date,
end_date

from policies p
inner join
customers c
on 
p.customer_id=c.customer_id
'''
print(cm.print_dataframe(pd.read_sql_query(sql3, conn).head(10)))



sql4='''
select p.customer_id,
count(1) as counts,
sum(premium) as sums
from policies p
inner join
customers c
on 
p.customer_id=c.customer_id
group by c.customer_id
'''
print(cm.print_dataframe(pd.read_sql_query(sql4, conn).head(10)))

sql5='''
select p.customer_id,
c.customer_name,
p.policy_type,
p.policy_id,
sum(premium) over(partition by p.customer_id order by start_date ) sum_adds,
premium,
start_date,
end_date
from policies p
inner join
customers c
on 
p.customer_id=c.customer_id
'''
print(cm.print_dataframe(pd.read_sql_query(sql5, conn).head(10)))

sql6=''' 
select 
customer_id
from
(select 
c.customer_id,
years -
row_number() over(partition by p.customer_id order by years  ) diff,
 years,
row_number() over(partition by p.customer_id order by years  ) rows
from  
( select customer_id, substr(cast(start_date as string),0,5) years from policies ) p
inner join
customers c
on 
p.customer_id=c.customer_id
group by c.customer_id,p.years
)t
group by diff,customer_id
having count(1) >=3
'''
print(cm.print_dataframe(pd.read_sql_query(sql6, conn).head(10)))

sql6=''' 
select 
*
from
(select 
c.customer_id,
p.years,
sum(p.premium) over(partition by p.customer_id,years) a, avg(p.premium) b,
sum(p.premium) over(partition by p.customer_id,years) -avg(p.premium)   diff2
from  
( select customer_id,premium, substr(cast(start_date as string),0,5) years from policies ) p
inner join
customers c
on 
p.customer_id=c.customer_id
group by c.customer_id,p.years
)t
'''
print(cm.print_dataframe(pd.read_sql_query(sql6, conn).head(10)))
# 关闭数据库连接
conn.close()
