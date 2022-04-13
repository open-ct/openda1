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
# %%
# 同理求解滚筒（3）
posible_roll = traverse_roll(min_roll_length = 2, max_roll_length = 5, colors = [0,1,2], start_bound = 0, end_bound = 19)
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
# %%
# 根据所有可能的roll3寻找roll2
posible_roll2_roll3 = []
cnt = 0
for roll3 in posible_roll3_list:
    print(cnt)
    cnt += 1
    flag_list = [-1]*len(verify_list)
    for index3 in range(roll3['start'], roll3['end']+1):
        flag_list[index2] = '3'
    for roll2 in posible_roll:
        flag_list_ = [i for i in flag_list]

        roll2_is_posible = True

        # if roll2['start']>=roll3['start'] and roll2['end']<=roll3['end']:
        #     roll2_is_posible = False
        #     continue

        for index2 in range(roll2['start'], roll2['end']+1):
            if flag_list_[index1] == -1 and roll2['color_list'][((index-roll2['start']) % len(roll2['color_list']))] != verify_list[index]:
                roll2_is_posible = False
                break

        if roll2_is_posible:
            posible_roll2_roll3.append((roll2, roll3))
# %%
len(posible_roll2_roll3)
# %%
posible_roll2_roll3[0]
# %%
