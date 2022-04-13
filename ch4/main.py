import ast
from json import encoder
import pandas
import numpy as np
import json
import csv


# df = pandas.read_csv('mianyang_CH4.csv')
# # df.columns = ["time", "user", "ticket_id",
# #               "qu_id", "qu_name", "task_answers", "owne"]
# df1 = df.loc[:, ['time', 'ticket_id', 'task_answers']]
# df1['time'] = pandas.to_datetime(df1.time)
# df1 = df1.sort_values(by='time', ignore_index=True)
# df1.to_csv('reduceCH4.csv')
# print(df1[0])


# df = pandas.read_csv('reduce2.csv', index_col=0)
# a = df[df['task_answers'].str.contains('null', na=False)]
# df_clear = df[df['task_answers'].str.contains('"page":3', na=False)]
# df_clear['time'] = pandas.to_datetime(df_clear.time)
# df_clear = df_clear.sort_values(by='time', ignore_index=True)
# df_clear.to_csv('test2.csv')

# df = pandas.read_csv('reduceCH4.csv', index_col=0)
# df = df[df['task_answers'].str.contains('"page":', na=False)]
# df.to_csv('reduceCH4.csv')

# for index in df.index:
#     # frame = json.loads(df.loc[index].data)['frame']
#     # try:
#     frame = ast.literal_eval(df.loc[index].task_answers)
#     # df.loc[index, ('task_answers')] = frame['answers'][2:4]
#     print(frame)
#     df.loc[index, ('task_answers')] = frame['page']
#     # except:
#     #     df.drop(df.index[index])
#     # if frame != None:
#     #     df.loc[index, ('data')] = json.dumps(frame.get('data'))
#     # else:
#     #     df.loc[index, ('data')] = None
# df.to_csv('reduceDataCH4.csv')

# print(type(df.loc[0, 'data']))
# str = '{"frame":1}'
# str = '{"frame":{"level":"easy","data":{"successRate":1,"minJumps":2,"jumps":2,"path":[2,1,0]}}}'
# a = eval(str)
# print(a['frame']['data'])
# jsonTest = json.dumps(str)
# print(json.loads(str).get('data'))

# temp = []

# with open('reduceCH4.csv', 'r', encoding='UTF-8') as f:
#     with open('reduceDataCH4.csv', 'w', newline='', encoding='UTF-8') as f1:
#         f1_csv = csv.writer(f1)
#         f1_csv.writerow(['id', 'time', 'ticket_id', 'task_answers'])

#         f_csv = csv.reader(f)
#         next(f_csv, None)
#         for index, row in enumerate(f_csv):
#             try:
#                 # print(row)
#                 frame = ast.literal_eval(row[3])
#                 # row[3] = frame['frame']['answer'][2:4]
#                 row[3] = frame['frame']['page']
#                 # if -1 in row[3]:
#                 #     continue
#                 f1_csv.writerow(row)
#             except:
#                 continue
# print(temp)


# def join(x):
#     res = []
#     for index in x.index:
#         res.append(x.loc[index, 'task_answers'])
#     return res

# def join(x):
#     res = [0 for y in range(10)]
#     startTime = x.loc[x.index[0], 'time']
#     for index, value in enumerate(x.index):
#         if index == len(x.index)-1 or x.loc[value, 'task_answers'] != x.loc[x.index[index + 1], 'task_answers']:
#             endTime = x.loc[value, 'time']
#             res[int(x.loc[value, 'task_answers'])] += pandas.Timedelta(
#                 pandas.to_datetime(endTime) - pandas.to_datetime(startTime)).seconds
#             startTime = endTime
#     print(res)
#     return res

# def join(x):
#     res = []
#     for index in x.index:
#         if len(res) == 0:
#             res.append(x.loc[index, 'task_answers'])
#         if x.loc[index, 'task_answers'] != res[-1]:
#             res.append(x.loc[index, 'task_answers'])
#     return res

# def join(x):
#     # print(x)
#     # print(x.index[-1])
#     # print(x.loc[x.index[-1]])
#     return x.loc[x.index[-1], 'time']


# df = pandas.read_csv('reduceDataCH4.csv')
# df2 = pandas.read_csv('joinCH4.csv')
# df = df.groupby('ticket_id').apply(join)
# df.to_csv('joinCH42.csv')
# df = pandas.read_csv('joinCH42.csv')
# df2['endTime'] = df['0']

# # df['ticket_id'] = df['ticket_id'].astype(str)
# # df2['ticket_id'] = df2['ticket_id'].astype(str)

# print(df)
# print(df2)
# df2.to_csv('test.csv')
# newDF = pandas.merge(df2, df, how='left', on='ticket_id')

# print(newDF)
# # # df.to_csv("join2CH4.csv")
# newDF.to_csv('test.csv')

df = pandas.read_csv('test.csv', index_col=0)
df2 = pandas.read_csv('2.csv')
df22 = pandas.read_csv('20211117.csv')

df = df.merge(df2, how='left', on='ticket_id')
df = df.merge(df22, how='left', on='ticket_id')
df['start_time'] = pandas.to_datetime(df.start_time)
df.rename({'ticket_id': 'STU_CODE', 'start_time': 'startTime'},
          axis=1, inplace=True)
df3 = pandas.read_csv('./20210930ch4.csv', index_col=0)
df3 = df3[['STU_CODE', 'total_level', 'INQUIRY_level', 'REASONING_level', 'EXPLANATION_level',
           'total_score', 'INQUIRY_score', 'REASONING_score', 'EXPLANATION_score', 'TOTAL_CH4_RATE']]
df = df.merge(df3, how='left', on='STU_CODE')
df = df.dropna()
df['length'] = df['seq'].str.len()
df = df[df['length'] <= 15]
df['duration'] = 0
for index in df.index:
    df.loc[index, 'duration'] = pandas.Timedelta(
        pandas.to_datetime(df.loc[index, 'endTime']) - pandas.to_datetime(df.loc[index, 'startTime'])).seconds
df = df.sort_values(by='duration', ignore_index=True)
df.to_csv('final.csv')
print(df)
