import src.python.common.common_utils as cm
import pandas as pd

if __name__ == '__main__':
    df=pd.read_csv("../src/datas/titannic_data.csv")
    cm.print_dataframe(df.head(10))

    # 1统计不同性别和不同Pclass的存活人数
    print("1统计不同性别和不同Pclass的存活人数")
    df1=df.groupby(['Sex', 'Pclass'])['Survived'].sum().reset_index()
    cm.print_dataframe(df1.head(10))
   # 2分性别统计各登船港口（Embarked）人数
    print("2分性别统计各登船港口（Embarked）人数")
    df2=df.groupby(['Sex','Embarked']).size().reset_index(name='counts')
    cm.print_dataframe(df2.head(10))
#3相关性分析：存活与年龄（age）、票类（Pclass）、票价（Fare）的相关性
    # Pandas 提供了 corr() 方法来计算列之间的皮尔逊相关系数（Pearson correlation coefficient），该系数范围从 -1 到 1：
    #
    # 1 表示完全正相关，
    # 0 表示没有线性关系，
    # -1 表示完全负相关。
    print('3相关性')
# 选择相关的列
    correlation_data = df[['Survived', 'Age', 'Pclass', 'Fare']]

# 计算相关性矩阵
    correlation_matrix = correlation_data.corr()

# 输出相关性矩阵
    print(correlation_matrix)


# 4. 用均值补充Age缺失值，并求出均值方差和25%分位数、中位数、75%分位数
    #均值
    print('# 4. 用均值补充Age缺失值，并求出均值方差和25%分位数、中位数、75%分位数')
    age_means=df['Age'].mean()
    df4=df.fillna(age_means).head(10)
    cm.print_dataframe(df4)
    # 计算 'Age' 列的方差
    age_variance = df['Age'].var()
    # 计算 25%、50%、75% 分位数
    q25 = df['Age'].quantile(0.25)
    median = df['Age'].quantile(0.50)  # 中位数
    q75 = df['Age'].quantile(0.75)

# 输出结果
    print(f"Age 方差: {age_variance}")
    print(f"25%分位数: {q25}")
    print(f"中位数（50%分位数）: {median}")
    print(f"75%分位数: {q75}")

#5.
import seaborn as sns
import matplotlib.pyplot as plt
# 参数说明：
# data=titanic_data：数据源，指定为 Titanic 数据集。
# x='Fare'：指定要绘制的数值变量是票价（Fare）。
# hue='Embarked'：按照登船港口（Embarked）分组并为每个港口使用不同的颜色。
# kde=True：绘制核密度估计（KDE）曲线，用于平滑显示数据的分布。
# multiple="stack"：当按 hue 进行分组时，堆叠不同类别的直方图，使其显示在同一图表中，便于比较。
# bins=30：直方图的箱数（区间数）。设置为 30 个箱子来显示票价的分布
# 绘制不同港口的票价直方图
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='Fare', hue='Embarked', kde=True, multiple="stack", bins=30)
plt.title('Fare Distribution by Embarked Port')
plt.xlabel('Fare')
plt.ylabel('Count')
plt.show()
# 参数说明：
# data=titanic_data：数据源，指定为 Titanic 数据集。
# x='Embarked'：设置 Embarked（登船港口）为 x 轴变量，表示不同港口。
# y='Fare'：设置 Fare（票价）为 y 轴变量，表示每个港口的票价分布。
# 绘制不同港口的票价箱线图
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Embarked', y='Fare')
plt.title('Fare Distribution by Embarked Port (Boxplot)')
plt.xlabel('Embarked Port')
plt.ylabel('Fare')
plt.show()















