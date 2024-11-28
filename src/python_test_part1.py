import sqlite3
import src.python.common.common_utils as cm
import pandas as pd

   # 创建数据库连接（如果文件不存在，会自动创建）
conn = sqlite3.connect('test-exam.db')
sql='''
    SELECT name FROM sqlite_master  where type='table'
    '''
print(pd.read_sql_query(sql, conn))
sqlp='''
    SELECT * FROM 保单表
    '''
print(pd.read_sql_query(sqlp, conn))
sqlp='''
    SELECT * FROM 客户表
    '''
print(pd.read_sql_query(sqlp, conn))
sql6=''' 
select 
p1.客户号,
case when  
 p1.客户号 is not null and p2.客户号 is not null 
 then '既有车险又有非车险保单的客户'
 when p1.客户号 is not null and p2.客户号 is  null 
 then '仅有车险保单的客户'
 else 
 '仅非车保单的客户'
  end
  '分别统计仅有车险保单的客户、既有车险又有非车险保单的客户、仅非车保单的客户'
from  
 (select distinct 客户号 from 保单表 where 险种 = '车险' )p1
 full join 
 
 (select distinct 客户号 from 保单表  where 险种 = '非车' )p2
 on
 p1.客户号=p2.客户号
 


'''
print(cm.print_dataframe(pd.read_sql_query(sql6, conn).head(10)))
#1）分别统计仅有车险保单的客户、既有车险又有非车险保单的客户、仅非车保单的客户。
#分别统计仅有车险保单的客户
print('1分别统计仅有车险保单的客户')
sql1='''
select c.客户号,c.姓名
from
保单表 p
inner join
客户表 c
on
p.客户号=c.客户号
group by c.客户号
having count(distinct p.险种)=1
and sum(case when p.险种='车险' then 1 else 0 end)>0
'''
print(pd.read_sql_query(sql1, conn))
# 既有车险又有非车险保单的客户
print('11既有车险又有非车险保单的客户')
sql11='''
select p.客户号,c.姓名
from 保单表 p
inner join
客户表 c
on
p.客户号=c.客户号
group by p.客户号
having count(distinct p.险种)<>1
and sum(case when p.险种='车险' then 1 else 0 end)>0
and sum(case when p.险种='非车' then 1 else 0 end)>0
'''
print(pd.read_sql_query(sql11, conn))
#仅非车保单的客户
print('111仅非车保单的客户')
sql111='''
select c.客户号,c.姓名
from
保单表 p
inner join
客户表 c
on
p.客户号=c.客户号
group by c.客户号
having count(distinct p.险种)=1
and sum(case when p.险种='非车' then 1 else 0 end)>0
'''
print(pd.read_sql_query(sql111, conn))

#2）需求：为了解车险客户的续存情况，请计算，客户每张保单起保日期与上一张保单的终保日期的天数的差额，上一张保单通过起保日期判断。
# 输出字段：客户号、保单号、起保日期、上一张保单的终保日期、天数的差额
print('2输出字段：客户号、保单号、起保日期、上一张保单的终保日期、天数的差额')
sql2='''
select p.客户号,
c.姓名,
p.险种,
p.保单号,
julianday(lead(终保日期,1) over(partition by p.客户号,p.险种 order by 起保日期 desc ))- julianday(终保日期) as 天数的差额,
起保日期,
终保日期,
lead(终保日期,1) over(partition by p.客户号 order by 起保日期 desc) as 上一张保单的终保日期
from 保单表 p
inner join
客户表 c
on 
p.客户号=c.客户号
order by c.客户号, 起保日期 desc 
'''
print(cm.print_dataframe(pd.read_sql_query(sql2, conn).head(10)))

#3）统计被保险人保单数及保费
print('3统计被保险人保单数及保费')

sql3='''
select p.客户号,
count(1) as counts,
sum(保费) as sums
from 保单表 p
inner join
客户表 c
on 
p.客户号=c.客户号
group by c.客户号
'''
print(cm.print_dataframe(pd.read_sql_query(sql3, conn).head(10)))
#4）需求：请在保单表的清单上添加一列，用于统计每个客户按起保日期排序并在2023年的保单的累计保费
print('4在保单表的清单上添加一列，用于统计每个客户按起保日期排序并在2023年的保单的累计保费')
sql4='''
select p.客户号,
c.姓名,
p.险种,
p.保单号,
case when substr(cast(起保日期 as string),0,5) =2023 then sum(保费) over(partition by p.客户号 order by 起保日期 )  else 保费 end sum_adds_2023,
保费,
起保日期,
终保日期
from 保单表 p
inner join
客户表 c
on 
p.客户号=c.客户号
'''
print(cm.print_dataframe(pd.read_sql_query(sql4, conn).head(10)))
#5）因营销活动，需提取连续3年及以上都购买过保单的客户
print('5因营销活动，需提取连续3年及以上都购买过保单的客户')
sql5=''' 
select 
*
from
(select 
c.客户号,
years -
row_number() over(partition by p.客户号 order by years  )  
as diff,
 years,
row_number() over(partition by p.客户号 order by years  ) rows
from  
( select 客户号, 
substr(cast(起保日期 as string),0,5) years 
from 保单表 
) p
inner join
客户表 c
on 
p.客户号=c.客户号
group by c.客户号,p.years
 )t

'''
print(cm.print_dataframe(pd.read_sql_query(sql5, conn).head(10)))
#6）统计每一年每个客户的保费与当年所有客户的平均保费的差额
print('6统计每一年每个客户的保费与当年所有客户的平均保费的差额')
sql6=''' 
select 
*
from
(select 
c.客户号,
p.years,
sum(p.保费) over(partition by p.客户号,years) a, avg(p.保费) 每一年每个客户的保费,
avg(p.保费) 当年所有客户的平均保费,
sum(p.保费) over(partition by p.客户号,years) -avg(p.保费)   差额
from  
( select 客户号,保费, substr(cast(起保日期 as string),0,5) years from 保单表 ) p
inner join
客户表 c
on 
p.客户号=c.客户号
group by c.客户号,p.years
)t
'''
print(cm.print_dataframe(pd.read_sql_query(sql6, conn).head(10)))
#

