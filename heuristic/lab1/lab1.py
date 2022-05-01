import random
import numpy as np
import copy

n = int(input('Введите кол-во процессоров(столбцы матрицы): '))
#x1 = int(input('Введите левую границу кол-ва заданий(строки матрицы): '))
#y1 = int(input('Введите правую границу кол-ва заданий(строки матрицы): '))
x2 = int(input('Введите левую границу мн-ва весов(значения матрицы): '))
y2 = int(input('Введите правую границу мн-ва весов(значения матрицы): '))
#col = random.randint(x1, y1)  # столбцы
col = 11
T = random.randint(x2, y2) # мн-во весов
print('Искомый массив:')
matrix = []
for i in range(col):
    T = random.randint(x2, y2)
    matrix.append([])
    for j in range(n):
        matrix[i].append(T)
[print(*[i for i in j]) for j in matrix]
matrix = sorted([matrix[i][0] for i in range(col)], reverse=True)
print('Однородный массив значений (вектор заданий T):')
print([i for i in matrix])
count_ = len(matrix)
print(f'Количество элементов вектора заданий = {count_}')
p = int(np.ceil(np.log2(count_)))

def ofmtsolve(z ,x, y):  # алгоритм деления
    for i in range(len(z)):  # len(matrix)
        if sum(x) <= sum(y):
            x.append(z[i])
        else:
            y.append(z[i])
    return x, y

OFMTT = list(ofmtsolve(matrix, [], []))
s = [[]] * 2
s[:2] = [OFMTT[i] for i in range(2)]
print(f'1 уровень: {s}')
h, flag = [], False
for k in range(len(s)):
    h.append(sum(s[k]))
print(f'Значения нагрузки: {h}')
for i in range(p - 1):
    x, h = [], []
    for j in range(2 ** (i + 2)):  # 2 ** (i + 2)
        if j % 2 == 0:
            if len(s[j // 2]) > 1:
                x[j:j + 1] = list(ofmtsolve(s[j // 2], [], []))
            else:
                x[j:j + 1] = [s[j // 2]]
    s = copy.deepcopy(x)
    for k in range(len(x)):
        h.append(sum(x[k]))
    print(f'{i + 2} уровень: {x}')
    print(f'Значения нагрузки: {h}')
    for elem in x:
        if [max(h)] == elem:
            flag = True
            break
    if flag == True:
        break
elements = ''
for i in range(len(h)):
    elements += str(h[i]) + ', ' * (i != len(h) - 1)
print(f"max({elements}) = {max(h)}")