import pandas as pd
import json 
import numpy as np
import ast
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.offline as offline
import plotly.figure_factory as ff
from pandas.core.indexes import interval
import re
# 2021-07-16T19:31:13+08:00
def get_interval_per_row(index, df):
    row_data = df.loc[index,:]
    start_time = row_data['start_time']
    if start_time != start_time:
        return -1
    start_time = datetime.strptime(str(start_time),"%Y-%m-%dT%H:%M:%S+08:00")

    expire_time = row_data['expire_time']
    if expire_time != expire_time:
        return -1
    expire_time = datetime.strptime(str(expire_time),"%Y-%m-%dT%H:%M:%S+08:00")

    stop_time = row_data['stop_time']
    if stop_time != stop_time:
        return -1
    stop_time = datetime.strptime(str(stop_time),"%Y-%m-%dT%H:%M:%S+08:00")

    total_minu = (stop_time - start_time).seconds / 60.0
    return total_minu

def remove_str_per_row(data_per_row):
    frame_list = ast.literal_eval(data_per_row)
    frame_dic_list = []
    for index in range(len(frame_list)):
        temp = json.loads(frame_list[index])
        if 'frame' in temp.keys():
            if 'data' in temp.keys():
                frame_dic_list.append(list(temp['frame']['data'].values())) 
            else:
                frame_dic_list.append(list(temp['frame'].values())) 
        else:
            frame_dic_list.append(temp) 
    return frame_dic_list
df_main = pd.read_csv('./20210717_2/data/data.csv')  
time_minu_list = []
drop_index_list = []
for row in range(len(df_main)):
    interval_minu = get_interval_per_row(row, df_main)
    if interval_minu == -1:
        drop_index_list.append(row)
    else:
        time_minu_list.append(interval_minu)
df_main = df_main.drop(drop_index_list)
if 'interval_minutes' not in df_main.columns:
    df_main.insert(len(df_main.columns), 'interval_minutes', time_minu_list)
grouped_main = df_main.groupby('contest_id')
df_contest_list = [tup[1] for tup in list(grouped_main)]
df_contest_name_list = [tup[0] for tup in list(grouped_main)]
df_res_1 = df_contest_list[0] # 智能计算
df_res_2 = df_contest_list[1] # 问题解决
x1 = []
x2 = []

for row in range(len(df_res_1)):
    print(row)
    interval = df_res_1.iloc[row, 17]
    if interval != -1:
        x1.append(interval)

for row in range(len(df_res_2)):
    interval = df_res_2.iloc[row, 17]
    if interval != -1:
        x2.append(interval)


layout={"title": "学生用时分布", 
                                       "xaxis_title": "学生用时，单位秒",
                                       "yaxis_title": "学生个数",
                                       # x轴坐标倾斜60度
                                       "xaxis": {"tickangle": 60}
                                      }

#数据组
hist_data=[x1,x2]

group_labels=['智能计算','问题解决']

fig=ff.create_distplot(hist_data,group_labels,bin_size=10,histnorm = 'probability')
fig['layout'].update(xaxis = dict(range = [0,100]))
plot(fig,filename='./plot/时间分布直方图.html')