import numpy
import pandas as pd

df = pd.read_csv('./413737.csv')

# df = df.loc[round(len(df)*0.025):round(len(df)*0.975)]

total = [[] for _ in range(4)]


for index in df.index:
    total[int(df.loc[index, 'total_level'] - 1)
          ].append(df.loc[index, 'duration'])

print("total")
for i in total:
    i.sort()
    i = i[round(len(i)*0.025):round(len(i)*0.975)]
    print(numpy.average(i), numpy.std(i))
