import pandas as pd

table = pd.read_csv('sort.csv', index_col=0)

table['time'] = pd.to_datetime(table['time'])
# table = table.sort_values(['STU_CODE', 'time'])
# table.to_csv('sort.csv')
res_table = pd.DataFrame(columns=[
    'stu_code',
    'Q1_PLAN',
    'Q2_PLAN',
    'Q1_A_PLAN',
    'Q2_A_PLAN',
    'Q1_A_PLAN_T',
    'Q2_A_PLAN_T',
    'Q1_B_1',
    'Q1_B_2',
    'Q1_B_3',
    'Q1_B_4',
    'Q1_B_5',
    'Q1_B_6',
    'Q2_B_1',
    'Q2_B_2',
    'Q2_B_3',
    'Q2_B_4',
    'Q2_B_5',
    'Q2_B_6',
    'Q1_B_PLAN',
    'Q2_B_PLAN',
    'Q1_C_1',
    'Q1_C_2',
    'Q1_C_3',
    'Q1_C_4',
    'Q1_C_5',
    'Q1_C_6',
    'Q1_C_7',
    'Q1_C_8',
    'Q2_C_1',
    'Q2_C_2',
    'Q2_C_3',
    'Q2_C_4',
    'Q2_C_5',
    'Q2_C_6',
    'Q2_C_7',
    'Q2_C_8',
    'Q1_C_PLAN',
    'Q2_C_PLAN',
    'Q0_T',
    'QI_T',
    'Q2_T',
    'TIME'
])


