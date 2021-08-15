#!/usr/bin/env python
# coding: utf-8

# # 需求（18日单日数据）
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
        return -1
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


df_main = pd.read_csv('./data/data-single-day.csv')  
df_main


# # 测试函数运行是否正常

# In[5]:


dic_list_test = remove_str_per_row(df_main.loc[1, 'task_answers'])
dic_list_test, len(dic_list_test)
time_test_minu = get_interval_per_row(0, df_main)
time_test_minu


# # 增加做题时间属性（'interval'）

# In[6]:


time_minu_list = []
drop_index_list = []
for row in range(len(df_main)):
    interval_minu = get_interval_per_row(row, df_main)
    if interval_minu == -1:
        drop_index_list.append(row)
    else:
        time_minu_list.append(interval_minu)


# In[7]:


len(df_main)


# In[8]:


len(drop_index_list)


# In[9]:


len(time_minu_list)


# In[10]:


df_main = df_main.drop(drop_index_list)
if 'interval_minutes' not in df_main.columns:
    df_main.insert(len(df_main.columns), 'interval_minutes', time_minu_list)


# # 数据针对试卷分类

# In[11]:


grouped_main = df_main.groupby('contest_id')
df_contest_list = [tup[1] for tup in list(grouped_main)]
df_contest_name_list = [tup[0] for tup in list(grouped_main)]


# In[12]:


df_contest_name_list


# # 分类结果
# 智能计算和问题解决分别在列表中的index=1和index=2

# In[13]:


df_res_1 = df_contest_list[0] # 智能计算
df_res_2 = df_contest_list[1] # 问题解决
print("各个问卷回答时间：")
print(grouped_main['interval_minutes'].mean())

# # 教师和校长数量

# In[14]:


print("教师和校长数量", len(df_contest_list[2]), len(df_contest_list[3]))


# # 智能计算学生数量

# In[15]:


x1_sum = len(df_contest_list[0])
print("当日智能计算总数", x1_sum)


# # 问题解决学生数量

# In[16]:


x2_sum = len(df_contest_list[1])
print("当日问题解决总数", x2_sum)


# # 学生总数

# In[17]:


print("当日学生总数", x1_sum + x2_sum)


# # 再将教师和校长的数据剔除

# In[18]:


[tup[0] for tup in list(df_res_1.groupby('tag'))]


# In[19]:


[tup[0] for tup in list(df_res_2.groupby('tag'))]


# # 提取最终画图用到的dataframe

# In[20]:


df_res_1.columns


# In[21]:


x1 = []
x2 = []

for row in range(len(df_res_1)):
    interval = df_res_1.iloc[row, 17]
    if interval != -1:
        x1.append(interval)

for row in range(len(df_res_2)):
    interval = df_res_2.iloc[row, 17]
    if interval != -1:
        x2.append(interval)


# In[22]:




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
plot(fig,filename='./plot/单日时间分布直方图.html')
offline.iplot(fig) 


# In[23]:


x1_ary, _ = np.histogram(x1, bins=[0,10,20,30,40,50,60])
x1_list = list(x1_ary)
x1_list.append(x1_sum - x1_ary.sum())
print("当日智能计算时间分布",x1_list)


# In[24]:


x2_ary, _ = np.histogram(x2, bins=[0,10,20,30,40,50,60])
x2_list = list(x2_ary)
x2_list.append(x2_sum - x2_ary.sum())
print("当日问题解决时间分布",x2_list)



# In[25]:


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


# In[26]:


import plotly as py
import plotly.graph_objs as go
pyplt=py.offline.plot
labels=['0~10分钟','10~20分钟','20~30分钟','30~40分钟','40~50分钟', '50～60分钟', '超过60分钟']
values=x1_list
trace=[go.Pie(labels=labels,values=values)]
layout=go.Layout(
    title='智能计算做题时间分布比例图(当日)'
)
fig=go.Figure(data=trace,layout=layout)
fig.update_traces(hoverinfo='label+percent',
#  textinfo='value', 
 textfont_size=20, marker=dict(colors=plotly.colors.qualitative.Plotly[0:7], line=dict(color='#000000', width=2)))
pyplt(fig,filename='plot/单日智能计算时间分布饼图.html')
offline.iplot(fig) 


# In[27]:


import plotly as py
import plotly.graph_objs as go
pyplt=py.offline.plot
labels=['0~10分钟','10~20分钟','20~30分钟','30~40分钟','40~50分钟', '50～60分钟', '超过60分钟']
values=x2_list
trace=[go.Pie(labels=labels,values=values)]
layout=go.Layout(
    title='问题解决做题时间分布比例图（当日）'
)
fig=go.Figure(data=trace,layout=layout)
fig.update_traces(hoverinfo='label+percent',
#  textinfo='value', 
 textfont_size=20, marker=dict(colors=plotly.colors.qualitative.Plotly[0:7], line=dict(color='#000000', width=2)))
pyplt(fig,filename='plot/问题解决时间分布饼图.html')
offline.iplot(fig) 


# # 以下找出偷懒学校排名

# 首先对偷懒学生（做题时间十分钟以下），添加列'lazy',真值为'1'

# In[28]:


# df_main.loc[0, 'interval_minutes']
df_main.columns
df_main.iloc[0,17]


# In[29]:


lazy_list = []
for row in range(len(df_main)):
    if df_main.iloc[row, 17] <= 10:
        lazy_list.append(1)
    else:
        lazy_list.append(0)
if 'lazy' not in df_main.columns:
    df_main.insert(len(df_main.columns), 'lazy', lazy_list)


# In[30]:


school_list =[tup[0] for tup in list(df_main.groupby('school'))] 
df_school_list = [tup[1] for tup in list(df_main.groupby('school'))] 


# In[31]:


school_total_list = [len(df) for df in df_school_list]


# In[32]:


df_lazy_count = pd.DataFrame(df_main.groupby('school')['lazy'].sum())
df_total_count = pd.DataFrame(df_main.groupby('school')['lazy'].count())


# In[33]:


df_lazy_count.insert(len(df_lazy_count.columns), 'total', list(df_total_count.loc[:, 'lazy']))
df_res = df_lazy_count


# In[34]:


ritio_list = []
for row in range(len(df_res)):
    ritio_list.append(float(df_res.iloc[row, 0]) / float(df_res.iloc[row, 1]))
df_res.insert(len(df_res.columns), 'ritio', ritio_list)


# In[35]:


df_res.sort_values(by = 'lazy', ascending=False).to_excel('./output/学生偷懒状况（按学校分类）(当日).xlsx')


# In[36]:


df_res.sort_values(by = 'lazy', ascending=False)


# In[ ]:




