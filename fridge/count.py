from os import lstat, stat
import pandas as pd

f = pd.read_csv('join.csv', index_col=0)

INC = 1
DEC = -1


for index in f.index:
    ans = f.loc[90000105106.0].answer
    print(index)
    typeCode = 0
    code = 00

    type1_tower = [0 for x in range(3)]
    type1_water = [0 for x in range(5)]

    arr_tower = []
    arr_water = []

    start = 0
    end = 0
    direction = INC
    ans = eval(ans)
    ans = [eval(x) for x in ans]
    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][0] == ans[end][0]:
            delt = ans[i][1] - ans[end][1]
            if abs(delt) == 1:
                if start == end:
                    direction = delt
                    end = i
                else:
                    if direction != delt:
                        length = end - start + 1
                        if length == 5:
                            arr_water.append(ans[start:end+1])
                        start = end
                        end = i
                        direction = delt
                        continue
                    else:
                        end = i
                        continue
            else:
                length = end - start + 1
                if length == 5:
                    arr_water.append(ans[start:end+1])
                start = i
                end = i
        else:
            length = end - start + 1
            if length == 5:
                arr_water.append(ans[start:end+1])
            start = i
            end = i
    length = end - start + 1
    if length == 5:
        arr_water.append(ans[start:end+1])

    for i in arr_water:
        type1_water[i[0][1]] = 1
    nums = type1_water.count(1)
    if nums >= 2:
        typeCode = 1
        code = 31
        continue
    if nums == 1:
        typeCode = 1
        code = 33
        continue

    for i in range(len(ans)):
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
                        length = end - start + 1
                        if length == 3:
                            arr_tower.append(ans[start:end+1])
                        start = end
                        end = i
                        direction = delt
                        continue
                    else:
                        end = i
                        continue
            else:
                length = end - start + 1
                if length == 3:
                    arr_tower.append(ans[start:end+1])
                start = i
                end = i
        else:
            length = end - start + 1
            if length == 3:
                arr_tower.append(ans[start:end+1])
            start = i
            end = i
    length = end - start + 1
    if length == 3:
        arr_tower.append(ans[start:end+1])

    for i in arr_tower:
        type1_tower[i[0][0]] = 1
    nums = type1_tower.count(1)
    if nums >= 2:
        typeCode = 1
        code = 32
        continue
    if nums == 1:
        typeCode = 1
        code = 34
        continue

    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][0] == ans[end][0]:
            end = i
            continue
        else:
            length = end - start + 1
            if length >= 5:
                res = list(
                    set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
                if len(res) == 5:
                    arr_water.append(res)
                    break
                else:
                    start = i
                    end = i
                    continue
            else:
                start = i
                end = i
                continue
    length = end - start + 1
    if length >= 5:
        res = list(set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
        if len(res) == 5:
            arr_water.append(res)
    if len(arr_water) != 0:
        typeCode = 2
        code = 21

    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][1] == ans[end][1]:
            end = i
            continue
        else:
            length = end - start + 1
            if length >= 3:
                res = list(
                    set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
                if len(res) == 3:
                    arr_tower.append(res)
                    break
                else:
                    start = i
                    end = i
                    continue
            else:
                start = i
                end = i
                continue
    length = end - start + 1
    if length >= 3:
        res = list(set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
        if len(res) == 3:
            arr_tower.append(res)
    if len(arr_tower) != 0:
        typeCode = 2
        code = 23

    for i in range(3):
        start = 0
        end = 0
        lstart = 0
        lend = 0
        count = 0
        for j in range(start, len(ans)):
            if ans[start][0] != i:
                start = end = j
                continue
            if j == end:
                continue
            if ans[j][0] == i:
                end = j
                continue
            else:
                if count == 0:
                    count += 1
                    lstart, lend = start, end
                    continue
                else:
                    if lend == end:
                        count = 0
                        start = end = j+1
                        continue
                    length = end - start + 1
                    if length > 5:
                        res = list(
                            set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
                        if len(res) > 5:
                            print(ans[start:end+1])
                            print(res)
                            arr_water.append(res)
                            start = -1
                            end = -1
                            break
                    start = lend + 2
                    end = j - 1
                    lend = end
                    # count = 0
                    continue
        length = end - start + 1
        if length > 5:
            res = list(
                set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
            if len(res) > 5:
                print(ans[start:end+1])
                print(res)
                arr_water.append(res)
    if len(arr_water) != 0:
        typeCode = 2
    print(typeCode)
    print(code)
