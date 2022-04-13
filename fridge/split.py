import pandas as pd

df = pd.read_csv('reduceData.csv', index_col=0)
print(len(df))
# df.drop(df.index['id'] == 'demo')
df = df[~df['id'].isin(['demo'])]
print(len(df))
df = df[~df['ans'].astype(str).isin(['[]'])]
print(len(df))
df['id'] = df['id'].apply(pd.to_numeric)

grouped = df.groupby('num')
for value,group in grouped:
    filename='./output/' + str(value)+'.csv'
    with open(filename, 'w') as f:
        f.truncate()
        group.sort_values(by='id')
        group.to_csv(filename)