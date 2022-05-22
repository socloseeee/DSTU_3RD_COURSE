from random import randint as r, choice as c
from copy import deepcopy


# Генерируем матрицу-строку длиной m со значениями от T1 до T2:
def generate_matrix(M, t1, t2):
    return [r(t1, t2) for _ in range(M)]


# Генерируем особь:
def generate_individ(MATRIX):
    return [(elem, r(1, 255)) for elem in MATRIX]


# Считаем загрузки:
def count_load(individ, n, t=255):
    load_result = [0 for _ in range(n)]
    proc = [i for i in range(t//n, t + t//n, int(t/n))]
    for task, gen in individ:
        for i in range(n):
            if gen <= proc[i]:
                load_result[i] += task
                break
    return load_result


# Считаем лучшую загрузку для каждой особи:
def best_load(max_loads):
    result = [max(el) for el in max_loads]
    return (min(result), result.index(min(result)))


# Кроссовер
def crossover(parent1, parent2):
    T = r(1, len(parent1) - 1)
    child1, child2 = parent1[:T] + parent2[T:], parent2[:T] + parent1[T:]
    return (child1, child2), T


# Мутация
def mutation(child, Pm):
    child_copy = deepcopy(child)
    child_genes = [e[1] for e in child_copy]
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
    index = r(0, len(binary_gen) - 1)
    change_bit = '1' if binary_gen[index] == '0' else '0'
    binary_gen = binary_gen[:index] + change_bit + binary_gen[index + 1:]
    f.write(f'\nChanged bit: {binary_gen}\nNew number: {int(binary_gen, 2)}\n')
    child_copy = [(task, genes) if genes != that_gen else (task, int(binary_gen, 2)) for task, genes in child_copy]
    f.write(f'Genes after: {" ".join([str(e[1]) for e in child_copy])}\n')
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
m = 13  # кол-во заданий
n = 5  # кол-во процессоров (кол-во равных промежутков от 0 до 255)
T1 = 9  # левая граница значения задания
T2 = 15  # правая граница значения задания
z = 11  # кол-во особей
k = 11  # кол-во поколений подряд при котором лучшая загрузка будет повторяться k-раз
Pk = 88  # вероятность кроссовера
Pm = 98  # вероятность мутации

# Открываем файл для записи:
txt_file = r'lab5_results.txt'
f = open(txt_file, 'w')

# Генерируем нулевое поколение:
matrix = generate_matrix(m, T1, T2)
individuals = [generate_individ(matrix) for _ in range(z)]  # генерируем родителей 0-го поколения

# Особи нулевого поколения (родители для будущего поколения):
listMax = []
f.write('0 GENERATION >\n')
for i, individual in enumerate(individuals):
    f.write(f'{i+1} individual (O{i+1}):\n{" ".join(["-".join([str(e) for e in el]) for el in individual])}')
    load = count_load(individual, n)
    listMax.append(load)
    f.write(f'\nload: {load}\n')
best_result, bestLoad_index = best_load(listMax)  # лучшая загрузка и (индекс лучшей особи - 1)
best_individual = individuals[bestLoad_index]
newline = '\n'
f.write(f'\nAll_Loads:\n{newline.join(["(O" + str(i + 1) + ") " + " ".join([str(e) for e in el]) for i, el in enumerate(listMax)])}\nBest_individual(0{bestLoad_index + 1}):\n{" ".join(["-".join([str(e) for e in el]) for el in best_individual])}\nIts load: {best_result}\n#\n')
previous_best_result, bestLoad_index = 0, 0
best_of_all_generations_result = best_result

# Переменные для ГА:
counter, gen_count = 0, 0

while k != counter:
    previous_best_result = best_result
    gen_count += 1
    generation = []
    best_generation_loads = []
    f.write(f'\n{gen_count} GENERATION >\nParents:\n{newline.join([" ".join(["-".join([str(elem) for elem in e])  for e in el]) for el in individuals])}\n\n')
    for _ in range(z):

        # Алгоритм образования пар родителей:
        parent1 = c(individuals)
        individuals_no_repeat = deepcopy(individuals)
        individuals_no_repeat.remove(parent1)  # дабы избежать попадание рандома на первого
        parent2 = c(individuals_no_repeat)
        while r(0, 100) <= Pk:
            parent2 = c(individuals_no_repeat)
        parents_list = (parent1, parent2)

        # Алгоритм отбора детей из потенциальных особей (2 + 2 мутанта)
        goldberg_selection = []
        load_list = []
        f.write(f'{_+1} child >')
        f.write(f'\nPair of parents:\n{" ".join(["-".join([str(e) for e in el]) for el in parent1])}\n{" ".join(["-".join([str(e) for e in el]) for el in parent2])}\n')
        crossover_result, T = crossover(parent1, parent2)
        f.write(f'Potential children(T={T}):\n{newline.join([" ".join(["-".join([str(e) for e in el]) for el in elem]) for elem in crossover_result])}\n')
        for i, child in enumerate(crossover_result):
            goldberg_selection.append(child)
            load_list.append(count_load(child, n))
            f.write(f'{i+1} Potential child(without mutation): {" ".join(["-".join([str(e) for e in el]) for el in child])}\nIts load: {load_list[-1]}\n')
            muted_child = mutation(child, Pm)
            goldberg_selection.append(muted_child)
            load_list.append(count_load(muted_child, n))
            f.write(f'{i+1} Potential child(with mutation): {" ".join(["-".join([str(e) for e in el]) for el in muted_child])}\nIts load: {load_list[-1]}\n')
        goldberg_selection.append(parent1)
        load_list.append(count_load(parent1, n))
        best_result, best_index = best_load(load_list)
        f.write(f'Children + parent loads (4+1): {[max(elem) for elem in load_list]}\n')
        if best_index == 0:
            f.write(f'1 potential child(without mutation) wins!\n')
        elif best_index == 1:
            f.write(f'1 potential child(with mutation) wins!\n')
        elif best_index == 2:
            f.write(f'2 potential child(without mutation) wins!\n')
        elif best_index == 3:
            f.write(f'2 potential child(with mutation) wins!\n')
        else:
            f.write(f'Parent wins!\n')
        f.write(f'\n')
        best_individual_now = goldberg_selection[best_index]
        generation.append(best_individual_now)

    # Список всех детей:
    f.write('\nChildren:\n')
    listMax = []
    for i, child in enumerate(generation):
        f.write(f'{str(i + 1) + ") " + " ".join(["-".join([str(e) for e in el]) for el in child])}\n')
        listMax.append(count_load(child, n))
    f.write(f'\nTheir load:\n{newline.join([str(i + 1) + ") " + " ".join([str(el) for el in count_load(elem, n)]) for i, elem in enumerate(generation)])}\n')

    # Лучший результат поколения и его индекс минус 1
    best_result, currentLoad = best_load(listMax)

    f.write(f'\nBest child({currentLoad + 1}): {" ".join(["-".join([str(e) for e in el]) for el in generation[currentLoad]])}\n')
    f.write(f'Its parents:\n{newline.join([" ".join(["-".join([str(e) for e in el]) for el in elem]) for elem in parents_list])}')
    f.write(f'\nTheir load:\n{newline.join([" ".join([str(el) for el in count_load(elem, n)]) for elem in parents_list])}\nBest child load: {best_result}\n')

    # Копируем поколение детей для того чтоб они были родителями в будущем:
    individuals = generation

    # Если сквозь поколения была лучшая загрузка ждем когда она не повторится или улучшится:
    if best_result < best_of_all_generations_result:
        best_of_all_generations_result = best_result
        counter = 0

    # Если загрузка предыдущего поколения равна загрузке текущего
    if best_result == previous_best_result:
        counter += 1
    else:
        counter = 0
    f.write(f'#\n')

print(f'Generations: {gen_count}\nBest result: {best_result}')
f.write(f'\nGenerations: {gen_count}\nBest result: {best_result}\n')

f.close()

# Вывод данных из нужного поколения:
show_generation(txt_file, gen_count)
