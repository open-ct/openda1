import numpy
import pandas as pd

df = pd.DataFrame(pd.read_csv('./413737.csv'))

df = df.loc[round(len(df)*0.025):round(len(df)*0.975)]

total = [[] for _ in range(4)]
inquiry = [[] for _ in range(4)]
resoning = [[] for _ in range(4)]
explan = [[] for _ in range(4)]

for index in df.index:
    total[int(df.loc[index, 'total_level'] - 1)
          ].append(df.loc[index, 'duration'])
    inquiry[int(df.loc[index, 'INQUIRY_level'] - 1)
            ].append(df.loc[index, 'duration'])
    resoning[int(df.loc[index, 'REASONING_level'] - 1)
             ].append(df.loc[index, 'duration'])
    explan[int(df.loc[index, 'EXPLANATION_level'] - 1)
           ].append(df.loc[index, 'duration'])

print(total[0])
print("total")
for i in total:
    print(numpy.average(i), numpy.std(i))
print("INQUIRY")
for i in inquiry:
    print(numpy.average(i), numpy.std(i))
print("rea")
for i in resoning:
    print(numpy.average(i), numpy.std(i))
print("explan")
for i in explan:
    print(numpy.average(i), numpy.std(i))
