import pandas as pd

# df = pd.read_spss('./20210923.sav')
# df.to_csv('./new2.csv')
df = pd.read_csv('20210930.csv')
df2 = pd.read_csv('./fridge_result_students.csv')

df1 = df[['STU_CODE', 'total_score',
          'INQUIRY_score', 'total_level', 'INQUIRY_level']]

newDF = pd.merge(df2, df1, how='left', on='STU_CODE')

newDF = newDF.dropna()
print(newDF)
newDF.to_csv('newResult0930.csv')
# print(newDF)