def join(x):
    Q1_PLAN = -1
    Q2_PLAN = -1
    Q1_A_PLAN = -1
    Q2_A_PLAN = -1
    Q1_A_PLAN_T = -1
    Q2_A_PLAN_T = -1
    Q1_B_1 = -1
    Q1_B_2 = -1
    Q1_B_3 = -1
    Q1_B_4 = -1
    Q1_B_5 = -1
    Q1_B_6 = -1
    Q2_B_1 = -1
    Q2_B_2 = -1
    Q2_B_3 = -1
    Q2_B_4 = -1
    Q2_B_5 = -1
    Q2_B_6 = -1
    Q1_B_PLAN = -1
    Q2_B_PLAN = -1
    Q1_C_1 = -1
    Q1_C_2 = -1
    Q1_C_3 = -1
    Q1_C_4 = -1
    Q1_C_5 = -1
    Q1_C_6 = -1
    Q1_C_7 = -1
    Q1_C_8 = -1
    Q2_C_1 = -1
    Q2_C_2 = -1
    Q2_C_3 = -1
    Q2_C_4 = -1
    Q2_C_5 = -1
    Q2_C_6 = -1
    Q2_C_7 = -1
    Q2_C_8 = -1
    Q1_C_PLAN = -1
    Q2_C_PLAN = -1
    Q0_T = -1
    Q1_T = -1
    Q2_T = -1
    TIME = -1

    modifyQ1 = [0 for _ in range(9)]
    modifyQ2 = [0 for _ in range(9)]

    modifyingQ1_4 = False
    modifyingQ1_5 = False
    modifyingQ2_4_1 = False
    modifyingQ2_4_2 = False
    modifyingQ2_5 = False
    modifyingQ2_6 = False
    modifyingQ2_7 = False

    Q1PLAN = None
    Q2PLAN = None

    startQ0 = False
    startQ0_t = 0

    startQ1 = False
    startQ1_1 = False
    startQ1_7 = False
    startQ1_t = 0

    startQ2 = False
    startQ2_1 = False
    startQ2_7 = False
    startQ2_t = 0

    lastI = 0
    lastFrame = []
    lastTemp = {'data': {'frame': None}}
    global res_table
    global count

    last_index = x.index[-1]
    dday = x.loc[last_index, 'time']

    for i in reversed(x.index):
        if 'True' in x.loc[i, 'data']:
            dday = x.loc[i, 'time'].day
            last_index = i
            break

    for index, i in enumerate(x.index):
        cday = x.loc[i, 'time'].day
        if dday != cday:
            continue
        temp = x.loc[i]
        if index > 0:
            lastTemp = x.loc[x.index[index - 1]]
        data = eval(temp['data'])['frame']
        lastFrame = eval(str(lastTemp['data']))['frame']
        # print(temp)
        if startQ0 == False and temp['num'] == 1:
            startQ0 = True
            startQ0_t = temp['time']
            continue

        if startQ1 == False and temp['num'] == 2:
            startQ1 = True
            startQ1_t = temp['time']
            Q0_T = pd.Timedelta(pd.to_datetime(
                x.loc[x.index[index - 1], 'time']) - pd.to_datetime(startQ0_t)).seconds
            continue

        if lastFrame != None and type(lastFrame['data']) == list and temp['num'] == 2:
            if data != None:
                Q1PLAN = data['data'][0]
            for ii in range(4):
                if data != None and lastFrame['data'][0][ii] != -1 and data['data'][0][ii] != lastFrame['data'][0][ii]:
                    modifyQ1[0] += 1

            if data != None:
                if lastFrame['data'][1] != '-1' and data['data'][1] != lastFrame['data'][1]:
                    modifyQ1[1] += 1

                if len(lastFrame['data'][2]) != 0 and data['data'][2] != lastFrame['data'][2]:
                    modifyQ1[2] += 1

                if lastFrame['data'][3] != '-1' and data['data'][3] != lastFrame['data'][3]:
                    modifyQ1[3] += 1

                if lastFrame['data'][4] != '':
                    if modifyingQ1_4 == False:
                        if data['data'][4] != lastFrame['data'][4]:
                            modifyingQ1_4 = True
                            modifyQ1[4] += 1
                    else:
                        if data['data'][4] == lastFrame['data'][4]:
                            modifyingQ1_4 = False

                if lastFrame['data'][5] != '':
                    if modifyingQ1_5 == False:
                        if data['data'][5] != lastFrame['data'][5]:
                            modifyingQ1_5 = True
                            modifyQ1[5] += 1
                    else:
                        if data['data'][5] == lastFrame['data'][5]:
                            modifyingQ1_5 = False

                if lastFrame['data'][6] != '-1' and data['data'][6] != lastFrame['data'][6]:
                    modifyQ1[6] += 1

                if lastFrame['data'][7] != '-1' and data['data'][7] != lastFrame['data'][7]:
                    modifyQ1[7] += 1

                if lastFrame['data'][8] != '-1' and data['data'][8] != lastFrame['data'][8]:
                    modifyQ1[7] += 1

                if lastFrame['data'][9] != '-1' and data['data'][9] != lastFrame['data'][9]:
                    modifyQ1[8] += 1
                if lastFrame['data'][10] != '-1' and data['data'][10] != lastFrame['data'][10]:
                    modifyQ1[8] += 1
                if lastFrame['data'][11] != '-1' and data['data'][11] != lastFrame['data'][11]:
                    modifyQ1[8] += 1
                if lastFrame['data'][12] != '-1' and data['data'][12] != lastFrame['data'][12]:
                    modifyQ1[8] += 1

        if data != None and startQ1_1 == False and temp['num'] == 2 and data['data'][1] != '-1':
            startQ1_1 = True
            Q1_A_PLAN_T = pd.Timedelta(pd.to_datetime(
                x.loc[x.index[index - 1], 'time']) - startQ1_t).seconds
            Q1_A_PLAN = modifyQ1[0]
            continue

        if data != None and startQ1_7 == False and temp['num'] == 2 and data['data'][-6] != '-1':
            startQ1_7 = True
            Q1_B_1 = modifyQ1[1]
            Q1_B_2 = modifyQ1[2]
            Q1_B_3 = modifyQ1[3]
            Q1_B_4 = modifyQ1[4]
            Q1_B_5 = modifyQ1[5]
            Q1_B_6 = modifyQ1[6]
            Q1_B_PLAN = modifyQ1[0] - Q1_A_PLAN
            continue

        if startQ2 == False and temp['num'] == 3:
            startQ2 = True
            startQ2_t = temp['time']
            Q1_T = pd.Timedelta(pd.to_datetime(
                x.loc[x.index[index - 1], 'time']) - pd.to_datetime(startQ1_t)).seconds
            if Q1PLAN != None:
                # Q1PLAN = lastFrame['data'][0]
                Q1ANS = [1, 3, 0, 2]
                count = 0
                for i in range(4):
                    if Q1ANS[i] == Q1PLAN[i]:
                        count += 1
                if Q1PLAN == [-1, -1, -1, -1]:
                    Q1_PLAN = 99
                elif count == 2:
                    Q1_PLAN = 10
                elif count == 3:
                    Q1_PLAN = 20
                elif count == 4:
                    Q1_PLAN = 40
                else:
                    Q1_PLAN = 70

            Q1_C_1 = modifyQ1[1] - Q1_B_1
            Q1_C_2 = modifyQ1[2] - Q1_B_2
            Q1_C_3 = modifyQ1[3] - Q1_B_3
            Q1_C_4 = modifyQ1[4] - Q1_B_4
            Q1_C_5 = modifyQ1[5] - Q1_B_5
            Q1_C_6 = modifyQ1[6] - Q1_B_6
            Q1_C_7 = modifyQ1[7]
            Q1_C_8 = modifyQ1[8]
            Q1_C_PLAN = modifyQ1[0] - Q1_B_PLAN - Q1_A_PLAN

            continue

        if data != None and lastFrame != None and temp['num'] == 3:
            Q2PLAN = data['data'][0]
            for ii in range(4):
                if lastFrame['data'][0][ii] != -1 and data['data'][0][ii] != lastFrame['data'][0][ii]:
                    modifyQ2[0] += 1

            if len(lastFrame['data'][1]) != 0 and data['data'][1] != lastFrame['data'][1]:
                modifyQ2[1] += 1

            if len(lastFrame['data'][2]) != 0 and data['data'][2] != lastFrame['data'][2]:
                modifyQ2[2] += 1

            if lastFrame['data'][3] != '-1' and data['data'][3] != lastFrame['data'][3]:
                modifyQ2[3] += 1

            if lastFrame['data'][4] != '':
                if modifyingQ2_4_1 == False:
                    if data['data'][4] != lastFrame['data'][4]:
                        modifyingQ2_4_1 = True
                        modifyQ2[4] += 1
                else:
                    if data['data'][4] == lastFrame['data'][4]:
                        modifyingQ2_4_1 = False

            if lastFrame['data'][5] != '':
                if modifyingQ2_4_2 == False:
                    if data['data'][5] != lastFrame['data'][5]:
                        if x.name == 11010702104031:
                            print(data['data'][5])
                        modifyingQ2_4_2 = True
                        modifyQ2[4] += 1
                else:
                    if data['data'][5] == lastFrame['data'][5]:
                        modifyingQ2_4_2 = False

            if lastFrame['data'][6] != '':
                if modifyingQ2_5 == False:
                    if data['data'][6] != lastFrame['data'][6]:
                        modifyingQ2_5 = True
                        modifyQ2[5] += 1
                else:
                    if data['data'][6] == lastFrame['data'][6]:
                        modifyingQ2_5 = False

            if lastFrame['data'][8] != '':
                if modifyingQ2_6 == False:
                    if data['data'][8] != lastFrame['data'][8]:
                        modifyingQ2_6 = True
                        modifyQ2[6] += 1
                else:
                    if data['data'][8] == lastFrame['data'][8]:
                        modifyingQ2_6 = False

            if lastFrame['data'][10] != '' and data['data'][10] != lastFrame['data'][10]:
                modifyQ2[7] += 1

            if lastFrame['data'][11] != '':
                if modifyingQ2_7 == False:
                    if data['data'][11] != lastFrame['data'][11]:
                        modifyingQ2_7 = True
                        modifyQ2[7] += 1
                else:
                    if data['data'][11] == lastFrame['data'][11]:
                        modifyingQ2_7 = False

            if lastFrame['data'][12] != '-1' and data['data'][12] != lastFrame['data'][12]:
                modifyQ2[8] += 1

        if data != None and startQ2_1 == False and temp['num'] == 3 and len(data['data'][1]) != 0:
            startQ2_1 = True
            Q2_A_PLAN_T = pd.Timedelta(pd.to_datetime(
                x.loc[x.index[index-1], 'time']) - startQ2_t).seconds
            Q2_A_PLAN = modifyQ2[0]
            continue

        if data != None and startQ2_7 == False and temp['num'] == 3 and data['data'][-3] != '':
            startQ2_7 = True
            Q2_B_1 = modifyQ2[1]
            Q2_B_2 = modifyQ2[2]
            Q2_B_3 = modifyQ2[3]
            Q2_B_4 = modifyQ2[4]
            Q2_B_5 = modifyQ2[5]
            Q2_B_6 = modifyQ2[6]
            Q2_B_PLAN = modifyQ2[0] - Q2_A_PLAN
            continue

        if i == last_index and temp['num'] == 3:
            if Q2PLAN != None:
                # Q2PLAN = data['data'][0]
                Q2ANS = [1, 3, 0, 2]
                count = 0
                for i in range(4):
                    if Q2ANS[i] == Q2PLAN[i]:
                        count += 1
                if Q2PLAN == [-1, -1, -1, -1]:
                    Q2_PLAN = 99
                elif count == 2:
                    Q2_PLAN = 10
                elif count == 3:
                    Q2_PLAN = 20
                elif count == 4:
                    Q2_PLAN = 40
                else:
                    Q2_PLAN = 70

            Q2_C_1 = modifyQ2[1] - Q2_B_1
            Q2_C_2 = modifyQ2[2] - Q2_B_2
            Q2_C_3 = modifyQ2[3] - Q2_B_3
            Q2_C_4 = modifyQ2[4] - Q2_B_4
            Q2_C_5 = modifyQ2[5] - Q2_B_5
            Q2_C_6 = modifyQ2[6] - Q2_B_6
            Q2_C_7 = modifyQ2[7]
            Q2_C_8 = modifyQ2[8]
            Q2_C_PLAN = modifyQ2[0] - Q2_B_PLAN - Q2_A_PLAN

            Q2_T = pd.Timedelta(pd.to_datetime(
                temp['time']) - pd.to_datetime(startQ2_t)).seconds
        if i == last_index:
            break

    dict = {
        'stu_code': table.loc[x.index[0], 'STU_CODE'],
        'Q1_PLAN': Q1_PLAN,
        'Q2_PLAN': Q2_PLAN,
        'Q1_A_PLAN': Q1_A_PLAN,
        'Q2_A_PLAN': Q2_A_PLAN,
        'Q1_A_PLAN_T': Q1_A_PLAN_T,
        'Q2_A_PLAN_T': Q2_A_PLAN_T,
        'Q1_B_1': Q1_B_1,
        'Q1_B_2': Q1_B_2,
        'Q1_B_3': Q1_B_3,
        'Q1_B_4': Q1_B_4,
        'Q1_B_5': Q1_B_5,
        'Q1_B_6': Q1_B_6,
        'Q2_B_1': Q2_B_1,
        'Q2_B_2': Q2_B_2,
        'Q2_B_3': Q2_B_3,
        'Q2_B_4': Q2_B_4,
        'Q2_B_5': Q2_B_5,
        'Q2_B_6': Q2_B_6,
        'Q1_B_PLAN': Q1_B_PLAN,
        'Q2_B_PLAN': Q2_B_PLAN,
        'Q1_C_1': Q1_C_1,
        'Q1_C_2': Q1_C_2,
        'Q1_C_3': Q1_C_3,
        'Q1_C_4': Q1_C_4,
        'Q1_C_5': Q1_C_5,
        'Q1_C_6': Q1_C_6,
        'Q1_C_7': Q1_C_7,
        'Q1_C_8': Q1_C_8,
        'Q2_C_1': Q2_C_1,
        'Q2_C_2': Q2_C_2,
        'Q2_C_3': Q2_C_3,
        'Q2_C_4': Q2_C_4,
        'Q2_C_5': Q2_C_5,
        'Q2_C_6': Q2_C_6,
        'Q2_C_7': Q2_C_7,
        'Q2_C_8': Q2_C_8,
        'Q1_C_PLAN': Q1_C_PLAN,
        'Q2_C_PLAN': Q2_C_PLAN,
        'Q0_T': Q0_T,
        'QI_T': Q1_T,
        'Q2_T': Q2_T,
        'TIME': Q0_T + Q1_T + Q2_T
    }

    res_table = pd.concat([res_table, pd.DataFrame([dict])], ignore_index=True)


table.groupby('STU_CODE').apply(join)
res_table.to_csv('res.csv')
print(res_table)

# print(table)
