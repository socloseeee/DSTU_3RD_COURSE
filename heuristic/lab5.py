from random import choice as c, randint as r
from copy import deepcopy


# Функция ввода и проверки валидности ВВЕДЁННЫХ ЧЕРЕЗ КОНСОЛЬ значений для нашей задачи!
def input_values(m='', n='', T1='', T2='', z='', k='', Pk='', Pm=''):
    while not m.isdigit():
        m = input('Введите кол-во элементов в строке > ')
        if not m.isdigit():
            print('Введите корректное значение!')
    while not n.isdigit():
        n = input('Введите кол-во столбцов(в фенотипе) > ')
        if not n.isdigit():
            print('Введите корректное значение!')
    while not T1.replace('-', '', 1).isdigit():
        T1 = input('Введите левую границу мн-ва весов(значения матрицы): ')
        if not T1.replace('-', '', 1).isdigit():
            print('Введите корректное значение!')
    if not T2.replace('-', '', 1).isdigit() or int('0' + T2) < int('0' + T1):
        if int('0' + T2) < int('0' + T1) and len(T2) > 0:
            print('Правая граница должна быть больше левой границы!')
        while True:
            T2 = input('Введите правую границу мн-ва весов(значения матрицы): ')
            if not T2.replace('-', '', 1).isdigit():
                print('Введите корректное значение!')
            else:
                if int(T2) < int(T1):
                    print('Правая граница должна быть больше левой границы!')
                else:
                    break
    while not z.isdigit():
        z = input('Введите кол-во особей > ')
        if not z.isdigit():
            print('Введите корректное значение!')
    while not k.isdigit():
        k = input('Введите кол-во поколений > ')
        if not k.isdigit():
            print('Введите корректное значение!')
    while not Pk.isdigit():
        Pk = input('Введите значение оператора кроссовера(в %) > ')
        if not Pk.isdigit():
            print('Введите корректное значение!')
    while not Pm.isdigit():
        Pm = input('Введите значение оператора мутации(в %) > ')
        if not Pm.isdigit():
            print('Введите корректное значение!')
    return int(m), int(n), int(T1), int(T2), int(z), int(k), int(Pk), int(Pm)


