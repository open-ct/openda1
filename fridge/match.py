from numpy.lib.function_base import average
import pandas as pd

df = pd.read_csv('./newResult0930.csv', index_col=0)
# df = pd.read_csv('./newResult.csv', index_col=0)

# df = df.dropna()
df['final_type'] = '0'

for index in df.index:
    if df.loc[index, 'code'] in [31, 32]:
        df.loc[index, 'final_type'] = 1
    elif df.loc[index, 'code'] in [21, 22, 23, 24, 33, 34]:
        df.loc[index, 'final_type'] = 2
    elif df.loc[index, 'code'] in [11, 12, 13, 14]:
        df.loc[index, 'final_type'] = 3
    else:
        df.loc[index, 'final_type'] = 4
# df.to_csv('test_r.csv')
# print(df)


res_total_level = [[0 for i in range(4)] for i in range(4)]
res_INQUIRY_level = [[0 for i in range(4)] for i in range(4)]

total_score = [[] for i in range(4)]
INQUIRY_score = [[] for i in range(4)]

for index in df.index:
    res_total_level[int(df.loc[index, 'total_level'] - 1)
                    ][df.loc[index, 'final_type'] - 1] += 1
    res_INQUIRY_level[int(df.loc[index, 'INQUIRY_level'] - 1)
                      ][df.loc[index, 'final_type'] - 1] += 1
    total_score[df.loc[index, 'final_type'] -
                1].append(df.loc[index, 'total_score'])
    INQUIRY_score[df.loc[index, 'final_type'] -
                  1].append(df.loc[index, 'INQUIRY_score'])
    # print(df.loc[index])
    # print(res_total_level)
    # print(res_INQUIRY_level)
    # print(total_score)
    # print(INQUIRY_score)

print("res_total_level")
for i in res_total_level:
    print(i, sum(i))
    for j in i:
        print(j/sum(i))

print("res_INQUIRY_level")
for i in res_INQUIRY_level:
    print(i, sum(i))
    for j in i:
        print(j/sum(i))

print("total_score")
for i in total_score:
    print(average(i))

print("INQUIRY_score")
for i in INQUIRY_score:
    print(average(i))
