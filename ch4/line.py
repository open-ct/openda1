from math import exp
from numpy.lib.function_base import average
import pandas as pd
import matplotlib.pyplot as plt

total = []
time = []


df = pd.read_csv('./413737.csv')
df = df.loc[round(len(df)*0.025):round(len(df)*0.975)]
min1 = min(df['duration'])
print(min1)
print(max(df['duration']))
gap = (max(df['duration'])+1 - min(df['duration'])) / 20
total = [[] for _ in range(20)]

print(gap)
for index in df.index:
    # print(round((df.loc[index, 'duration'] - min1) / gap))
    total[round((df.loc[index, 'duration'] - min1) //
                gap)].append(df.loc[index, 'TOTAL_CH4_RATE'])
# time.append(df.loc[index, 'duration'])

lin1 = []
for i in total:
    lin1.append(average(i))
    print(average(i))


# plt.figure(figsize=(100, 60))
aa = range(round(min1), round(max(df['duration'])), round(gap))
for a in aa:
    print(a)
plt.plot(aa, lin1, color='red',
         label='label1', linewidth=3.0)  # 画第2条折线
plt.savefig('./test3.jpg')
# plt.show()
