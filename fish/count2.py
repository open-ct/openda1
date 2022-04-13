import pandas as pd

f = pd.DataFrame(pd.read_csv('./joinPage7.csv', index_col=0))

INC = 1
DEC = 1

codeSum = {}
codeSum[130] = 0
codeSum[131] = 0
codeSum[121] = 0
codeSum[120] = 0
codeSum[110] = 0
codeSum[111] = 0
codeSum[170] = 0

codeSum[230] = 0
codeSum[231] = 0
codeSum[221] = 0
codeSum[220] = 0
codeSum[210] = 0
codeSum[211] = 0
codeSum[270] = 0

for index in f.index:
    ans = f.loc[index, '0']

    code = 70
    start = 0
    end = 0
    direction = INC
    plus = 100

    points = [[0 for _ in range(5)] for _ in range(5)]
    ans = eval(ans)
    ans = [eval(x) for x in ans]
    print(ans)

    continuous_arr_water = []
    for i in range(len(ans)):
        points[ans[i][0]-1][ans[i][-1] - 1] = 1
        if i == end:
            continue
        if ans[i][1] != ans[i-1][1]:
            plus = 200
        if ans[i][0] == ans[end][0]:
            delt = ans[i][-1] - ans[end][-1]
            if abs(delt) == 1:
                if start == end:
                    direction = delt
                    end = i
                else:
                    if direction != delt:
                        continuous_arr_water.append(ans[start:end+1])
                        start = end
                        end = i
                        direction = delt
                        continue
                    else:
                        end = i
                        continue
            else:
                continuous_arr_water.append(ans[start:end+1])
                start = i
                end = i
        else:
            continuous_arr_water.append(ans[start:end+1])
            start = i
            end = i
    arr = [0 for _ in range(5)]
    for i in continuous_arr_water:
        if len(i) == 5:
            arr[i[0][0]-1] = 1

    if sum(arr) > 1:
        code = 30
        codeSum[plus + 30] += 1
        continue
    if sum(arr) == 1:
        code = 31
        codeSum[plus+31] += 1
        continue

    group_arr_water = []
    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][0] == ans[end][0]:
            end = i
            continue
        else:
            res = list(
                set(list(map(lambda x: x[0]*5+x[2], ans[start:end+1]))))
            group_arr_water.append(res)
            start = i
            end = i
    arr = [0 for _ in range(5)]
    num = 0
    for i in group_arr_water:
        if len(i) == 5:
            num += 1

    if num != 0:
        code = 21
        codeSum[plus + 21] += 1
        continue

    num = 0
    for i in points:
        if sum(i) == 5:
            num += 1
    if num != 0:
        code = 20
        codeSum[plus + 20] += 1
        continue

    arr = [0 for _ in range(5)]
    for i in continuous_arr_water:
        if len(i) >= 3:
            arr[i[0][0] - 1] = 1
    if sum(arr) > 1:
        code = 10
        codeSum[plus + 10] += 1
        continue

    selection = [1, 2, 3, 4, 5]

    tt = []
    for s in selection:
        temp = []
        for i in range(len(ans)):
            if ans[i][0] == s:
                temp.append(ans[i][-1])
        tt.append(temp)

    flag = False
    for i in tt:
        if len(i) < 3:
            continue
        start = 0
        end = 0
        flag = False
        for index in range(len(i)):
            if end == index:
                continue
            if abs(i[index] - i[end]) == 1:
                end = index
            else:
                start = index
                end = index
                continue
            if end - start + 1 == 3:
                flag = True
                break
        if flag:
            break
    if flag:
        code = 11
        codeSum[plus + 11] += 1
        continue
    code = 70
    codeSum[plus + 70] += 1
print(codeSum)
