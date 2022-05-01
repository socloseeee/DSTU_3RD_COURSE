import random
import math

n = int(input('Введите кол-во процессоров(столбцы матрицы): '))
# x1 = int(input('Введите левую границу кол-ва заданий(строки матрицы): '))
# y1 = int(input('Введите правую границу кол-ва заданий(строки матрицы): '))
x2 = int(input('Введите левую границу мн-ва весов(значения матрицы): '))
y2 = int(input('Введите правую границу мн-ва весов(значения матрицы): '))
# col = random.randint(x1, y1)  # строки
col = 11
print('Искомый массив:')
matrix = []
for i in range(col):
    matrix.append([])
    for j in range(n):
        matrix[i].append(random.randint(x2, y2))
[print(*[i for i in j]) for j in matrix]

number, x = int(input(
    'Выберите метод сортировки массива(От большего к меньшему(1)/От меньшего к большему(2)/Наугад первый или второй метод(3)/Не сортировать(4)): ')), 0

while True:
    if number == 1:
        matrix_sum = sorted([sum(elem) for elem in matrix], reverse=True)
        break
    if number == 2:
        matrix_sum = sorted([sum(elem) for elem in matrix])
        break
    if number == 3:
        number = random.randint(1, 2)
    if number == 4:
        matrix_sum = matrix
        break

if number != 4:
    print('Суммы элементов строк:')
    print(*[i for i in matrix_sum])
    new_matrix = []
    for i in range(len(matrix_sum)):  # Сортируем массив
        for j in range(len(matrix)):
            if matrix_sum[i] == sum(matrix[j]):
                new_matrix.append(matrix[j])
                del matrix[j]
                break
    matrix = new_matrix

print('Отсортированный массив:')
[print(*[i for i in j]) for j in matrix]

new_matrix = [['x⁰' if matrix[j][i] != min(matrix[j]) else matrix[j][i] for i in range(n)] for j in range(col)]
new_matrix = []
print('МЕТОД МИНИМАЛЬНЫХ ЭЛЕМЕНТОВ:')
for j in range(col):
    new_matrix.append([])
    check = 0  # check - позволяет вычленять из двух одинаковых только первое левое значение
    for i in range(n):
        if matrix[j][i] != min(matrix[j]) or matrix[j][i] == check:
            new_matrix[j].append('x⁰')
        else:
            new_matrix[j].append(matrix[j][i])
            check = int(matrix[j][i])
print('Расписание:')
[print(*[str(i).ljust(2) for i in j]) for j in new_matrix]
new_matrix = list(zip(*new_matrix))
result = [sum([new_matrix[j][i] for i in range(len(new_matrix[0])) if new_matrix[j][i] != 'x⁰']) for j in
          range(len(new_matrix))]
print('Значение барьера:')
barrier = sum(result) / n
print(f'{" + ".join([str(elem) for elem in tuple(result)])} / {n} = {barrier}')

print('МЕТОД БАРЬЕРА:')
result_str = [0] * n
new_matrix = [['x⁰' if matrix[j][i] != min(matrix[j]) else matrix[j][i] for i in range(n)] for j in range(col)]
new_matrix = []
flag = False

for j in range(col):
    if not flag:
        new_matrix.append([])
        check = 0  # check - позволяет вычленять из двух одинаковых только первое левое значение
        for i in range(n):
            if matrix[j][i] != min(matrix[j]) or matrix[j][i] == check:
                new_matrix[j].append('x⁰')
            else:
                result_str[i] += matrix[j][i]
                new_matrix[j].append(matrix[j][i])
                check = int(matrix[j][i])
                if result_str[i] > barrier and not flag:
                    flag = True
                    new_matrix.append([])
                    for s in range(n):
                        new_matrix[-1].append('-')
    else:
        for i in range(n):
            result_str[i] += matrix[j][i]
        min_index = result_str.index(min(result_str))
        for i in range(n):
            if i != min_index:
                result_str[i] -= matrix[j][i]
        new_matrix.append([str(result_str[i]).ljust(2) if result_str[i] != 0 else 'x⁰' for i in range(len(result_str))])
print('Расписание:')
[print(*[str(i).ljust(2) for i in j]) for j in new_matrix]
print('Результат:')
print(f'max{tuple(result_str)} = {max(result_str)}')