#!/usr/bin/env python
# coding: utf-8

# # 需求（和20210718中类似）
# 这是截至目前科学问题解决的作答数据，现在需要请你帮忙做一个跟之前日报类似的作答时长的分析。首先，需要你将数据文件中无关的作答删除，比如demo账号、学校为协同中心的试测账号；然后，计算所有有stop时间的学生的作答时长（用stop时间减去start时间），并且以每10分钟为一档（0-10分钟、10-20分钟、……50-60分钟）统计出作答的人数及比例，并且画出饼状图，特别注意，可能会存在一些超过60分钟的学生，这可能是系统计时不准确，所以这部分也算到50-60分钟内；然后，将所有没有stop时间的学生单独分为一类，称为作答超时学生，也要算出这部分学生的人数和比例，并且也要画到刚才的饼状图中。最后你需要给出一个EXCEL的统计表以及一张饼状图。辛苦你最晚明天早上发到群里，有什么问题可以随时在群里提出。@LHF 师姐，你这边还有什么要补充的需求吗？
# ## 1、统计人数
# 截止到2021年7月17日晚上20:30左右，当天有学生XX人次、XX名教师、XX名校长完成了测试；累计共有学生XX人次、XX名教师、XX名校长完成了测试。
# ## 2、作答时间
# 智能计算素养和问题解决素养两个专题的规定测试时间均为60分钟，截止目前完成测试学生实际作答的平均时间为XX分钟。
# 
# （一）智能计算素养专题
# 
# 智能计算素养专题的题目在预测试中作答时长均值为40-50分钟，少数同学的作答时长在30分钟以下和1小时以上。7月17日当天，绵阳地区有XX名学生的实际作答时长小于等于10分钟，XX名学生的实际作答时长小于等于20分钟；XX名学生的实际作答时长小于等于30分钟。总体作答时长分布如下图：
# 
# 【一个7月17日当天学生完成作答智能计算素养专题的时长分布饼状图，时长单位为分钟，每10分钟一块就可以，每一块上标注上所占比例，超过60分钟的就一块“60分钟及以上”】
# 截止到7月17日20:30左右，累计共有XX名学生的实际作答时长小于等于10分钟，XX名学生的实际作答时长小于等于20分钟；XX名学生的实际作答时长小于等于30分钟。总体作答时长分布如下图：
# 
# 【一个累计学生完成作答智能计算素养专题的时长分布饼状图，时长单位为分钟，每10分钟一块就可以，每一块上标注上所占比例，超过60分钟的就一块“60分钟及以上”】
# 
# （二）问题解决素养专题
# 
# 问题解决素养专题的题目在预测试中33%的学生作答时间超过45分钟，23%的学生超过50分钟，9%的学生超过60分钟，大部分学生都需要50分钟才能完成测试。7月17日当天，绵阳地区有XX名学生的实际作答时长小于等于10分钟，XX名学生的实际作答时长小于等于20分钟；XX名学生的实际作答时长小于等于30分钟。总体作答时长分布如下图：
# 
# 【一个7月17日当天学生完成作答问题解决专题的时长分布饼状图，时长单位为分钟，每10分钟一块就可以，每一块上标注上所占比例，超过60分钟的就一块“60分钟及以上”】
# 
# 截止到7月17日20:30左右，累计共有XX名学生的实际作答时长小于等于10分钟，XX名学生的实际作答时长小于等于20分钟；XX名学生的实际作答时长小于等于30分钟。总体作答时长分布如下图：
# 
# 【一个累计学生完成作答问题解决素养专题的时长分布饼状图，时长单位为分钟，每10分钟一块就可以，每一块上标注上所占比例，超过60分钟的就一块“60分钟及以上”】
# 
# ## 3、作答学校分布
# 7月17日当天，作答时长小于等于10分钟的学生所在学校（大于10人）：
# 
# 学校名称  ｜  人数
# 
# 
# 累计到7月17日20:30左右，作答时长小于等于10分钟的学生所在学校（大于50人）：
# 
# 学校名称  ｜  人数
# ## 4、输出EXCEL文件
# 添加一列做题时长

# # 首先引入第三方库

# In[1]:


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


# # 提前定义每一行的计算时间函数

# In[2]:


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
        return '回答超时'
    stop_time = datetime.strptime(str(stop_time),"%Y-%m-%dT%H:%M:%S+08:00")

    total_minu = (stop_time - start_time).seconds / 60.0
    return total_minu


# # 提前定义转码task_answers字段的函数

# In[3]:


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


# # 读取数据

# In[4]:


df_main = pd.read_excel('./data/data.xlsx')  


# ## 删除不需要的数据
# 包括ticket_id为demo的数据和school为‘协同中心’的数据

# In[15]:


if 'demo' in df_main.groupby('school').groups.keys():
    df_main = df_main.drop(list(df_main.groupby('school').get_group('demo').index))
elif '协同中心' in df_main.groupby('school').groups.keys():
    df_main = df_main.drop(list(df_main.groupby('school').get_group('协同中心').index))
df_main = df_main.reset_index(drop = True)


# In[16]:


dic_list_test = remove_str_per_row(df_main.loc[1, 'task_answers'])
dic_list_test, len(dic_list_test)
time_test_minu = get_interval_per_row(0, df_main)
time_test_minu


# # 增加做题时间属性（'interval'）

# In[17]:


time_minu_list = []
drop_index_list = []
for row in range(len(df_main)):
    interval_minu = get_interval_per_row(row, df_main)
    if interval_minu == -1:
        drop_index_list.append(row)
    else:
        time_minu_list.append(interval_minu)


