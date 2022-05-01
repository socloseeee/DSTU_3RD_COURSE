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

# new_matrix = [['x⁰' if matrix[j][i] != min(matrix[j]) else matrix[j][i] for i in range(n)] for j in range(col)]
# new_matrix = []
# print('МЕТОД МИНИМАЛЬНЫХ ЭЛЕМЕНТОВ:')
# for j in range(col):
#     new_matrix.append([])
#     check = 0  # check - позволяет вычленять из двух одинаковых только первое левое значение
#     for i in range(n):
#         if matrix[j][i] != min(matrix[j]) or matrix[j][i] == check:
#             new_matrix[j].append('x⁰')
#         else:
#             new_matrix[j].append(matrix[j][i])
#             check = int(matrix[j][i])
# print('Расписание:')
# [print(*[str(i).ljust(2) for i in j]) for j in new_matrix]
# new_matrix = list(zip(*new_matrix))
# result = [sum([new_matrix[j][i] for i in range(len(new_matrix[0])) if new_matrix[j][i] != 'x⁰']) for j in
#           range(len(new_matrix))]
# print('Результат:')
# print(f'max{tuple(result)} = {max(result)}')

print('МЕТОД КВАДРАТОВ:')
result_str = [0] * n
new_matrix = [[0 for i in range(n)] for j in range(col)]

print('Расписание:')
for j in range(col):
    min_sum = [0] * n
    for i in range(n):
        result_str[i] += matrix[j][i]
        #result_str[i] *= result_str[i]
        min_sum[i] = sum([elem * elem for elem in result_str])
        #result_str[i] = int(math.sqrt(result_str[i]))
        result_str[i] -= matrix[j][i]
    min_sum_index = min_sum.index(min(min_sum))
    #print(min_sum)
    for i in range(n):
        if i == min_sum_index:
            result_str[i] += matrix[j][i]
            #min_sum[i] = int(math.sqrt(min_sum[i]))
        #else:
            #min_sum[i] = int(math.sqrt(min_sum[i]))
            #min_sum[i] = result_str[i]
    #print(min_sum)
    print(*[str(result_str[i]).ljust(2) if result_str[i] != 0 else 'x⁰' for i in range(len(result_str))])
print('Результат:')
print(f'max{tuple(result_str)} = {max(result_str)}')
