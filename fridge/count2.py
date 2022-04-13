import pandas as pd

f = pd.DataFrame(pd.read_csv('join2.csv', index_col=0))

INC = 1
DEC = -1

typeSum = [0 for _ in range(4)]
codeSum = {}
codeSum[0] = 0
codeSum[31] = 0
codeSum[32] = 0
codeSum[33] = 0
codeSum[34] = 0
codeSum[21] = 0
codeSum[22] = 0
codeSum[23] = 0
codeSum[24] = 0
codeSum[11] = 0
codeSum[12] = 0
codeSum[13] = 0
codeSum[14] = 0


f['type'] = 0
f['code'] = 0
f['cover'] = 0

for index in f.index:
    ans = f.loc[index].answer
    print(index)
    typeCode = 0
    code = 00

    type1_tower = [0 for x in range(5)]
    type1_water = [0 for x in range(3)]

    arr_tower = []
    arr_water = []
    group_arr_tower = []
    group_arr_water = []
    continuous_arr_tower = []
    continuous_arr_water = []

    start = 0
    end = 0
    direction = INC
    ans = eval(ans)
    ans = [eval(x) for x in ans]
    temp = list(set(list(map(lambda x: x[0]*5+x[1], ans))))
    f.loc[index, 'cover counts'] = len(temp) / 15
    f.loc[index, 'cover rate'] = len(temp)
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
    continuous_arr_water.append(ans[start:end+1])

    for i in continuous_arr_water:
        if len(i) == 5:
            type1_water[i[0][0]] = 1

    start = 0
    end = 0
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
                        continuous_arr_tower.append(ans[start:end+1])
                        start = end
                        end = i
                        direction = delt
                        continue
                    else:
                        end = i
                        continue
            else:
                continuous_arr_tower.append(ans[start:end+1])
                start = i
                end = i
        else:
            continuous_arr_tower.append(ans[start:end+1])
            start = i
            end = i
    continuous_arr_tower.append(ans[start:end+1])

    for i in continuous_arr_tower:
        if len(i) == 3:
            type1_tower[i[0][1]] = 1

    nums = type1_water.count(1)
    if nums >= 2:
        typeCode = 1
        code = 31
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    nums = type1_tower.count(1)
    if nums >= 2:
        typeCode = 1
        code = 32
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    nums = type1_water.count(1)
    if nums == 1:
        typeCode = 1
        code = 33
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    nums = type1_tower.count(1)
    if nums == 1:
        typeCode = 1
        code = 34
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    start = 0
    end = 0
    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][0] == ans[end][0]:
            end = i
            continue
        else:
            res = list(
                    set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
            group_arr_water.append(res)
            start = i
            end = i
            continue

    res = list(set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
    group_arr_water.append(res)

    num = 0
    for i in group_arr_water:
        if len(i) == 5:
            num += 1
    if num != 0:
        typeCode = 2
        code = 21
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    start = 0
    end = 0
    for i in range(len(ans)):
        if i == end:
            continue
        if ans[i][1] == ans[end][1]:
            end = i
            continue
        else:
            res = list(
                    set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
            group_arr_tower.append(res)
            start = i
            end = i

    res = list(set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
    group_arr_tower.append(res)

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
                    res = list(
                            set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
                    arr_water.append(res)
                    start = lend + 2
                    end = j - 1
                    lend = end
                    continue
        res = list(
                set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
        arr_water.append(res)
    num = 0
    for i in arr_water:
        if len(i) == 6:
            num += 1
    if num != 0:
        typeCode = 2
        code = 22
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    num = 0
    for i in group_arr_tower:
        if len(i) == 3:
            num += 1
    if num != 0:
        typeCode = 2
        code = 23
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    for i in range(5):
        start = 0
        end = 0
        lstart = 0
        lend = 0
        count = 0
        for j in range(start, len(ans)):
            if ans[start][1] != i:
                start = end = j
                continue
            if j == end:
                continue
            if ans[j][1] == i:
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
                    res = list(
                            set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
                    arr_tower.append(res)
                    start = lend + 2
                    end = j - 1
                    lend = end
                    # count = 0
                    continue
        res = list(
                set(list(map(lambda x: x[0]*5+x[1], ans[start:end+1]))))
        arr_tower.append(res)
    num = 0
    for i in arr_tower:
        if len(i) == 4:
            num += 1
    if num != 0:
        typeCode = 2
        code = 24
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    num = 0
    for i in group_arr_water:
        if len(i) in [3, 4]:
            num += 1
    if num != 0:
        typeCode = 3
        code = 11
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    num = 0
    for i in arr_water:
        if len(i) in [3, 4]:
            num += 1
    if num != 0:
        typeCode = 3
        code = 12
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    num = 0
    for i in group_arr_tower:
        if len(i) == 2:
            num += 1
    if num != 0:
        typeCode = 3
        code = 13
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue

    for i in arr_tower:
        if len(i) == 2:
            num += 1
    if num != 0:
        typeCode = 3
        code = 14
        typeSum[typeCode] += 1
        codeSum[code] += 1
        f.loc[index, 'type'] = typeCode
        f.loc[index, 'code'] = code
        continue
    f.loc[index, 'type'] = 0
    f.loc[index, 'code'] = 0
    typeSum[0] += 1
    codeSum[0] += 1

f.to_csv('result2.csv')

print(sum(typeSum))
summery = sum(typeSum)
print(sum(codeSum))

with open('result2.txt', 'w') as f:
    for i in codeSum:
        toWrite = str(i) + ',' + \
                str(codeSum[i]) + ',' + str(codeSum[i] / summery) + '\n'
        print(toWrite)
        f.write(toWrite)
    sum1 = codeSum[31] + codeSum[32] + codeSum[33] + codeSum[34]
    f.write(str('1') + ',' + str(sum1) + ',' + str(sum1 / summery) + '\n')
    sum1 = codeSum[21] + codeSum[22] + codeSum[23] + codeSum[24]
    f.write(str('2') + ',' + str(sum1) + ',' + str(sum1 / summery) + '\n')
    sum1 = codeSum[11] + codeSum[12] + codeSum[13] + codeSum[14]
    f.write(str('3') + ',' + str(sum1) + ',' + str(sum1 / summery) + '\n')
