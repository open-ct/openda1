import pandas as pd

S1MAXPAGE = 3
S2MAXPAGE = 12
S3MAXPAGE = 12
S4MAXPAGE = 9
S5MAXPAGE = 2

table = pd.read_csv('filter2.csv', index_col=0)
indexList = list(set(list(table['id'])))

res_table = pd.DataFrame(index=indexList, columns=[
    'S1RETU',
    'S2RETU',
    'S3RETU',
    'S4RETU',
    'S5RETU',
    'S1RETU_1',
    'S1RETU_2',
    'S1RETU_3',
    'S2RETU_1',
    'S2RETU_2',
    'S2RETU_3',
    'S2RETU_4',
    'S2RETU_5',
    'S2RETU_6',
    'S2RETU_7',
    'S2RETU_8',
    'S2RETU_9',
    'S2RETU_10',
    'S2RETU_11',
    'S2RETU_12',
    'S3RETU_1',
    'S3RETU_2',
    'S3RETU_3',
    'S3RETU_4',
    'S3RETU_5',
    'S3RETU_6',
    'S3RETU_7',
    'S3RETU_8',
    'S3RETU_9',
    'S3RETU_10',
    'S3RETU_11',
    'S3RETU_12',
    'S4RETU_1',
    'S4RETU_2',
    'S4RETU_3',
    'S4RETU_4',
    'S4RETU_5',
    'S4RETU_6',
    'S4RETU_7',
    'S4RETU_8',
    'S4RETU_9',
    'S5RETU_1',
    'S5RETU_2',
    'S1RS_1',
    'S1RS_2',
    'S1RS_3',
    'S2RS_1',
    'S2RS_2',
    'S2RS_3',
    'S2RS_4',
    'S2RS_5',
    'S2RS_6',
    'S2RS_7',
    'S2RS_8',
    'S2RS_9',
    'S2RS_10',
    'S2RS_11',
    'S2RS_12',
    'S3RS_1',
    'S3RS_2',
    'S3RS_3',
    'S3RS_4',
    'S3RS_5',
    'S3RS_6',
    'S3RS_7',
    'S3RS_8',
    'S3RS_9',
    'S3RS_10',
    'S3RS_11',
    'S3RS_12',
    'S4RS_1',
    'S4RS_2',
    'S4RS_3',
    'S4RS_4',
    'S4RS_5',
    'S4RS_6',
    'S4RS_7',
    'S4RS_8',
    'S4RS_9',
    'S5RS_1',
    'S5RS_2',
    'S1RO',
    'S2RO',
    'S3RO',
    'S4RO',
    'S5RO',
    'S1ROS',
    'S2ROS',
    'S3ROS',
    'S4ROS',
    'S5ROS',
    'S11ST',
    'S12ST',
    'S21ST',
    'S22ST',
    'S23ST',
    'S24ST',
    'S31ST',
    'S41ST',
    'S42ST',
    'S51ST',
    'S52ST',
    'S53ST',
    'S54ST',
    'S55ST',
    'OR',
    'ORM',
    'S1STT',
    'S2STT',
    'S3STT',
    'S4STT',
    'S5STT',

    'S1STT_1',
    'S1STT_2',
    'S1STT_3',
    'S2STT_1',
    'S2STT_2',
    'S2STT_3',
    'S2STT_4',
    'S2STT_5',
    'S2STT_6',
    'S2STT_7',
    'S2STT_8',
    'S2STT_9',
    'S2STT_10',
    'S2STT_11',
    'S2STT_12',
    'S3STT_1',
    'S3STT_2',
    'S3STT_3',
    'S3STT_4',
    'S3STT_5',
    'S3STT_6',
    'S3STT_7',
    'S3STT_8',
    'S3STT_9',
    'S3STT_10',
    'S3STT_11',
    'S3STT_12',
    'S4STT_1',
    'S4STT_2',
    'S4STT_3',
    'S4STT_4',
    'S4STT_5',
    'S4STT_6',
    'S4STT_7',
    'S4STT_8',
    'S4STT_9',
    'S5STT_1',
    'S5STT_2',
    'S1READ',
    'S2READ',
    'S3READ',
    'S4READ',
    'S5READ',
    'S1START',
    'S2START',
    'S3START',
    'S4START',
    'S5START',

    'S11ANS',
    'S12ANS',
    'S21ANS',
    'S22ANS',
    'S23ANS',
    'S24ANS',
    'S31ANS',
    'S41ANS',
    'S42ANS',
    'S51ANS',
    'S52ANS',
    'S53ANS',
    'S54ANS',
    'S55ANS',
    'S1Draft',
    'S2Draft',
    'S3Draft',
    'S4Draft',
    'S5Draft',
])

