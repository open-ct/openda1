import pandas as pd

f = pd.DataFrame(pd.read_csv('./joinPage3.csv', index_col=0))

INC = 1
DEC = 1

codeSum = {}
codeSum[30] = 0
codeSum[31] = 0
codeSum[21] = 0
codeSum[20] = 0
codeSum[10] = 0
codeSum[11] = 0
codeSum[70] = 0

for index in f.index:
    ans = f.loc[index, '0']

    code = 70
    start = 0
    end = 0
    direction = INC

    points = [[0 for _ in range(5)] for _ in range(5)]
    ans = eval(ans)
    ans = [eval(x) for x in ans]

    print(ans)
    continuous_arr_temp = []
    for i in range(len(ans)):
        points[ans[i][1]//7 - 1][ans[i][0]-1] = 1
        if i == end:
            continue
        if ans[i][1] == ans[end][1]:
            delt = ans[i][0] - ans[end][0]
            if abs(delt) == 1:
                if start == end:
                    direction = delt
                    end = i
                else:
                    if direction != delt:
                        continuous_arr_temp.append(ans[start:end+1])
                        start = end
                        end = i
                        direction = delt
                        continue
                    else:
                        end = i
                        continue
            else:
                continuous_arr_temp.append(ans[start:end+1])
                start = i
                end = i
        else:
            continuous_arr_temp.append(ans[start:end+1])
            start = i
            end = i

    print(points)
    arr = [0 for _ in range(5)]
    for i in continuous_arr_temp:
        if len(i) == 5:
            arr[i[0][1]//7 - 1] = 1

    if sum(arr) > 1:
        code = 30
        codeSum[30] += 1
        continue
    if sum(arr) == 1:
        code = 31
        codeSum[31] += 1
        continue

    group_arr_temp = []
    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][1] == ans[end][1]:
            end = i
            continue
        else:
            res = list(
                set(list(map(lambda x: x[0]+x[1]*7, ans[start:end+1]))))
            group_arr_temp.append(res)
            start = i
            end = i
    arr = [0 for _ in range(5)]
    num = 0
    for i in group_arr_temp:
        if len(i) == 5:
            num += 1

    if num != 0:
        code = 21
        codeSum[21] += 1
        continue

    num = 0
    for i in points:
        if sum(i) == 5:
            num += 1
    if num != 0:
        code = 20
        codeSum[20] += 1
        continue

    arr = [0 for _ in range(5)]
    for i in continuous_arr_temp:
        if len(i) >= 3:
            arr[i[0][1]//7 - 1] = 1
    if sum(arr) > 1:
        code = 10
        codeSum[10] += 1
        continue

    selection = [7, 14, 21, 28, 35]

    tt = []
    for s in selection:
        temp = []
        for i in range(len(ans)):
            if ans[i][1] == s:
                temp.append(ans[i][0])
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
        codeSum[11] += 1
        continue
    code = 70
    codeSum[70] += 1
print(codeSum)
