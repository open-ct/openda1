import pandas as pd

df = pd.read_csv('./filter.csv', index_col=0)

l = len(df)

df = df.dropna()
l2 = len(df)

df.to_csv('./filter2.csv')

print(l)
print(l2)
