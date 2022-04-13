import pandas

df = pandas.read_csv('./fr_last.csv')
df2 = pandas.read_csv('./fish_time.csv')
df = df.merge(df2, how='left', on='ticket_id')

df['duration'] = 0
for index in df.index:
    df.loc[index, 'duration'] = pandas.Timedelta(
        pandas.to_datetime(df.loc[index, 'end_time']) - pandas.to_datetime(df.loc[index, 'start_time'])).seconds

df3 = pandas.read_csv('./20210930.csv', index_col=0)
df3 = df3[['STU_CODE', 'total_level', ]]
df3['ticket_id'] = df3['STU_CODE']
df = df.merge(df3, how='left', on='ticket_id')
df = df.dropna()
df = df.sort_values(by='duration', ignore_index=True)
df.to_csv('final.csv')
print(df)