# In[18]:


len(df_main)


# In[19]:


len(drop_index_list)


# In[20]:


len(time_minu_list)


# In[33]:


df_main = df_main.drop(drop_index_list)
df_main = df_main.reset_index(drop=True)
if 'interval_minutes' not in df_main.columns:
    df_main.insert(len(df_main.columns), 'interval_minutes', time_minu_list)


# # 数据针对试卷分类

# In[22]:


grouped_main = df_main.groupby('contest_id')
df_contest_list = [tup[1] for tup in list(grouped_main)]
df_contest_name_list = [tup[0] for tup in list(grouped_main)]


# In[23]:


df_contest_name_list


# # 分类结果
# 智能计算和问题解决分别在列表中的index=1和index=2

# In[25]:


df_res_1 = df_contest_list[0] # 智能计算
# df_res_2 = df_contest_list[1] # 问题解决


# # 提取时间数据

# In[37]:


interval_data_dic = {
    '0~10':{'count':0,'index':[],'data':[]},
    '10~20':{'count':0,'index':[],'data':[]},
    '20~30':{'count':0,'index':[],'data':[]},
    '30~40':{'count':0,'index':[],'data':[]},
    '40~50':{'count':0,'index':[],'data':[]},
    '50~60':{'count':0,'index':[],'data':[]},
    '超时':{'count':0,'index':[]}
    }
for row in df_main.index:
    data_tmp = df_main.loc[row, 'interval_minutes']
    if data_tmp == '回答超时':
        interval_data_dic['超时']['count'] += 1
        interval_data_dic['超时']['index'].append(row)
        continue

    if data_tmp >= 0 and data_tmp < 10:
        interval_data_dic['0~10']['count'] += 1
        interval_data_dic['0~10']['index'].append(row)
    elif data_tmp >= 10 and data_tmp < 20:
        interval_data_dic['10~20']['count'] += 1
        interval_data_dic['10~20']['index'].append(row)
    elif data_tmp >= 20 and data_tmp < 30:
        interval_data_dic['20~30']['count'] += 1
        interval_data_dic['20~30']['index'].append(row)
    elif data_tmp >= 30 and data_tmp < 40:
        interval_data_dic['30~40']['count'] += 1
        interval_data_dic['30~40']['index'].append(row)
    elif data_tmp >= 40 and data_tmp < 50:
        interval_data_dic['40~50']['count'] += 1
        interval_data_dic['40~50']['index'].append(row)
    elif data_tmp >= 50:
        interval_data_dic['50~60']['count'] += 1
        interval_data_dic['50~60']['index'].append(row)


# # 提取最终画图用到的dataframe

# In[44]:


colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

layout={"title": "学生用时分布", 
                                       "xaxis_title": "学生用时，单位秒",
                                       "yaxis_title": "学生个数",
                                       # x轴坐标倾斜60度
                                       "xaxis": {"tickangle": 60}
                                      }

#数据组
x1 = []
for data in df_main.loc[:, 'interval_minutes']:
    if type(data)!=str:
        x1.append(data)

hist_data= [x1]

group_labels=['智能计算']

fig=ff.create_distplot(hist_data,group_labels,bin_size=10,histnorm = 'probability')
fig['layout'].update(xaxis = dict(range = [0,100]))
plot(fig,filename='./plot/总计时间分布直方图(不包含超时数据).html')
offline.iplot(fig) 


# In[45]:


colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]
colors[0:7]
import plotly
plotly.colors.qualitative.Plotly


# In[48]:



import plotly as py
import plotly.graph_objs as go
pyplt=py.offline.plot
labels=['0~10分钟','10~20分钟','20~30分钟','30~40分钟','40~50分钟', '50～60分钟', '超时']
values=[interval_data_dic[key]['count'] for key in interval_data_dic.keys()]

trace=[go.Pie(labels=labels,values=values)]
layout=go.Layout(
    title='智能计算做题时间分布比例图（累计）'
)
fig=go.Figure(data=trace,layout=layout)
fig.update_traces(hoverinfo='label+percent',
#  textinfo='value', 
 textfont_size=20, marker=dict(colors=plotly.colors.qualitative.Plotly[0:7], line=dict(color='#000000', width=2)))
pyplt(fig,filename='plot/总计智能计算时间分布饼图.html')
pd.DataFrame(index=labels, data = [[v] for v in values]).to_excel('plot/总计智能计算时间分布饼图.xlsx')
offline.iplot(fig) 


# In[71]:


import plotly as py
import plotly.graph_objs as go
pyplt=py.offline.plot
labels=['0~10分钟','10~20分钟','20~30分钟','30~40分钟','40~50分钟', '50～60分钟', '超过60分钟']
values=[interval_data_dic[key]['count'] for key in interval_data_dic.keys()]
trace=[go.Pie(labels=labels,values=values)]
layout=go.Layout(
    title='总计 问题解决做题时间分布比例图（累计）'
)
fig=go.Figure(data=trace,layout=layout)
fig.update_traces(hoverinfo='label+percent',
#  textinfo='value', 
 textfont_size=20, marker=dict(colors=plotly.colors.qualitative.Plotly[0:7], line=dict(color='#000000', width=2)))
pyplt(fig,filename='plot/总计问题解决时间分布饼图.html')
offline.iplot(fig) 


# # 以下找出偷懒学校排名

# 首先对偷懒学生（做题时间十分钟以下），添加列'lazy',真值为'1'

# In[ ]:




