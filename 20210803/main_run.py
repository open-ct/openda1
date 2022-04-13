# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # 计算思维数据处理
# %% [markdown]
# 数据处理要求：
# ### 1、每个题的平均作答时长；——结果数据
# ### 2、每个题的编码种类（有多少种，分别是什么，每种多少学生）；——结果数据
# 3、每个题的每个操作步骤的平均作答时长；——过程数据
# ### 4、正确率（暂未提供标准编码，可以探索一下题目本身，协助形成标准答案编码）；——结果数据
# 5、关键节点（通过数据，探索学生在从初始状态向终止状态进行的过程中，有几个关键步骤，每个关键步骤有几种类型的关键节点编码），体现“用数据说话”去探索关键节点。——过程数据
# 6、每个题目的每种编码下，都有什么样的学生作答类型，比如都是正确的，但是可以聚成多少类，每一类有什么特征，学生是通过什么样的操作路径到达最终的。
# ### 7、每道题目的正确率；——结果数据
# 
# <font color="red">注意 要求点四和要求点七相同，将一同分析
# %% [markdown]
# ## 0、数据加载和预处理
# 首先读取数据，并通过pandas进行数据帧处理
# 为了排版整洁和处理方便，以及保证工具的可拓展性，这里将处理工具封装成`data_analysis`的python类，并在jupyter中调用，该类在jupyter notebook同文件夹下的`main.py`文件中

# %%
# 首先引入需要的第三方库
import math
import pandas as pd
import json 
import numpy as np
import ast
from datetime import datetime
from pandas.core import groupby
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.offline as offline
from pandas.core.indexes import interval
import plotly.figure_factory as ff
pyolt=plot
import plotly.express as px
import math
import re

# %%
# 从main.py中引用对应的工具
from main import data_analysis

# %%
# 尝试将不同学校分开分析
df_all = pd.read_excel('./data/ticket_user_mianyang.xlsx')  
#%%
school_list = [tup[0] for tup in list(df_all.groupby('school'))][1:]                    # 这里从index=1开始向后取元素是为了避开demo 
df_list = [tup[1].reset_index(drop=True) for tup in list(df_all.groupby('school'))][1:] # 注意将index重置
df_entity_list = [data_analysis(df = df, name = school_list[i]) for i, df in enumerate(df_list)]

# %%
# 计算正确率并输出结果到output
for df_en in df_entity_list:
    df_en.calculate_acc()
    df_en.output()

# %%
# 首先将excel文件读取为pandas的dataframe类型
# 然后将该dataframe作为参数以初始化对应的数据处理工具，这里没有对excel文件进行预处理，
#   超时数据已经删除，但是并没有对不同学校进行学生分类，所以命名为'df_all'
# df_all = pd.read_excel('./data/ticket_user_mianyang.xlsx')  
# dataframe并不直接对其进行处理，而是作为参数初始化一个类的实体，这样的好处是可以避免大量的代码冗余
#    在对不同学校和不同数据行进行分类后处理时，只需要额外生成新的类的实体即可
#    在这里对应所有数据行直接生成一个实体，命名为'df_all_entity'
#    注意在参数里有一个命名为'name'的参数，这里是方便在调试过程中快速判断出问题的是哪个dataframe
df_all_entity =  data_analysis(df = df_all, name = 'all')
# 该步骤运行时间较长，在32秒左右


# %%
# ## 每道题的编码种类和正确率分析
print("题目个数为：",len(df_all_entity.count_df_list))
print("参与答题总次数：",df_all_entity.row_num)

accuracy_list, addition_list = df_all_entity.calculate_acc()
prob_name_list = ['小松鼠跳柱子（1）','小松鼠跳柱子（2）','填充小石子（1）','填充小石子（2）','嵌套的矩形（1）','嵌套的矩形（2）','模式的复制（1）','模式的复制（2）','浇花（1）','浇花（2）','密码（1）','密码（2）','4进制编码（1）','4进制编码（2）','供水系统（1）','供水系统（2）', '对应的形状（1）','对应的形状（2）','滚筒（1）']
dis_list = [(prob_name_list[i], acc) for i, acc in enumerate(accuracy_list)]
dis_list

print('calculate done')

# %%
# 判断每一行中22个题目是否正确

def judge_all_data(df_all_entity, data_all, addition_list):
    columns_list = []
    for i, data in enumerate(data_all):
        data = df_all_entity.content_to_str(data)
        if i in [0,1,2,3]:
            if data in addition_list[i].index:
                columns_list.append(data)
                columns_list.append(addition_list[i].loc[data, 'success'])
            else:
                columns_list.append(data)
                columns_list.append('0')
        elif i in [5,6,7,8,18,19]:
            if data in addition_list[i-1].index:
                columns_list.append(data)
                columns_list.append(addition_list[i-1].loc[data, 'success'])
            else:
                columns_list.append(data)
                columns_list.append('0')
        elif i in [9]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None and len(list_temp)==2 and type(list_temp[0])==str:
                if list_temp[0][0:2] > list_temp[0][-2:]:
                    list_temp[0] = list_temp[0][-2:] + '_' + list_temp[0][0:2]
                if list_temp[1][0:2] > list_temp[1][-2:]:
                    list_temp[1] = list_temp[1][-2:] + '_' + list_temp[1][0:2]
                if list_temp[0] > list_temp[1]:
                    list_temp =  str([list_temp[1], list_temp[0]])
                else:
                    list_temp =  str(list_temp)
            else:
                list_temp =  str(list_temp)

            columns_list.append(list_temp)
            if list_temp in addition_list[8].index:
                columns_list.append(addition_list[8].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            
        elif i in [10]:
            list_temp = ast.literal_eval(data)
            if type(list_temp)==list and len(list_temp)>=1 and type(list_temp[0]) == str:
                list_temp = [[int(rebuild_i) for rebuild_i in re.findall(r"\d+", str(rebuild))] for rebuild in list_temp]
                for list_mem in list_temp:
                    list_mem.sort()
                list_temp.sort()
                list_temp = str([str(list_str[0]) + '_' + str(list_str[1]) for list_str in list_temp])
                
            else:
                list_temp =  str(list_temp)
            columns_list.append(list_temp)
            if list_temp in addition_list[9].index:
                columns_list.append(addition_list[9].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [11]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp =  ''
            columns_list.append(list_temp)
            if list_temp in addition_list[10].index:
                columns_list.append(addition_list[10].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [12]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp =  ''

            columns_list.append(list_temp)
            if list_temp in addition_list[11].index:
                columns_list.append(addition_list[11].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [13]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp = ''
            columns_list.append(list_temp)
            if list_temp in addition_list[12].index:
                columns_list.append(addition_list[12].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [14]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp = ''
            columns_list.append(list_temp)
            if list_temp in addition_list[13].index:
                columns_list.append(addition_list[13].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [15]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp = ''
            columns_list.append(list_temp)
            if list_temp in addition_list[14].index:
                columns_list.append(addition_list[14].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [16]:
            list_temp = ast.literal_eval(data)

            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp = ''
            columns_list.append(list_temp)
            if list_temp in addition_list[15].index:
                columns_list.append(addition_list[15].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        elif i in [17]:
            list_temp = ast.literal_eval(data)
            if list_temp!=None:
                list_temp = "".join(re.findall(r"\d+", str(list_temp)))
            else:
                list_temp = ''
            columns_list.append(list_temp)
            if list_temp in addition_list[16].index:
                columns_list.append(addition_list[16].loc[list_temp, 'success'])
            else:
                columns_list.append('0')
            # columns_list.append(addition_list[i-1].loc[df_all_entity.content_to_str(data_all[i]), 'success'])
        
        elif i in [4,20,21]:
            columns_list.append(data)
            columns_list.append('unknow')
        
    return columns_list

df_column_prob_index = df_all_entity.df.index

df_column_prob_columns = []
for pro in range(22):
    df_column_prob_columns.append(str(pro))
    df_column_prob_columns.append('success_'+str(pro))

for df in addition_list:
    if 'list' in df.columns and 'success' in df.columns:
        for row in df.index:
            df._set_value(row,'list', str(df.loc[row, 'list']))
        df.set_index('list', inplace = True)

df_column_prob_data = []
for row in df_all_entity.df.index:
    data_all = df_all_entity.df.loc[row, 'ans']
    if len(data_all) == 22:
        df_column_prob_data.append(judge_all_data(df_all_entity, data_all, addition_list))
    else:
        df_column_prob_data.append(['None']*44)
# for row in df_all_entity.df.index:
#%%
df_column_prob = pd.DataFrame(index=df_all_entity.df.index, columns=df_column_prob_columns, data=df_column_prob_data)
df_column_prob.to_excel('./output/单个学生题目正确统计.xlsx')
df_all_entity.df.to_excel('./output/单个学生题目正确统计（学生附加信息，二者index相同）.xlsx')
pd.concat([df_all_entity.df, df_column_prob], axis=1).to_excel('./output/单个学生题目正确统计(合并).xlsx')
#%%
# 作答时间分析，在原数据上增加'interval'（做题时间）、'day'、'hour_start'、'hour_end'
data1 = list(df_all_entity.df.loc[:, 'start_time_float'])
layout={"title": "学生用时分布", 
                                       "xaxis_title": "时间（24小时制）",
                                       "yaxis_title": "学生个数",
                                       # x轴坐标倾斜60度
                                       "xaxis": {"tickangle": 60}
                                      }

#数据组
hist_data=[data1]

group_labels=['做题时间分布']
import plotly.figure_factory as ff
fig=ff.create_distplot(hist_data,group_labels,bin_size=1,histnorm = 'probability')
fig['layout'].update(xaxis = dict(range = [0,24]))
plot(fig,filename='./plot/每小时回答人数统计.html')

hour_list = list(range(24))
hour_count_list = []
for hour in hour_list:
    hour_count_seq = df_all_entity.df.sort_values('start_hour').groupby('start_hour')['start_hour'].count()
    if hour not in list(hour_count_seq.index):
        hour_count_list.append(0)
    else:
        hour_count_list.append(hour_count_seq.loc[hour])

pd.DataFrame(index = hour_list, columns=['count'], data = hour_count_list).to_excel('./plot/每小时回答人数统计.xlsx')


# %%
# 正确率和编码个数绘图
## 正确的编码个数
data1 = go.Bar(x = prob_name_list, y = [len(group.groupby('success').get_group('1')) if '1' in group.groupby('success').groups.keys() else 0 for group in df_all_entity.addition_list], name = '回答中正确编码的个数')

## 错误编码的个数
data2 = go.Bar(x = prob_name_list, y = [len(group.groupby('success').get_group('0')) if '0' in group.groupby('success').groups.keys() else 0 for group in df_all_entity.addition_list], name = '回答中错误编码的个数')

## 回答正确率
data3 = go.Bar(x = prob_name_list, y = accuracy_list, name = '回答正确率')

success_count = []
for df in addition_list:
    if 'success' in df.columns:
        if '1' in df.groupby('success').groups.keys():
            success_count.append(df.groupby('success').get_group('1')['count'].sum())
        else:
            success_count.append(0)

layout={"title": "不同题目的编码数量和正确率", 
       "xaxis_title": "题目编号",
       "yaxis_title": "编码个数",
       # x轴坐标倾斜60度
       "xaxis": {"tickangle": 60}
      }
from plotly.subplots import make_subplots
fig = make_subplots(rows=3, cols=1)
fig.append_trace(data1, row = 1, col = 1)
fig.append_trace(data2, row = 2, col = 1)
fig.append_trace(data3, row = 3, col = 1)

# fig = go.Figure(data=[data1, data2, data3],layout=layout)
plot(fig,filename="./plot/不同题目的编码数量和正确率.html",auto_open=False,image='png',image_height=800,image_width=1500)
pd_list = []
for i, row in enumerate(data1.y):
    pd_list.append([data1.y[i], data2.y[i], data3.y[i], success_count[i]])

pd.DataFrame(index=prob_name_list, columns=[data1.name, data2.name, data3.name, 'success_count'], data= pd_list).to_excel('./plot/不同题目的编码数量和正确率.xlsx')

#%%

data1 = go.Bar(x = school_list, y = [np.mean(df.accuracy_list) for df in df_entity_list], name = '各个学校的平均正确率')
data2 = go.Bar(x = school_list, y = [df.row_num for df in df_entity_list], name = '各个学校的参加人数')
layout={"title": "各个学校的平均正确率", 
       "xaxis_title": "学校名称",
       "yaxis_title": "正确率",
       # x轴坐标倾斜60度
       "xaxis": {"tickangle": 60}
      }
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=1)
fig.append_trace(data1, row = 1, col = 1)
fig.append_trace(data2, row = 2, col = 1)

plot(fig,filename="./plot/各个学校的平均正确率和参加人数.html",auto_open=False,image='png',image_height=800,image_width=1500)
pd_list = []
for i, row in enumerate(data1.y):
    pd_list.append([data1.y[i], data2.y[i]])
pd.DataFrame(index=school_list, columns=[data1.name, data2.name], data= pd_list).to_excel('./plot/各个学校的平均正确率和参加人数.xlsx')
# %% [markdown]
# # 正确答案编码
# %%
# 模拟第19题的答案编码，遍历所有答案
# 所有可能的五角星（0,a）和三角形（1,b）组合
seq_list = []
for i in range(8):
    for j in range(int(math.pow(2,i+1))):
        temp=str(bin(j))[2:].zfill(i+1).replace('0','a')
        temp = temp.replace('1', 'b')
        seq_list.append(temp)
# 所有可能的长方形（1）和圆形（0）组合
trans_list = []
for i in range(3):
    for j in range(int(math.pow(2,i+1))):
        trans_list.append(str(bin(j))[2:].zfill(i+1))
# 正确序列 
verify_str = '10100010010'
right_ans = []
cnt = 0
for seq in seq_list:
    for star in trans_list:
        for trian in trans_list:
            cnt +=1
            if seq.replace('a', star).replace('b', trian) == verify_str:
                right_ans.append([seq.replace('a','0').replace('b','1'), star, trian])
right_ans
# %%
# 模拟滚筒（2）的过程，遍历所有的答案
# 
import math
def roll_one_time(first_dic, second_dic, verify_list):
    max_length = len(verify_list)
    line_list = [-1] * max_length
    # first roll
    for i in range(first_dic['start'], first_dic['end']+1):
        line_list[i] = first_dic['color_list'][i % len(first_dic['color_list'])]

    # second roll
    for i in range(second_dic['start'], second_dic['end']+1):
        line_list[i] = second_dic['color_list'][i % len(second_dic['color_list'])]
    
    is_right = True
    for i, c in enumerate(line_list):
        if c != verify_list[i]:
            is_right = False
            break
    if is_right:
        return is_right, [first_dic, second_dic]
    else:
        return is_right, []


def traverse_color(min_roll_length = 2, max_roll_length = 5, colors = [0,1,2]):
    color_lists = []
    for i in range(min_roll_length, max_roll_length+1):
        for j in range(int(math.pow(len(colors), i))):
            tmp_list = []
            for k in range(i):
                tmp_list.insert(0, colors[j % len(colors)]) 
                j = j // len(colors)
            color_lists.append(tmp_list)
    return color_lists

def traverse_position(start_bound = 0, end_bound = 15):
    position_list = []
    start_list = range(start_bound,end_bound+1)
    end_list = range(start_bound,end_bound+1)
    for s in start_list:
        for e in end_list:
            if e>s:
                position_list.append((s, e))
    return position_list

def traverse_roll(min_roll_length = 2, max_roll_length = 5, colors = [0,1,2], start_bound = 0, end_bound = 15):
    roll_dic_list = []
    for cl in traverse_color(min_roll_length, max_roll_length, colors):
        for p in traverse_position(start_bound, end_bound):
            if p[1]-p[0]+1>=len(cl):
                tmp_dic = {'color_list':[], 'start':0, 'end':0}
                tmp_dic['color_list']=cl
                tmp_dic['start'] = p[0]
                tmp_dic['end'] = p[1]
                roll_dic_list.append(tmp_dic)
    return roll_dic_list

# %%
# search from bottom to top

posible_roll = traverse_roll()
len(posible_roll)

# %%
posible_colors = traverse_color()
len(posible_colors)

# %%
posible_position = traverse_position()
len(posible_position)
# %%
# 从最后一次滚筒开始找起（第二次）
verify_list = [0, 1, 0, 1, 2, 2, 0, 1, 1, 2, 2, 0, 1, 1, 0, 1]
line_list = [-1]*len(verify_list)

posible_roll2_list = []
for roll2 in posible_roll:
    
    roll2_is_posible = True
    for index in range(roll2['start'], roll2['end']+1):
        if roll2['color_list'][((index-roll2['start']) % len(roll2['color_list']))] != verify_list[index]:
            roll2_is_posible = False
    if roll2_is_posible:
        posible_roll2_list.append(roll2)
len(posible_roll2_list)

# %%
# 根据所有可能的roll2寻找roll1
posible_roll1_roll2 = []
cnt = 0
for roll2 in posible_roll2_list:
    print(cnt)
    cnt += 1
    flag_list = [-1]*len(verify_list)
    for index2 in range(roll2['start'], roll2['end']+1):
        flag_list[index2] = -2
    for roll1 in posible_roll:
        flag_list_ = [i for i in flag_list]

        roll1_is_posible = True
        for index1 in range(roll1['start'], roll1['end']+1):
            if flag_list_[index1] == -1:
                flag_list_[index1] = -3
        if -1 in flag_list_:
            roll1_is_posible = False
            continue

        for index1 in range(roll1['start'], roll1['end']+1):
            if roll1['color_list'][((index1-roll1['start']) % len(roll1['color_list']))] != verify_list[index1] and flag_list_[index1] == -3:
                roll1_is_posible = False
                break
        if roll1_is_posible:
            posible_roll1_roll2.append((roll1, roll2))


# %%
len(posible_roll1_roll2)
# %%
posible_roll1_roll2
# %% [markdown]
# 所有可能的答案：
'''python
posible_roll1_roll2
[({'color_list': [0, 1], 'start': 0, 'end': 15},
  {'color_list': [1, 2, 2, 0, 1], 'start': 3, 'end': 12}),
 ({'color_list': [0, 1, 0, 1], 'start': 0, 'end': 15},
  {'color_list': [1, 2, 2, 0, 1], 'start': 3, 'end': 12}),
 ({'color_list': [0, 1], 'start': 0, 'end': 15},
  {'color_list': [1, 2, 2, 0, 1], 'start': 3, 'end': 13}),
 ({'color_list': [0, 1, 0, 1], 'start': 0, 'end': 15},
  {'color_list': [1, 2, 2, 0, 1], 'start': 3, 'end': 13}),
 ({'color_list': [0, 1], 'start': 0, 'end': 15},
  {'color_list': [2, 2, 0, 1, 1], 'start': 4, 'end': 12}),
 ({'color_list': [0, 1, 0, 1], 'start': 0, 'end': 15},
  {'color_list': [2, 2, 0, 1, 1], 'start': 4, 'end': 12}),
 ({'color_list': [0, 1], 'start': 0, 'end': 15},
  {'color_list': [2, 2, 0, 1, 1], 'start': 4, 'end': 13}),
 ({'color_list': [0, 1, 0, 1], 'start': 0, 'end': 15},
  {'color_list': [2, 2, 0, 1, 1], 'start': 4, 'end': 13})]
'''

#%% 
# 对于滚筒（3），遍历的计算复杂度太高，这里只给出验证函数
def verify_roll_3(roll1, roll2, roll3, verify_list = [1,0,1,2,1,0,2,2,1,2,0,1,2,0,2,2,1,0,2,0]):
    flag_list = [-1]*len(verify_list)
    for index3 in range(roll3['start'], roll3['end']+1):
        if verify_list[index3] != roll3['color_list'][((index3-roll3['start']) % len(roll3['color_list']))]:
            return False
        flag_list[index3] = '3'
    
    for index2 in range(roll2['start'], roll2['end']+1):
        if flag_list[index2] == -1:
            if verify_list[index2] != roll2['color_list'][((index2-roll2['start']) % len(roll2['color_list']))]:
                return False
            flag_list[index2] = '2'
    
    for index1 in range(roll1['start'], roll1['end']+1):
        if flag_list[index1] == -1:
            if verify_list[index1] != roll1['color_list'][((index1-roll1['start']) % len(roll1['color_list']))]:
                return False
            flag_list[index1] = '1'
    
    if -1 in flag_list:
        return False
    else:
        return True

#%%
posible_roll = traverse_roll(min_roll_length = 2, max_roll_length = 4, colors = [0,1,2], start_bound = 0, end_bound = 19)
len(posible_roll)

#%%
# 从最后一次滚筒开始找起（第三次）
verify_list = [1,0,1,2,1,0,2,2,1,2,0,1,2,0,2,2,1,0,2,0]
line_list = [-1]*len(verify_list)

posible_roll3_list = []
for roll3 in posible_roll:
    
    roll3_is_posible = True
    for index in range(roll3['start'], roll3['end']+1):
        if roll3['color_list'][((index-roll3['start']) % len(roll3['color_list']))] != verify_list[index]:
            roll3_is_posible = False
    if roll3_is_posible:
        posible_roll3_list.append(roll3)
len(posible_roll3_list)

#%%
# 根据所有可能的roll3寻找roll2
posible_roll2_roll3 = []
cnt = 0
for roll3 in posible_roll3_list:
    print(cnt)
    cnt += 1
    flag_list = [-1]*len(verify_list)
    for index3 in range(roll3['start'], roll3['end']+1):
        flag_list[index3] = '3'
    for roll2 in posible_roll:
        flag_list_ = [i for i in flag_list]

        roll2_is_posible = True

        # if roll2['start']>=roll3['start'] and roll2['end']<=roll3['end']:
        #     roll2_is_posible = False
        #     continue

        for index2 in range(roll2['start'], roll2['end']+1):
            if flag_list_[index2] == -1 and roll2['color_list'][(index2-roll2['start']) % len(roll2['color_list'])] != verify_list[index2]:
                roll2_is_posible = False
                break

        if roll2_is_posible:
            posible_roll2_roll3.append((roll2, roll3))

# %%
len(posible_roll2_roll3)
# %%
verify_list = [1,0,1,2,1,0,2,2,1,2,0,1,2,0,2,2,1,0,2,0]
all_right_ans=[]
cnt = 0
for roll23 in posible_roll2_roll3:
    print(cnt,len(all_right_ans))
    cnt+=1
    for roll1 in posible_roll:
        if min([roll1['start'], roll23[0]['start'], roll23[1]['start']])!=0 or max([roll1['end'], roll23[0]['end'], roll23[1]['end']])!=len(verify_list)-1:
            continue
        if verify_roll_3(roll1, roll23[0], roll23[1], verify_list):
            all_right_ans.append((roll1, roll23[0], roll23[1]))

# %%
len(all_right_ans)
# %%
all_right_ans
# %% [markdown]
## 共有15种正确答案
'''python
[({'color_list': [1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 12}),
 ({'color_list': [1, 0, 1], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 12}),
 ({'color_list': [1, 0, 1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 12}),
 ({'color_list': [1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 13}),
 ({'color_list': [1, 0, 1], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 13}),
 ({'color_list': [1, 0, 1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [1, 2, 0], 'start': 8, 'end': 13}),
 ({'color_list': [1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 12}),
 ({'color_list': [1, 0, 1], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 12}),
 ({'color_list': [1, 0, 1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 12}),
 ({'color_list': [1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 13}),
 ({'color_list': [1, 0, 1], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 13}),
 ({'color_list': [1, 0, 1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1], 'start': 9, 'end': 13}),
 ({'color_list': [1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1, 2], 'start': 9, 'end': 12}),
 ({'color_list': [1, 0, 1], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1, 2], 'start': 9, 'end': 12}),
 ({'color_list': [1, 0, 1, 0], 'start': 0, 'end': 19},
  {'color_list': [2, 1, 0, 2], 'start': 3, 'end': 18},
  {'color_list': [2, 0, 1, 2], 'start': 9, 'end': 12})]
'''