# Функция генерации кортежа значений и генов:
def generate_string_and_genes(m, T1, T2, n, string_):
    return [(string_[_], r(1, 255)) for _ in range(m)], \
           [((255 // n) * i + i, (255 // n) * (i + 1) + i) if i != n - 1 else ((255 // n) * i + i, 255) for i in range(n)]


# Функция для вывода информации об особи:
def print_string_and_genes(values, i, sum):
    print(f'{i + 1}-я особь (О{i+1})>', '\nЭлементы строки:', *[str(elem[0]) + '-' + str(elem[1]) for elem in values[0]], '\nГены:',
          *[str(elem[0]) + '-' + str(elem[1]) for elem in values[1]], '\nСумма генов:', *sum, '\n')

# Алгоритм образования фенотипов
def phenotype_formation(m, T1, T2, n, z, string_, create_individuals, correct_values, txt_file):
    sum_feno = []
    individuals = []
    for j in range(z):
        sum = [0 for _ in range(n)]
        if create_individuals:
            values = generate_string_and_genes(m, T1, T2, n, string_)
            # print(values)
        else:
            values = [correct_values[j]]
            values.append([((255 // n) * i + i, (255 // n) * (i + 1) + i) if i != n - 1 else ((255 // n) * i + i, 255) for i in range(n)])
            # print(values)
        #print(values[0])
        for elem in values[0]:
            for i, el in enumerate(values[1]):
                if el[0] <= elem[1] <= el[1]:
                    sum[i] += elem[0]
        # print_string_and_genes(values, j, sum)
        # Запись особей в файл ################################
        with open(txt_file, 'a') as file:
            string = f'{j + 1}-я особь (О{j+1})>\n'
            file.writelines(string)
            individuals_for_write = [str(elem[0]) + '-' + str(elem[1]) + ' ' for elem in values[0]]
            file.writelines(individuals_for_write)
            file.writelines('\nСумма генов:\n')
            file.writelines(' '.join([str(e) for e in sum]) + '\n')
        #######################################################
        sum_feno.append(sum)
        individuals.append(values[0])
    return sum_feno, individuals


# Алгоритм скрещивания особей
def crossing_individuals(m, T1, T2, n, z, string_, create_individuals, correct_values, Pk, txt_file):
    best_individual, phenotypes = phenotype_formation(m, T1, T2, n, z, string_, create_individuals, correct_values, txt_file)
    best_individual = min([max(el) for el in best_individual])
    # print(f'Минимальное из всех максимальных в этих фенотипах: {best_individual}\n')
    # Записываем лучшую загрузку среди родителей ##########
    with open(txt_file, 'a') as file:
        file.writelines(f'Минимальное из всех максимальных в этих фенотипах: {best_individual}\n')
    #######################################################
    crossed_pheno = []
    #print(*phenotypes, sep='\n')
    for i, elem in enumerate(phenotypes):
        check = deepcopy(phenotypes)
        del check[i]
        crossed_pheno.append([elem, c(check)])
    parents = deepcopy(crossed_pheno)
    T = r(1, m - 1)
    indexes = [f'(P{"".join([str(phenotypes.index(el) + 1) for el in elem])}, P{"".join([str(phenotypes.index(el) + 1) for el in elem])[::-1]})' for elem in crossed_pheno]
    # [print(f'{indexes[i]} {crossed_pheno[i]}') for i in range(z)]
    # Запись в файл ##########################################
    with open(txt_file, 'a') as file:
        file.writelines('Рандомные пары:\n')
        newline = '\n'
        [file.writelines(f'{i + 1}-я пара({" ".join([str(phenotypes.index(elem) + 1) + (s == 0) * " и" for s, elem in enumerate(crossed_pheno[i])])} особи):{newline}{"".join([" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in crossed_pheno[i][j]]) + newline for j in range(2)])}\n') for i in range(z)]
        file.writelines('T: ' + str(T) + newline*2)
    ##########################################################
    crossover_info = ['' for _ in range(z)]  # информация о том прошла ли операция кроссовера с первого раза
    for i, elem in enumerate(crossed_pheno):
        crossover_check = False
        while not crossover_check:
            if r(1, 100) <= Pk:
                elem[0], elem[1] = elem[0][:T] + elem[1][T:], elem[1][:T] + elem[0][T:]
                crossover_check = True
            else:
                crossover_info[i] = 'This was changed!\n'
                new_elem = c(phenotypes)
                if phenotypes.count(new_elem) < len(phenotypes) - 1:
                    while new_elem == c(phenotypes):
                        new_elem = c(phenotypes)
                crossed_pheno[i] = [elem[0], new_elem]
    #print(crossover_info)
    # Запись в файл ##########################################
    with open(txt_file, 'a') as file:
        newline = '\n'
        [file.writelines(f'{crossover_info[i] + "".join([" ".join([str(elem[0]) + "-" + str(elem[1]) for s, elem in enumerate(crossed_pheno[i][j])]) + newline for j in range(2)])}\n') for i in range(z)]
    ##########################################################
    # print(f'\nT : {T}\n')
    # [print(f'{indexes[i]} {crossed_pheno[i]}') for i in range(z)]
    return indexes, crossed_pheno, best_individual, parents


# Отбор детей путём создания и сортировки фенотипов:
def child_phenotype_selection(m, T1, T2, n, string_, genes):
    sum = [0 for _ in range(n)]
    values = [[(string_[_], genes[_]) for _ in range(m)],
              [(i * (255//n) + (i != 0), int(255 // (n/(i + 1)))) for i in range(n)]]
    # print(values[0])
    for elem in values[0]:
        for i, el in enumerate(values[1]):
            if el[0] <= elem[1] <= el[1]:
                sum[i] += elem[0]
                #print(sum)
    # print('Сумма генов:', *sum)
    return sum, values


def num_to_binary(value):
    binum = '00000000'
    num = value
    for j in range(len(binum)):
        binum = binum[:j] + str(num % 2) + binum[j + 1:]
        num //= 2
    binum = binum[::-1]
    return binum


# Алгоритм образования фенотипа с учетом мутация и кросинговера:
def crossover_mutation_phenotype_selection(m, T1, T2, n, z, Pk, Pm, string_, genes, txt_file):
    sum = [0 for _ in range(n)]
    new_genes = deepcopy(genes)
    # print('Производим операции кроссовера и мутации: ')
    while True:
        if r(1, 100) <= Pk:
            value = c(new_genes)
            index = new_genes.index(value)
            break
    # print(f'Гены до: {genes}')
    # print(f'Возьмём число: {value}')
    binary_num = num_to_binary(value)
    # print(f'Его двоичная форма: {binary_num}')
    # Запись в файл ########################################################################
    with open(txt_file, 'a') as file:
        file.writelines(f'Производим операции кроссовера и мутации:\nГены до: {" ".join([str(e) for e in new_genes])}\nВозьмём число: {value}\nЕго двоичная форма: {binary_num}')
        file.writelines('\n')
    ########################################################################################
    if binary_num.count('0') > 0:
        while True:
            if r(1, 100) <= Pm:
                random_num = r(0, len(binary_num) - 1)
                while binary_num[random_num] != '0':
                    random_num = r(0, len(binary_num) - 1)
                binary_num =  binary_num[:random_num] + '1' + binary_num[random_num + 1:]
                break
    # print(f'Поменяли цифру: {binary_num}')
    new_genes[index] = int(binary_num, 2)
    # Запись в файл ########################################################################
    with open(txt_file, 'a') as file:
        file.writelines(f'Поменяли цифру: {binary_num}\nИтоговое число: {new_genes[index]}')
        file.writelines('\n')
    ########################################################################################
    # print(f'Итоговое число: {genes[index]}')
    values = [[(string_[_], new_genes[_]) for _ in range(m)],
              [(i * (255 // n) + (i != 0), int(255 // (n / (i + 1)))) for i in range(n)]]
    # print('\n',values)
    for elem in values[0]:
        for i, el in enumerate(values[1]):
            if el[0] <= elem[1] <= el[1]:
                sum[i] += elem[0]
    # print(f'Гены после: {genes}')
    # print('Сумма генов (C вероятностью мутации):', *sum)
    # Запись в файл ########################################################################
    with open(txt_file, 'a') as file:
        file.writelines(f'Гены после: {" ".join([str(e) for e in new_genes])}\nСумма генов (C вероятностью мутации): {" ".join([str(e) for e in sum])}')
        file.writelines('\n' * 2)
    ########################################################################################
    return sum, values


# Алгоритм отбора особей:
def child_selection(m, T1, T2, n, z, Pk, Pm, create_individuals, correct_values, string_, txt_file):
    #string_ = [r(T1, T2) for _ in range(m)]  # генерируем строку значений
    indexes, crossed_pheno, check_sum, parents = crossing_individuals(m, T1, T2, n, z, string_, create_individuals, correct_values, Pk, txt_file)
    check_mas = []
    result_sum, result_individual = [], []
    with open(txt_file, 'a') as file:
        file.writelines(f'Дети:\n')
    for i, elem in enumerate(crossed_pheno):
        # print(f'\nCоздаём {i + 1}-ю особь({indexes[i][1:-1]} - 1-й и 2-й ребёнок соответственно): \n{indexes[i]} {elem}')
        # Запись в файл ##########################################
        with open(txt_file, 'a') as file:
            file.writelines(f'Cоздаём {i + 1}-ю особь >')
            file.writelines('\n' * 2)
        ##########################################################
        check_mas_sum = []
        check_mas = []
        for j, el in enumerate(elem):
            # print(f'{j + 1}-й ребёнок:')
            #print([e[1] for e in el])
            # Запись в файл ##########################################
            with open(txt_file, 'a') as file:
                file.writelines(
                    f'Cоздаём {j + 1}-го ребёнка:\n{" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in el])}')
                file.writelines('\n')
            ##########################################################
            sum, values = child_phenotype_selection(m, T1, T2, n, string_, [e[1] for e in el])
            # Запись в файл ##########################################
            with open(txt_file, 'a') as file:
                file.writelines(f'Сумма генов(Без учёта мутации): {" ".join([str(e) for e in sum])}')
                file.writelines('\n')
            ##########################################################
            check_mas.append(el)
            check_mas_sum.append(sum)
            #print(el)
            sum, values = crossover_mutation_phenotype_selection(m, T1, T2, n, z, Pk, Pm, string_, [e[1] for e in el], txt_file)
            #print(values)
            check_mas.append(values[0])
            #print(values[0])
            check_mas_sum.append(sum)
        # print(check_mas_sum)
        #print(check_mas)
        # print(f'Минимальное из всех максимальных в суммах: {min([max(el) for el in check_mas_sum])}')
        # print(check_mas_sum)
        check = min([max(el) for el in check_mas_sum])
        # print([max(el) for el in check_mas_sum])
        #print(check)
        #print(check_mas_sum)
        for i, elem in enumerate(check_mas_sum):
            #print(elem)
            if check == max(elem):
                new_index = i
                break
        # print(check_mas)
        # print(new_index)
        # print(f'{(new_index // 2) + 1}-й ребёнок выиграл отбор!\n{check_mas[new_index]}')
        #print()
        #print_string_and_genes(check_mas[new_index], i, sum)
        result_sum.append(min([max(el) for el in check_mas_sum]))
        #print(check_mas)
        result_individual.append(check_mas[new_index])
        #print(result_sum)
        #print(check_mas)
        # Запись в файл ########################################################################
        with open('lab_5_find_generation.txt', 'a') as file:
            file.writelines(f'Загрузки детей с учетом и без учета мутаций: {" ".join([str(e) for e in check_mas_sum])}\n'
                            f'{(new_index // 2) + 1}-й ребёнок выиграл отбор!\n{" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in check_mas[new_index]])}')
            file.writelines('\n' * 2)
        ########################################################################################
        #print(check_mas_sum)
    #print(check_mas_sum)
    #print(new_index)
    #best_individual_new = check_mas[new_index]
    return min(result_sum), check_sum, result_individual, result_sum, parents


# Создаём особей и работаем с поколениями
def genetic_algorythm(m, n, T1, T2, z, k, Pk, Pm, txt_file):
    create_individuals = True
    correct_values = []
    check_number = 0
    first_in = True
    count = 0
    generation = 0
    best_individual = []
    string_ = [r(T1, T2) for _ in range(m)]
    while count != k:
        generation += 1
        #count += 1
        # print(f'\n{generation}-Е ПОКОЛЕНИЕ > ')

        # Запись в файл ##########################################
        with open(txt_file, 'a') as file:
            file.writelines(f'{generation}-Е ПОКОЛЕНИЕ > ' + '\nРодители:\n')
        ##########################################################

        previous_best_individual_load = check_number
        # previous_best_individual = best_individual
        a, b, correct_values, best_sums, parents = child_selection(m, T1, T2, n, z, Pk, Pm, create_individuals, correct_values, string_, txt_file)
        create_individuals = False
        best_individual_index = best_sums.index(min(best_sums))
        best_individual = correct_values[best_individual_index]
        #print(f'c{correct_values}')
        #print('sss', best_sums)
        #print(correct_values[best_individual_index])
        #print(b)
        # if previous_best_individual == best_individual:
        #     count += 1
        if a > b:
            a = b
        if check_number >= a or first_in:
            first_in = False
            check_number = a
            # count = 0
            # count += 1
        if previous_best_individual_load == check_number:
            # print(previous_best_individual_load)
            count += 1
        else:
            count = 0
        # print(f'Лучшая особь: {best_individual}')
        # print(f'Новые значения: {correct_values}')
        # print(f'Максимальные суммы из фенотипов: {best_sums}')
        # print(f'Лучшая загрузка особи в этом поколении: {a}\nЛучшая загрузка особи по результату всех поколений: {check_number}')
        # for elem in values[0]:
        #     for i, el in enumerate(values[1]):
        #         if el[0] <= elem[1] <= el[1]:
        #             sum[i] += elem[0]
        sum_parents = []
        # sum = [0 for _ in range(n)]
        # Загрузка родителей:
        for elements in parents[best_individual_index]:
            sum = [0 for _ in range(n)]
            #print(elements)
            for elem in elements:
                for i, el in enumerate([(i * (255//n) + (i != 0), int(255 // (n/(i + 1)))) for i in range(n)]):
                    if el[0] <= elem[1] <= el[1]:
                        sum[i] += elem[0]
            sum_parents.append(sum)
        #print(sum_parents)
        # Загрузка лучшей особи:
        sum_individual = [0 for _ in range(n)]
        for elem in best_individual:
            for i, el in enumerate([(i * (255 // n) + (i != 0), int(255 // (n / (i + 1)))) for i in range(n)]):
                if el[0] <= elem[1] <= el[1]:
                    sum_individual[i] += elem[0]
        #print(count, sum_individual)
        # Запись в файл ##########################################
        with open(txt_file, 'a') as file:
            newline = '\n'
            file.writelines(f'Лучшая особь в поколении - ({best_individual_index + 1}-я): {" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in best_individual])}\nЗагрузка особи: {sum_individual}\nЛучшая загрузка особи в этом поколении: {a}\nЕё родители из {best_individual_index + 1}-й пары!\n'
                            f'Родители:\n{newline.join([" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in e]) + newline + f"Загрузка {i + 1}-го родителя: " + " ".join([str(el) for el in sum_parents[i]]) for i, e in enumerate(parents[best_individual_index])])}\n'
                            f'\nОсоби прошедшие отбор:\n{str(newline).join([" ".join([str(elem[0]) + "-" + str(elem[1]) for elem in e]) for e in correct_values])}\n'
                            f'Максимальные суммы из загрузок детей: {" ".join([str(e) for e in best_sums])}\n'
                            f'Лучшая загрузка особи по результату всех поколений: {check_number}\n#\n\n')
        ##########################################################
    print(f'\nВсего поколений: {generation}')
    print(f'Ответ: {check_number}')
    # Запись в файл ##########################################
    with open(txt_file, 'a') as file:
        file.writelines(f'Всего поколений: {generation}\nОтвет: {check_number}\n')
    ##########################################################
    return generation


# Очищаем txt файл от ненужных данных
def clear_file(txt_file):
    f = open(txt_file, 'w')
    f.close()


# Выводим нужное поколение
def show_generation(txt_file, amount_of_generations):
    with open(txt_file, 'r') as file:
        while True:
            file.seek(0)
            while True:
                num = input('Выберите какое поколение вывести (exit - чтобы выйти) > ')
                if num.isdigit() and 0 < int(num) <= amount_of_generations or num == 'exit':
                    chosen_generation = f"{num}-Е ПОКОЛЕНИЕ > \n"
                    break
                else:
                    print('Некорректный ввод!')
                chosen_generation = f"{num}-Е ПОКОЛЕНИЕ > \n"
            print()
            if num == 'exit':
                break
            generation_tree_data = file.readlines()
            new_slice = generation_tree_data[generation_tree_data.index(chosen_generation):]
            this_generation = new_slice[:new_slice.index('#\n')]
            print("".join(this_generation))
        print('Всего хорошего!')


if __name__ == "__main__":
    # Файл в который мы выгрузим всё наше генетическое древо:
    txt_file = 'lab_5_find_generation.txt'
    # Вводим и проверяем на валидность значения:
    m, n, T1, T2, z, k, Pk, Pm = input_values(m='11', n='4', T1='10', T2='19', z='10', k='10', Pk='87', Pm='88')
    # Очищаем txt файл от ненужных данных
    clear_file(txt_file)
    # Запускаем алгоритм
    amount_of_generations = genetic_algorythm(m, n, T1, T2, z, k, Pk, Pm, txt_file)
    # Вывод данных из нужного поколения
    show_generation(txt_file, amount_of_generations)
