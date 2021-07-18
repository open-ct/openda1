import pandas as pd
import json 
import numpy as np
import ast
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.offline as offline
from pandas.core.indexes import interval
import re

class data_analysis:
    def __init__(self, df, name = 'default') -> None:
        self.name = name
        self.with_successrate = [0, 1]
        self.problem_num = 23
        self.df = df
        self.row_num = len(df)
        self.df.insert(len(self.df.columns), 'ans', self.remove_str())
        # self.df.insert(len(self.df.columns), 'interval', self.get_interval())
        self.ndf = pd.DataFrame(self.create_new_df())
        self.ndf_list = self.divide_ndf()
        self.group_list = self.group_by()
        # self.count_df_list = self.count_group()
        # self.addition_list, self.success_df,self.problem_num_list = self.get_addition()
        # self.output_df = 0
        
        self.output()
        print('init complete')

    def remove_str_per_row(self, data_per_row):
        frame_list = ast.literal_eval(data_per_row)
        frame_dic_list = []
        for index in range(len(frame_list)):
            frame_dic_list.append(json.loads(frame_list[index])) 
        return frame_dic_list

    def remove_str(self):
        ndf_ans_8_list = []
        ndf_rm_frame = []
        for i in range(self.row_num):
            dic_temp = self.remove_str_per_row(self.df.loc[i,'task_answers'])
            ndf_ans_8_list.append(dic_temp)
            new_dic_list = []
            for dic in dic_temp:
                dic = dic['frame']
                new_dic = dic
                new_dic_list.append(new_dic)
            ndf_rm_frame.append(new_dic_list)

        return ndf_rm_frame
    
    def get_interval(self):
        interval_list = []
        for i in range(len(self.df)):
            interval_list.append(self.get_interval_per_row(i))
        return interval_list

    def get_interval_per_row(self, index):
        row_data = self.df.loc[index,:]
        start_time = row_data['start_time']
        start_time = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S+08:00")

        expire_time = row_data['expire_time']
        expire_time = datetime.strptime(expire_time,"%Y-%m-%dT%H:%M:%S+08:00")

        stop_time = row_data['stop_time']
        if stop_time != stop_time:
            return -1
        stop_time = datetime.strptime(stop_time,"%Y-%m-%dT%H:%M:%S+08:00")

        total_sec = (stop_time - start_time).seconds
        return total_sec
    
    def create_new_df(self):
        twoD_list = []
        for row in range(self.row_num):
            ans_dic_list = self.df.loc[row, 'ans']
            twoD_list.append(ans_dic_list)
        return twoD_list
    
    def divide_ndf(self):
        ndf_list = []
        for i in range(len(self.ndf.columns)):
            ndf_list.append(pd.DataFrame(self.ndf.loc[:,i]))
        return ndf_list
    
    def group_by_per_problem(self, index):
        df_temp = self.ndf_list[index]
        df_str_list = []
        for j in range(len(df_temp)):
            ndf_index_j = df_temp.iloc[j, 0]
            if ndf_index_j == None:
                df_str_list.append(str(None))
            else:
                df_str_list.append(self.content_to_str(ndf_index_j))
        df_temp.insert(1, 'ans_str', df_str_list)
        df_per_problom = df_temp.groupby('ans_str')
        return df_per_problom

    def content_to_str(self, data):
        if data == None:
            return str(None)
        elif type(data) == type([]):
            return self.data_to_str(data)
        elif 'data' in data.keys():
            return self.data_to_str(data['data'])
        else:
            return self.data_to_str(data)

    def data_to_str(self, data):
        if type(data) == type({}):
            return str(list(data.values()))
        else:
            return str(data)

    def group_by(self):
        group_list = []
        for i in range(self.problem_num):
            df_temp = self.group_by_per_problem(i)
            group_list.append(df_temp)
        return group_list

    def get_addition(self):
        addition_list = []
        accuracy_list = []
        for i, df in enumerate(self.count_df_list):
            additional_infor_df = pd.DataFrame({'list':[ast.literal_eval(index) for index in df.index]})
            additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( df.iloc[:, 0]))
            
            if i in self.with_successrate:
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['0' if l==None else str(l[0]) for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [2,3]:
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)!=0 and l[0]=='00' else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [5]:
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==2 and l[0]+l[1]=='B_AC_A' else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [6]:
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==5 and l[0]+l[1]+l[2]+l[3]+l[4]=='B_AC_AG_FD_BE_B' else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [7]:
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==4 and [[0,1],[0,2],[1,2]] in l and [[0,4],[0,5],[1,5]] in l and [[0,6],[0,7],[1,7]] in l and [[0,10],[0,11],[1,11]] else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [8]:
                verify_list = [[[1, 0], [2, 0], [3, 0], [3, 1]], [[0, 1], [1, 1], [2, 1], [2, 2]], [[3, 2], [4, 2], [5, 2], [5, 3]], [[2, 3], [3, 3], [4, 3], [4, 4]], [[0, 4], [1, 4], [2, 4], [2, 5]]]
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==5 and verify_list[0] in l  and verify_list[1] in l  and verify_list[2] in l  and verify_list[3] in l  and verify_list[4] in l else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [9]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row,'list']
                    if list_temp!=None and len(list_temp)==2:
                        if list_temp[0][0:2] > list_temp[0][-2:]:
                            list_temp[0] = list_temp[0][-2:] + '_' + list_temp[0][0:2]
                        if list_temp[1][0:2] > list_temp[1][-2:]:
                            list_temp[1] = list_temp[1][-2:] + '_' + list_temp[1][0:2]
                        if list_temp[0] > list_temp[1]:
                            additional_infor_df._set_value(row,'list', str([list_temp[1], list_temp[0]]))
                        else:
                            additional_infor_df._set_value(row,'list', str(list_temp))
                    else:
                        additional_infor_df._set_value(row,'list', str(list_temp))
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[ast.literal_eval(index) for index in grouped.index]})
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_list = [['02_09', '05_06'],['02_05', '06_09'],['02_06', '05_09']]
                    

                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==2 and l in verify_list else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [10]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                
                    if list_temp!=None:
                        list_temp = [[int(rebuild_i) for rebuild_i in re.findall(r"\d+", rebuild)] for rebuild in list_temp]
                        for list_mem in list_temp:
                            list_mem.sort()
                        list_temp.sort()
                        additional_infor_df._set_value(row,'list', str([str(list_str[0]) + '_' + str(list_str[1]) for list_str in list_temp]))
                    else:
                        additional_infor_df._set_value(row,'list', str(list_temp))
                
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[ast.literal_eval(index) for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))

                verify_list = ['2','6','12','14','15','16']
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l!= None and len(l)==3 and len(set([re.findall(r"\d+",l[0])[0], re.findall(r"\d+",l[0])[1], re.findall(r"\d+",l[1])[0], re.findall(r"\d+",l[1])[1], re.findall(r"\d+",l[2])[0],re.findall(r"\d+",l[2])[1]]))==6 and re.findall(r"\d+",l[0])[0] in verify_list and re.findall(r"\d+",l[0])[1] in verify_list and re.findall(r"\d+",l[1])[0] in verify_list and re.findall(r"\d+",l[1])[1] in verify_list and re.findall(r"\d+",l[2])[0] in verify_list and re.findall(r"\d+",l[2])[1] in verify_list else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [11]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '0012210224'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [12]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '2213110425'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [13]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '21'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [14]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '121223'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [18]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_list = ['0', '2']
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if len(l)==3 and l[0] in verify_list and l[1] in verify_list and l[2] in verify_list else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [19]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '000000'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l.replace('2','0')==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [21]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', "".join(re.findall(r"\d+", str(list_temp))))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '1010011001'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [22]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', str(list_temp))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_list = ['[[0, 0, 1, 1, 0, 1, 0], [[1, 0], [0]]]','[[1, 1, 0, 0, 1, 0, 1], [[0], [1, 0]]]']
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l in verify_list else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            elif i in [15]:
                for row in range(len(additional_infor_df)):
                    list_temp = additional_infor_df.loc[row, 'list']
                    if list_temp!=None:
                        additional_infor_df._set_value(row,'list', str(list_temp))
                    else:
                        additional_infor_df._set_value(row,'list', '')
                grouped = additional_infor_df.groupby('list')['count'].sum()
                additional_infor_df = pd.DataFrame({'list':[index for index in grouped.index]})        
                additional_infor_df.insert(len(additional_infor_df.columns), 'count', list( grouped.iloc[:]))
                verify_str = '[[1, 0, 1, 2], 1, 16, True]'
                additional_infor_df.insert(len(additional_infor_df.columns), 'success', ['1' if l==verify_str else '0' for l in additional_infor_df.iloc[:,0] ])
                accuracy_list.append(additional_infor_df.groupby('success')['count'].sum().iloc[1]/self.row_num)
            addition_list.append(additional_infor_df)
        pro_name_list = ['小松鼠跳柱子（1）', '小松鼠跳柱子（2）', '填充小石子（1）', '填充小石子（2）','嵌套的矩形（1）', '嵌套的矩形（2）','模式的复制（1）','模式的复制（2）','浇花（1）','浇花（2）','密码（1）','密码（2）','4进制编码（1）','4进制编码（2）','滚筒（1）','供水系统（1）','供水系统（2）','对应的形状（1）','对应的形状（2）']
        
        return addition_list, pd.DataFrame({'problem_num':pro_name_list, 'accuracy': accuracy_list}),pro_name_list

    def count_group(self):
        count_df_list = []
        for group in self.group_list:
            count_df_list.append(group.count())

        return count_df_list

    def plot(self):
        data = [go.Histogram(x=list(self.df.loc[:,'interval']))] 
        layout={"title": "学生用时分布", 
                                       "xaxis_title": "学生用时，单位秒",
                                       "yaxis_title": "学生个数",
                                       # x轴坐标倾斜60度
                                       "xaxis": {"tickangle": 60}
                                      }
        fig = go.Figure(data=data,layout=layout)
        plot(fig,filename="./plot/"+self.name+"/time.html",auto_open=False,image='png',image_height=800,image_width=1500)
        # offline.iplot(fig) 
        return 0

    def plot_problem(self):
        data = [go.Bar(x = list(range(self.problem_num)), y = [len(list(group)) for group in self.group_list])] 
        layout={"title": "不同题目的编码数量", 
                                       "xaxis_title": "题目编号",
                                       "yaxis_title": "编码个数",
                                       # x轴坐标倾斜60度
                                       "xaxis": {"tickangle": 60}
                                      }
        fig = go.Figure(data=data,layout=layout)
        plot(fig,filename="./plot/"+self.name+"/plot_problem.html",auto_open=False,image='png',image_height=800,image_width=1500)
        # offline.iplot(fig) 
        return 0
    
    def output(self):
        # self.plot()
        # self.plot_problem()
        for i, df in enumerate(self.ndf_list):
            df.iloc[:, 1].to_excel('./output/' + str(self.name)+'/' +str(i) + '.xlsx')
        for i, df in enumerate(self.addition_list):
            df.to_excel('./output/' + str(self.name)+'/' +str(i) + '_count.xlsx')
    
if __name__ == '__main__':
    df = pd.read_excel('./data/data.xlsx')  
    df_junior = pd.read_excel('./data/junior.xlsx')  
    df_senior = pd.read_excel('./data/senior.xlsx') 
    data_entity = data_analysis(df)
    data_entity_junior = data_analysis(df = df_junior, name = 'junior')
    data_entity_senior = data_analysis(df = df_senior, name = 'senior')
