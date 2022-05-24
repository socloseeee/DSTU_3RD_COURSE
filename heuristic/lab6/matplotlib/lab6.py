from random import choice as c, randint as r
from copy import deepcopy
import matplotlib.pyplot as plt
import os


# Генерируем матрицу(m - строки, n - столбцы) со значениями от T1 до T2:
def generate_matrix(m, n, T1, T2):
    return [[r(T1, T2) for j in range(n)] for i in range(m)]


# Генерируем особь:
def generate_individ(m):
    return [r(1, 255) for elem in range(m)]


# Считаем загрузки:
def count_load(individ, n=5, t=255):
    load_result = [0 for _ in range(n)]
    proc = [i for i in range(t//n, t + t//n, int(t/n))]
    for j, gen in enumerate(individ):
        for i in range(n):
            if gen <= proc[i]:
                load_result[i] += matrix[j][i]
                break
    return load_result


# Считаем лучшую загрузку для каждой особи:
def best_load(max_loads):
    result = [max(el) for el in max_loads]
    return (min(result), result.index(min(result)))


# Двухточечный кроссовер
def crossover(parent1, parent2):
    T1 = r(1, len(parent1) - 1)
    T2 = r(1, len(parent1) - 1)
    while T2 == T1:
        T2 = r(1, len(parent1) - 1)
    if T1 > T2:
        T1, T2 = T2, T1
    f.write(f'T: {T1}, {T2}\n')
    child1, child2 = parent1[:T1] + parent2[T1:T2+1] + parent1[T2+1:], parent2[:T1] + parent1[T1:T2+1] + parent2[T2+1:]
    return child1, child2


# Двухточечная мутация
def mutation(child, Pm):
    child_copy = deepcopy(child)
    child_genes = [e for e in child_copy]
    f.write(f'Genes before: {" ".join([str(e) for e in child_genes])}')
    gen = c(child_genes)
    while r(1, 100) < Pm:
        gen = c(child_genes)
    f.write(f'\nGene: {gen}\n')
    that_gen = deepcopy(gen)
    binary_gen = '00000000'
    for j in range(len(binary_gen)):
        binary_gen = binary_gen[:j] + str(gen % 2) + binary_gen[j + 1:]
        gen //= 2
    binary_gen = binary_gen[::-1]
    f.write(f'Its binary form: {binary_gen}')
    binary_gen = list(binary_gen)
    index1 = r(0, len(binary_gen)-1)
    index2 = r(0, len(binary_gen)-1)
    if binary_gen.count(binary_gen[0]) != len(binary_gen):
        while index2 == index1 or binary_gen[index1] == binary_gen[index2]: # чтоб 0 менялся с 1 и индексы не одинаковые
            index2 = r(0, len(binary_gen)-1)
    binary_gen[index1], binary_gen[index2] = binary_gen[index2], binary_gen[index1]
    binary_gen = "".join(binary_gen)
    f.write(f'\nChanged bit: {binary_gen}\nNew number: {int(binary_gen, 2)}\n')
    child_copy = [genes if genes != that_gen else int(binary_gen, 2) for genes in child_copy]
    f.write(f'Genes after: {" ".join([str(e) for e in child_copy])}\n')
    return child_copy


# Выводим нужное поколение
def show_generation(txt_file, amount_of_generations):
    with open(txt_file, 'r') as file:
        while True:
            file.seek(0)
            while True:
                num = input('Choose generation to show (exit - to quit programm) > ')
                if num.isdigit() and 0 <= int(num) <= amount_of_generations or num == 'exit':
                    chosen_generation = f"{num} GENERATION >\n"
                    break
                else:
                    print('Incorrect input!')
                chosen_generation = f"{num} GENERATION >\n"
            print()
            if num == 'exit':
                break
            generation_tree_data = file.readlines()
            new_slice = generation_tree_data[generation_tree_data.index(chosen_generation):]
            this_generation = new_slice[:new_slice.index('#\n')]
            print("".join(this_generation))
        print('Good Bye!')


# Переменные для задания ГА:
m = 12  # кол-во заданий
n = 3  # кол-во процессоров (кол-во равных промежутков от 0 до 255)
T1 = 10  # левая граница значения задания
T2 = 17  # правая граница значения задания
z = 11  # кол-во особей
k = 11  # кол-во поколений подряд при котором лучшая загрузка будет повторяться k-раз
Pk = 92  # вероятность кроссовера
Pm = 93  # вероятность мутации
newline = '\n'

# Открываем файл для записи:
txt_file = 'lab6_results.txt'
f = open(txt_file, 'w')

# Генерируем нулевое поколение:
matrix = generate_matrix(m, n, T1, T2)
individuals = [generate_individ(m) for _ in range(z)]  # генерируем родителей 0-го поколения

# Выводим матрицу (для последующих расчётов загрузки)
proc = [i for i in range(255//n, 255 + 255//n, int(255/n))]
col = [f'n{i+1}(value<{proc[i]})' for i in range(n)]
row = [f'm{i+1}' for i in range(m)]

fig, ax = plt.subplots()
fig.set_figheight(m // 4)
fig.set_figwidth(n*2)
ax.axis('tight')
ax.axis('off')
ax.table(cellText=matrix, cellLoc='center', rowLabels=row, rowColours=["palegreen"] * m, colLabels=col, colColours=["palegreen"] * n,loc='center')

ax.set_title('Матрица заданий', family='fantasy', size=15)
plt.savefig("Матрица заданий.png")

# Открываем картинку:
os.startfile(r'Матрица заданий.png')

# Особи нулевого поколения (родители для будущего поколения):
listMax = []
f.write('0 GENERATION >\n')
for i, individual in enumerate(individuals):
    f.write(f'{i+1} individual (O{i+1}): {" ".join([str(elem) for elem in individual])}\n')
    load = count_load(individual, n)
    listMax.append(load)
    f.write(f'load: {load}\n')
best_result, bestLoad_index = best_load(listMax)  # лучшая загрузка и (индекс лучшей особи - 1)
best_individual = individuals[bestLoad_index]
f.write(f'All_Loads:\n{newline.join(["(O" + str(i + 1) + ") " + " ".join([str(e) for e in el]) for i, el in enumerate(listMax)])}'
        f'\nBest individual is (O{bestLoad_index+1}):\n{" ".join([str(elem) for elem in best_individual])}\n')
f.write(f'Its load: {best_result}\n#\n')
previous_best_result, bestLoad_index = 0, 0
best_of_all_generations_result = best_result

# Переменные для ГА:
counter, gen_count = 0, 0

while k != counter - 1:
    previous_best_result = best_result
    gen_count += 1
    generation = []
    best_generation_loads = []
    f.write(f'\n{gen_count} GENERATION >\n'
            f'Parents:\n'
            f'{newline.join([str(i+1) + " individual" + "(O" + str(i+1) + ")" + newline + " ".join([str(elem) for elem in individual]) for i, individual in enumerate(individuals)])}\n\n')
    for _ in range(z):

        # Алгоритм образования пар родителей:
        parent1 = c(individuals)
        individuals_no_repeat = deepcopy(individuals)
        individuals_no_repeat.remove(parent1)  # дабы избежать попадание рандома на первого
        parent2 = c(individuals_no_repeat)
        while r(0, 100) <= Pk:
            parent2 = c(individuals_no_repeat)
        f.write(f'{_ + 1} child selection >\n')
        f.write(f'Pair of parents:\n'
                f'1 Parent: {" ".join(str(elem) for elem in parent1)}\n'
                f'2 Parent: {" ".join(str(elem) for elem in parent2)}\n')
        f.write(f'Parent1 load: {count_load(parent1, n)}\nParent2 load: {count_load(parent2, n)}\n')
        parents_list = (parent1, parent2)

        # Алгоритм отбора детей из потенциальных особей (2 + 2 мутанта)
        children = []
        load_list = []
        counter_child = 0
        crossover_result = crossover(parent1, parent2)
        f.write(f'Potential children:\n{newline.join([" ".join([str(el) for el in elem]) for elem in crossover_result])}\n')
        for i, child in enumerate(crossover_result):
            children.append(child)
            load_list.append(count_load(child, n))
            f.write(f'{counter_child+i+1} Potential child({i+1} without mutation):\n'
                    f'{" ".join([str(el) for el in child])}\n')
            f.write(f'Its load: {load_list[-1]}\n')
            f.write(f'Mutation process...\n')
            counter_child += 1
            muted_child = mutation(child, Pm)
            children.append(muted_child)
            load_list.append(count_load(muted_child, n))
            f.write(f'{counter_child + i + 1} Potential child({i + 1} with mutation):\n'
                    f'{" ".join([str(el) for el in child])}\n')
            f.write(f'Its load: {load_list[-1]}\n')
        best_child_load, best_child_index = best_load(load_list)
        num = 0
        if best_child_index == 0:
            f.write('The best child is 1 (without mutation):\n')
        elif best_child_index == 1:
            f.write('The best child is 1 (with mutation):\n')
        elif best_child_index == 2:
            f.write('The best child is 2 (without mutation):\n')
        else:
            f.write('The best child is 2 (with mutation): ')
        f.write(f'{" ".join([str(elem) for elem in children[best_child_index]])}\n')
        f.write(f'Its load: {best_child_load}\n\n')
        generation.append(children[best_child_index])

    # Список всех детей:
    f.write('Children:\n')
    listMax = []
    for i, child in enumerate(generation):
        f.write(f'{str(i + 1)}) {" ".join([str(elem) for elem in child])}\n')
        listMax.append(count_load(child, n))
    f.write(f'\nTheir load:\n{newline.join([str(i + 1) + ") " + " ".join([str(el) for el in count_load(elem, n)]) for i, elem in enumerate(generation)])}\n')

    # Индекс лучшего результата в поколении
    currentLoad = best_load(listMax)[1]

    # Собираем матрицу родителей и лучших детей для отбора:
    check_matrix, parent_child_loads = [], []
    for elem in generation:
        check_matrix.append(elem)
        parent_child_loads.append(max(count_load(elem, n)))
    for elem in individuals:
        check_matrix.append(elem)
        parent_child_loads.append(max(count_load(elem, n)))

    best_result = sorted(parent_child_loads)[0]

    # Создаём матрицу индексов лучших особей:
    best_index = []
    for elem in sorted(parent_child_loads)[:z]:
        for i, el in enumerate(parent_child_loads):
            if elem == el:
                best_index.append(i)
                break

    # Добавляем лучших особей поколения среди родителей и детей:
    individuals = []
    for elem in best_index:
        individuals.append(check_matrix[elem])

    f.write(f'\nBest individual: {" ".join([str(elem) for elem in individuals[0]])}\n')
    f.write(f'Its load: {" ".join([str(el) for el in count_load(individuals[0], n)])}\n')

    f.write(f'Best children + parents loads: {parent_child_loads}\n')
    f.write(f'Best z individuals: {sorted(parent_child_loads)[:z]}\n')
    f.write(f'Best load: {best_result}\n')

    # Если сквозь поколения была лучшая загрузка ждем когда она не повторится или улучшится:
    if best_result < best_of_all_generations_result:
        best_of_all_generations_result = best_result
        counter = 0

    # Если загрузка предыдущего поколения равна загрузке текущего
    if best_of_all_generations_result == best_result:
        counter += 1
    else:
        counter = 0
    f.write(f'#\n')
    # print(gen_count, best_result, best_of_all_generations_result)


print(f'Generations: {gen_count}\nBest result: {best_result}')
f.write(f'\nGenerations: {gen_count}\nBest result: {best_result}\n')

f.close()

# Вывод данных из нужного поколения:
show_generation(txt_file, gen_count)
