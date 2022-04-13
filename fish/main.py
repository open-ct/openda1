import pandas as pd
import csv


df = pd.DataFrame(pd.read_csv('./test.csv', index_col=0))

df = df[:-2]
df['time'] = pd.to_datetime(df.time)
df = df.sort_values(by='time', ignore_index=True)

df3 = df[df['task_answers'].str.contains('"page":3', na=False)]
df6 = df[df['task_answers'].str.contains('"page":7', na=False)]

df3.to_csv('page3.csv')
df6.to_csv('page7.csv')

with open('page3.csv', 'r', encoding='UTF-8') as f:
    with open('reducePage3.csv', 'w', newline='', encoding='UTF-8') as f1:
        f1_csv = csv.writer(f1)
        f1_csv.writerow(['id', 'time', 'ticket_id', 'task_answers'])
        f_csv = csv.reader(f)
        next(f_csv, None)
        for index, row in enumerate(f_csv):
            try:
                if 'demo' in row[2]:
                    continue
                ans = (eval(row[3])['frame']['answer'][5:7])
                if ans == [[1], [1]]:
                    continue
                if [-1] in ans:
                    continue
                row[3] = [ans[0][0], ans[1][0]]
                f1_csv.writerow(row)
            except:
                continue
with open('page7.csv', 'r', encoding='UTF-8') as f:
    with open('reducePage7.csv', 'w', newline='', encoding='UTF-8') as f1:
        f1_csv = csv.writer(f1)
        f1_csv.writerow(['id', 'time', 'ticket_id', 'task_answers'])
        f_csv = csv.reader(f)
        next(f_csv, None)
        for index, row in enumerate(f_csv):
            try:
                if 'demo' in row[2]:
                    continue
                ans = (eval(row[3])['frame']['answer'][12:15])
                if [-1] in ans:
                    continue
                row[3] = [ans[0][0], ans[1][0], ans[2][0]]
                f1_csv.writerow(row)
            except:
                continue


def join(x):
    res = []
    for index in x.index:
        res.append(x.loc[index, 'task_answers'])
    return res


df = pd.DataFrame(pd.read_csv('./reducePage3.csv', index_col=0))
df = df.groupby('ticket_id').apply(join)

df.to_csv("joinPage3.csv")

df = pd.DataFrame(pd.read_csv('./reducePage7.csv', index_col=0))
df = df.groupby('ticket_id').apply(join)

df.to_csv("joinPage7.csv")
