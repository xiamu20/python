import common_utils as cm
import pandas as pd

if __name__ == '__main__':
    df=pd.read_csv("../datas/titannic_data.csv")
    cm.print_dataframe(df.head(10))

    # 1统计不同性别和不同Pclass的存活人数
    print("统计不同性别和不同Pclass的存活人数")
    df1=df.groupby(['Sex', 'Pclass'])['Survived'].sum().reset_index()
    cm.print_dataframe(df1)
   # 2分性别统计各登船港口（Embarked）人数
    print("分性别统计各登船港口（Embarked）人数")
    df2=df.groupby(['Sex','Embarked']).size().reset_index(name='counts')
    cm.print_dataframe(df2)

# 4. 用均值补充Age缺失值，并求出均值方差和25%分位数、中位数、75%分位数
    age_means=df['Age'].mean()
    df4=df.fillna(age_means)
    cm.print_dataframe(df4)