MAXPAGES = [S1MAXPAGE, S2MAXPAGE, S3MAXPAGE, S4MAXPAGE, S5MAXPAGE]

MAXANS = [2, 4, 1, 2, 5]


def join2(item):
    ans = [[] for i in range(5)]
    flag = [False for i in range(5)]
    allTrue = [True for i in range(5)]
    OR = 0
    ORM = 0
    for index, i in enumerate(item.index):
        if index == 0:
            continue
        if item.loc[i, 'qcode'] != item.loc[item.index[index - 1], 'qcode']:
            ans[item.loc[item.index[index-1], 'qcode'] -
                1] = eval(item.loc[item.index[index - 1], 'data'])['basic']
            flag[item.loc[item.index[index-1], 'qcode'] - 1] = True
        if flag == allTrue:
            OR = 1
        if OR == 1 and eval(item.loc[i, 'data'])['basic'] != ans[item.loc[i, 'qcode'] - 1]:
            ORM = 1
    res_table.loc[item.name, 'OR'] = OR
    res_table.loc[item.name, 'ORM'] = ORM


def join(item):
    try:
        maxpage = MAXPAGES[item.name[1] - 1]
        maxans = MAXANS[item.name[1] - 1]
        returPageTimes = [0 for i in range(maxpage)]
        returPageStay = [0.0 for i in range(maxpage)]
        ansTime = [0.0 for i in range(MAXANS[item.name[1] - 1])]
        STT = [0.0 for i in range(maxpage)]
        ansRETU = [set({}) for i in range(MAXANS[item.name[1] - 1])]
        finishReading = False
        startAns = False
        start = 0
        ReadingTime = 0.0
        ST = set({})
        RO = 0
        RETU = 0
        ROS = 0
        startIndex = -1
        draftRate = 0.0
        # print(item.loc[item.index[-1], 'time'])
        lastDate = pd.to_datetime(item.loc[item.index[-1], 'time']).day
        for index, i in enumerate(item.index):
            row = item.loc[i]
            if pd.to_datetime(row['time']).day != lastDate:
                continue
            else:
                if startIndex == -1:
                    startIndex = index
                    TT = pd.Timedelta(pd.to_datetime(
                        item.loc[item.index[-1], 'time']) - pd.to_datetime(item.loc[item.index[startIndex], 'time'])).microseconds / 1e6
            data = eval(item.loc[i, 'data'])
            if index > startIndex:
                STT[data['deck'] - 1] += pd.Timedelta(pd.to_datetime(
                    row['time']) - pd.to_datetime(item.loc[item.index[index - 1], 'time'])).microseconds / 1e6
            if index > startIndex and data['basic'] != eval(item.loc[item.index[index - 1], 'data'])['basic']:
                tempBasic = data['basic']
                lastBasic = eval(
                    item.loc[item.index[index - 1], 'data'])['basic']
                for ans in range(maxans):
                    if tempBasic[ans] != lastBasic[ans]:
                        ansTime[ans] += pd.Timedelta(pd.to_datetime(
                            row['time']) - pd.to_datetime(item.loc[item.index[index - 1], 'time'])).microseconds / 1e6
                        ansRETU[ans].add(
                            eval(item.loc[item.index[index - 1], 'data'])['deck'])
                        ST.add(
                            eval(item.loc[item.index[index - 1], 'data'])['deck'])
                        break
                startAns = True
                ReadingTime = pd.Timedelta(pd.to_datetime(
                    item.loc[item.index[index - 1], 'time']) - pd.to_datetime(item.loc[item.index[0], 'time'])).microseconds / 1e6
                if finishReading:
                    start = pd.Timedelta(pd.to_datetime(
                        row['time']) - pd.to_datetime(item.loc[item.index[index - 1], 'time'])).microseconds / 1e6
            if data['deck'] == maxpage:
                finishReading = True
            if finishReading:
                if data['deck'] != maxpage:
                    RETU = 1
                    returPageTimes[data['deck'] - 1] += 1
                    gap = pd.Timedelta(
                        pd.to_datetime(item.loc[i, 'time']) - pd.to_datetime(item.loc[item.index[index - 1], 'time'])).microseconds / 1e6
                    # if gap > 3:
                    returPageStay[data['deck'] - 1] += gap
                    if startAns:
                        ROS = 1
                    else:
                        RO = 1
            if i == item.index[-1] and item.name[1] != 3:
                draft = list(data['canvas']['input'][0])
                draftSet = set(draft)
                aans = set(list("".join(data['basic'])))
                uni = draftSet & aans
                if len(draft) == 0:
                    draftRate = 0
                else:
                    draftRate = len(uni) / len(draft)
        if item.name[1] == 1:
            res_table.loc[item.name[0], 'S1RETU'] = RETU
            res_table.loc[item.name[0], 'S1RETU_1'] = returPageTimes[0]
            res_table.loc[item.name[0], 'S1RETU_2'] = returPageTimes[1]
            res_table.loc[item.name[0], 'S1RETU_3'] = returPageTimes[2]
            res_table.loc[item.name[0], 'S1RS_1'] = returPageStay[0]
            res_table.loc[item.name[0], 'S1RS_2'] = returPageStay[1]
            res_table.loc[item.name[0], 'S1RS_3'] = returPageStay[2]
            res_table.loc[item.name[0], 'S1RO'] = RO
            res_table.loc[item.name[0], 'S1ROS'] = ROS
            res_table.loc[item.name[0], 'S11ST'] = ansRETU[0]
            res_table.loc[item.name[0], 'S12ST'] = ansRETU[1]
            res_table.loc[item.name[0], 'S1STT'] = TT
            res_table.loc[item.name[0], 'S1STT_1'] = STT[0]
            res_table.loc[item.name[0], 'S1STT_2'] = STT[1]
            res_table.loc[item.name[0], 'S1STT_3'] = STT[2]
            res_table.loc[item.name[0], 'S1READ'] = ReadingTime
            res_table.loc[item.name[0], 'S1START'] = start
            res_table.loc[item.name[0], 'S11ANS'] = ansTime[0]
            res_table.loc[item.name[0], 'S12ANS'] = ansTime[1]
            res_table.loc[item.name[0], 'S1Draft'] = draftRate
        elif item.name[1] == 2:
            res_table.loc[item.name[0], 'S2RETU'] = RETU
            res_table.loc[item.name[0], 'S2RETU_1'] = returPageTimes[0]
            res_table.loc[item.name[0], 'S2RETU_2'] = returPageTimes[1]
            res_table.loc[item.name[0], 'S2RETU_3'] = returPageTimes[2]
            res_table.loc[item.name[0], 'S2RETU_4'] = returPageTimes[3]
            res_table.loc[item.name[0], 'S2RETU_5'] = returPageTimes[4]
            res_table.loc[item.name[0], 'S2RETU_6'] = returPageTimes[5]
            res_table.loc[item.name[0], 'S2RETU_7'] = returPageTimes[6]
            res_table.loc[item.name[0], 'S2RETU_8'] = returPageTimes[7]
            res_table.loc[item.name[0], 'S2RETU_9'] = returPageTimes[8]
            res_table.loc[item.name[0], 'S2RETU_10'] = returPageTimes[9]
            res_table.loc[item.name[0], 'S2RETU_11'] = returPageTimes[10]
            res_table.loc[item.name[0], 'S2RETU_12'] = returPageTimes[11]
            res_table.loc[item.name[0], 'S2RS_1'] = returPageStay[0]
            res_table.loc[item.name[0], 'S2RS_2'] = returPageStay[1]
            res_table.loc[item.name[0], 'S2RS_3'] = returPageStay[2]
            res_table.loc[item.name[0], 'S2RS_4'] = returPageStay[3]
            res_table.loc[item.name[0], 'S2RS_5'] = returPageStay[4]
            res_table.loc[item.name[0], 'S2RS_6'] = returPageStay[5]
            res_table.loc[item.name[0], 'S2RS_7'] = returPageStay[6]
            res_table.loc[item.name[0], 'S2RS_8'] = returPageStay[7]
            res_table.loc[item.name[0], 'S2RS_9'] = returPageStay[8]
            res_table.loc[item.name[0], 'S2RS_10'] = returPageStay[9]
            res_table.loc[item.name[0], 'S2RS_11'] = returPageStay[10]
            res_table.loc[item.name[0], 'S2RS_12'] = returPageStay[11]
            res_table.loc[item.name[0], 'S2RO'] = RO
            res_table.loc[item.name[0], 'S2ROS'] = ROS
            res_table.loc[item.name[0], 'S21ST'] = ansRETU[0]
            res_table.loc[item.name[0], 'S22ST'] = ansRETU[1]
            res_table.loc[item.name[0], 'S23ST'] = ansRETU[2]
            res_table.loc[item.name[0], 'S24ST'] = ansRETU[3]
            res_table.loc[item.name[0], 'S2STT'] = TT
            res_table.loc[item.name[0], 'S2STT_1'] = STT[0]
            res_table.loc[item.name[0], 'S2STT_2'] = STT[1]
            res_table.loc[item.name[0], 'S2STT_3'] = STT[2]
            res_table.loc[item.name[0], 'S2STT_4'] = STT[3]
            res_table.loc[item.name[0], 'S2STT_5'] = STT[4]
            res_table.loc[item.name[0], 'S2STT_6'] = STT[5]
            res_table.loc[item.name[0], 'S2STT_7'] = STT[6]
            res_table.loc[item.name[0], 'S2STT_8'] = STT[7]
            res_table.loc[item.name[0], 'S2STT_9'] = STT[8]
            res_table.loc[item.name[0], 'S2STT_10'] = STT[9]
            res_table.loc[item.name[0], 'S2STT_11'] = STT[10]
            res_table.loc[item.name[0], 'S2STT_12'] = STT[11]
            res_table.loc[item.name[0], 'S2READ'] = ReadingTime
            res_table.loc[item.name[0], 'S2START'] = start
            res_table.loc[item.name[0], 'S21ANS'] = ansTime[0]
            res_table.loc[item.name[0], 'S22ANS'] = ansTime[1]
            res_table.loc[item.name[0], 'S23ANS'] = ansTime[2]
            res_table.loc[item.name[0], 'S24ANS'] = ansTime[3]
            res_table.loc[item.name[0], 'S2Draft'] = draftRate
        elif item.name[1] == 3:
            res_table.loc[item.name[0], 'S3RETU'] = RETU
            res_table.loc[item.name[0], 'S3RETU_1'] = returPageTimes[0]
            res_table.loc[item.name[0], 'S3RETU_2'] = returPageTimes[1]
            res_table.loc[item.name[0], 'S3RETU_3'] = returPageTimes[2]
            res_table.loc[item.name[0], 'S3RETU_4'] = returPageTimes[3]
            res_table.loc[item.name[0], 'S3RETU_5'] = returPageTimes[4]
            res_table.loc[item.name[0], 'S3RETU_6'] = returPageTimes[5]
            res_table.loc[item.name[0], 'S3RETU_7'] = returPageTimes[6]
            res_table.loc[item.name[0], 'S3RETU_8'] = returPageTimes[7]
            res_table.loc[item.name[0], 'S3RETU_9'] = returPageTimes[8]
            res_table.loc[item.name[0], 'S3RETU_10'] = returPageTimes[9]
            res_table.loc[item.name[0], 'S3RETU_11'] = returPageTimes[10]
            res_table.loc[item.name[0], 'S3RETU_12'] = returPageTimes[11]
            res_table.loc[item.name[0], 'S3RS_1'] = returPageStay[0]
            res_table.loc[item.name[0], 'S3RS_2'] = returPageStay[1]
            res_table.loc[item.name[0], 'S3RS_3'] = returPageStay[2]
            res_table.loc[item.name[0], 'S3RS_4'] = returPageStay[3]
            res_table.loc[item.name[0], 'S3RS_5'] = returPageStay[4]
            res_table.loc[item.name[0], 'S3RS_6'] = returPageStay[5]
            res_table.loc[item.name[0], 'S3RS_7'] = returPageStay[6]
            res_table.loc[item.name[0], 'S3RS_8'] = returPageStay[7]
            res_table.loc[item.name[0], 'S3RS_9'] = returPageStay[8]
            res_table.loc[item.name[0], 'S3RS_10'] = returPageStay[9]
            res_table.loc[item.name[0], 'S3RS_11'] = returPageStay[10]
            res_table.loc[item.name[0], 'S3RS_12'] = returPageStay[11]
            res_table.loc[item.name[0], 'S3RO'] = RO
            res_table.loc[item.name[0], 'S3ROS'] = ROS
            res_table.loc[item.name[0], 'S31ST'] = ansRETU[0]
            res_table.loc[item.name[0], 'S3STT'] = TT
            res_table.loc[item.name[0], 'S3STT_1'] = STT[0]
            res_table.loc[item.name[0], 'S3STT_2'] = STT[1]
            res_table.loc[item.name[0], 'S3STT_3'] = STT[2]
            res_table.loc[item.name[0], 'S3STT_4'] = STT[3]
            res_table.loc[item.name[0], 'S3STT_5'] = STT[4]
            res_table.loc[item.name[0], 'S3STT_6'] = STT[5]
            res_table.loc[item.name[0], 'S3STT_7'] = STT[6]
            res_table.loc[item.name[0], 'S3STT_8'] = STT[7]
            res_table.loc[item.name[0], 'S3STT_9'] = STT[8]
            res_table.loc[item.name[0], 'S3STT_10'] = STT[9]
            res_table.loc[item.name[0], 'S3STT_11'] = STT[10]
            res_table.loc[item.name[0], 'S3STT_12'] = STT[11]
            res_table.loc[item.name[0], 'S3READ'] = ReadingTime
            res_table.loc[item.name[0], 'S3START'] = start
            res_table.loc[item.name[0], 'S31ANS'] = ansTime[0]
            res_table.loc[item.name[0], 'S3Draft'] = draftRate
        elif item.name[1] == 4:
            res_table.loc[item.name[0], 'S4RETU'] = RETU
            res_table.loc[item.name[0], 'S4RETU_1'] = returPageTimes[0]
            res_table.loc[item.name[0], 'S4RETU_2'] = returPageTimes[1]
            res_table.loc[item.name[0], 'S4RETU_3'] = returPageTimes[2]
            res_table.loc[item.name[0], 'S4RETU_4'] = returPageTimes[3]
            res_table.loc[item.name[0], 'S4RETU_5'] = returPageTimes[4]
            res_table.loc[item.name[0], 'S4RETU_6'] = returPageTimes[5]
            res_table.loc[item.name[0], 'S4RETU_7'] = returPageTimes[6]
            res_table.loc[item.name[0], 'S4RETU_8'] = returPageTimes[7]
            res_table.loc[item.name[0], 'S4RETU_9'] = returPageTimes[8]
            res_table.loc[item.name[0], 'S4RS_1'] = returPageStay[0]
            res_table.loc[item.name[0], 'S4RS_2'] = returPageStay[1]
            res_table.loc[item.name[0], 'S4RS_3'] = returPageStay[2]
            res_table.loc[item.name[0], 'S4RS_4'] = returPageStay[3]
            res_table.loc[item.name[0], 'S4RS_5'] = returPageStay[4]
            res_table.loc[item.name[0], 'S4RS_6'] = returPageStay[5]
            res_table.loc[item.name[0], 'S4RS_7'] = returPageStay[6]
            res_table.loc[item.name[0], 'S4RS_8'] = returPageStay[7]
            res_table.loc[item.name[0], 'S4RS_9'] = returPageStay[8]
            res_table.loc[item.name[0], 'S4RO'] = RO
            res_table.loc[item.name[0], 'S4ROS'] = ROS
            res_table.loc[item.name[0], 'S41ST'] = ansRETU[0]
            res_table.loc[item.name[0], 'S42ST'] = ansRETU[1]
            res_table.loc[item.name[0], 'S4STT'] = TT
            res_table.loc[item.name[0], 'S4STT_1'] = STT[0]
            res_table.loc[item.name[0], 'S4STT_2'] = STT[1]
            res_table.loc[item.name[0], 'S4STT_3'] = STT[2]
            res_table.loc[item.name[0], 'S4STT_4'] = STT[3]
            res_table.loc[item.name[0], 'S4STT_5'] = STT[4]
            res_table.loc[item.name[0], 'S4STT_6'] = STT[5]
            res_table.loc[item.name[0], 'S4STT_7'] = STT[6]
            res_table.loc[item.name[0], 'S4STT_8'] = STT[7]
            res_table.loc[item.name[0], 'S4STT_9'] = STT[8]
            res_table.loc[item.name[0], 'S4READ'] = ReadingTime
            res_table.loc[item.name[0], 'S4START'] = start
            res_table.loc[item.name[0], 'S41ANS'] = ansTime[0]
            res_table.loc[item.name[0], 'S42ANS'] = ansTime[1]
            res_table.loc[item.name[0], 'S4Draft'] = draftRate
        else:
            res_table.loc[item.name[0], 'S5RETU'] = RETU
            res_table.loc[item.name[0], 'S5RETU_1'] = returPageTimes[0]
            res_table.loc[item.name[0], 'S5RETU_2'] = returPageTimes[1]
            res_table.loc[item.name[0], 'S5RS_1'] = returPageStay[0]
            res_table.loc[item.name[0], 'S5RS_2'] = returPageStay[1]
            res_table.loc[item.name[0], 'S5RO'] = RO
            res_table.loc[item.name[0], 'S5ROS'] = ROS
            res_table.loc[item.name[0], 'S51ST'] = ansRETU[0]
            res_table.loc[item.name[0], 'S52ST'] = ansRETU[1]
            res_table.loc[item.name[0], 'S53ST'] = ansRETU[2]
            res_table.loc[item.name[0], 'S54ST'] = ansRETU[3]
            res_table.loc[item.name[0], 'S55ST'] = ansRETU[4]
            res_table.loc[item.name[0], 'S5STT'] = TT
            res_table.loc[item.name[0], 'S5STT_1'] = STT[0]
            res_table.loc[item.name[0], 'S5STT_2'] = STT[1]
            res_table.loc[item.name[0], 'S5READ'] = ReadingTime
            res_table.loc[item.name[0], 'S5START'] = start
            res_table.loc[item.name[0], 'S51ANS'] = ansTime[0]
            res_table.loc[item.name[0], 'S52ANS'] = ansTime[1]
            res_table.loc[item.name[0], 'S53ANS'] = ansTime[2]
            res_table.loc[item.name[0], 'S54ANS'] = ansTime[3]
            res_table.loc[item.name[0], 'S55ANS'] = ansTime[4]
            res_table.loc[item.name[0], 'S5Draft'] = draftRate
    except Exception as e:
        print(e)
        print('error')


table.groupby(['id']).apply(join2)
table.groupby(['id', 'qcode']).apply(join)

res_table.to_csv('res.csv')
