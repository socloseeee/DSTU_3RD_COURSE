import matplotlib.pyplot as plt
import networkx as nx
from random import randint as r, choice as c, uniform as u
from copy import deepcopy


# Создаём граф
def create_graph(n):
    matrix = [[0 for __ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i != j:
                value = round(u(T1, T2), 2)  # round(u(T1, T2), 2) - x,xx (x - num)
                while True:                  # r(T1, T2) - x (x - num)
                    value = round(u(T1, T2), 2)
                    if value not in matrix[i] and value not in matrix[j]:
                        break
                matrix[i][j] = value
                matrix[j][i] = value
    return matrix


# Жадный алгоритм (Метод Критического Пути):
def greedy_algorithm(n, chosen_city):
    city_checked, weights, i, next = [chosen_city], [], 0, True
    while len(city_checked) != n:
        if next:
            copy_point = deepcopy(graph_matrix[i])  # копируем пути из i-й точки
            copy_point.remove(0)  # удаляем 0 чтобы выявить минимальный элемент
        value = graph_matrix[i].index(min(copy_point)) + 1
        if value in city_checked or value == chosen_city:
            next = False
            copy_point.remove(min(copy_point))
        else:
            city_checked.append(value)
            i = value - 1
            next = True
    city_checked.append(chosen_city)
    from_, to_ = 0, 0
    for i in range(len(city_checked)-1):
        from_, to_ = city_checked[i], city_checked[i+1]
        weights.append(graph_matrix[from_-1][to_-1])
    return city_checked, weights


# Формируем пути(особей):
def create_individuals(n, chosen_city):
    city_checked, weights, i, next = [chosen_city], [], chosen_city-1, True
    while len(city_checked) != n:
        cities = [i for i in range(1,n+1)]
        value = r(1,n)
        while True:
            if value in city_checked:
                value = c(cities)
                cities.remove(value)
            else:
                break
        weights.append(graph_matrix[i][value - 1])
        city_checked.append(value)
        i = value - 1
    city_checked.append(chosen_city)
    weights.append(graph_matrix[city_checked[-2] - 1][city_checked[0] - 1])
    return city_checked, weights


# Считаем путь:
def count_the_way(path_length):
    return sum(path_length)


# Кроссовер(одноточечный):
def crossover(parent1, parent2):
    T = r(1, len(parent1[0]) - 1)
    parent1_path, parent1_weights = parent1
    parent2_path, parent2_weights = parent2
    child1_path, child2_path = parent1_path[:T] + parent2_path[T:], parent2_path[:T] + parent1_path[T:]
    index1, index2 = [], []
    for i in range(len(parent1[0])):
        if child1_path.count(i + 1) > 1 and i + 1 != parent1_path[0]:
            index = child1_path[::-1].index(i + 1)
            index1.append(len(parent1[0]) - index - 1)
            child1_path[::-1].remove(child1_path[index])
        if child2_path.count(i + 1) > 1 and i + 1 != parent2_path[0]:
            index = child2_path[::-1].index(i + 1)
            index2.append(len(parent1[0]) - index - 1)
            child2_path[::-1].remove(child2_path[index])
    child1_path = child1_path[:-1]
    child2_path = child2_path[:-1]
    last1, last2 = child1_path[-1], child2_path[-1]
    child1_added, child2_added = [], []  # добавляем точки для последующего рассчёта весов
    for elem in [el for el in range(1, len(parent1[0]))]:
        if elem != parent1[0][0] and elem not in child1_path:
            child1_added.append(elem)
            child1_path.append(elem)
    child1_path.append(parent1[0][0])
    for elem in [el for el in range(1, len(parent1[0]))]:
        if elem != parent1[0][0] and elem not in child2_path:
            child2_added.append(elem)
            child2_path.append(elem)
    child2_path.append(parent1[0][0])
    for elem in child1_path:
        if child1_path.count(elem) > 1 and elem != city:
            child1_path = child1_path[::-1]
            while child1_path.count(elem) > 1:
                child1_path.remove(elem)
            child1_path = child1_path[::-1]
    for elem in child2_path:
        if child2_path.count(elem) > 1 and elem != city:
            child2_path = child2_path[::-1]
            while child2_path.count(elem) > 1:
                child2_path.remove(elem)
            child2_path = child2_path[::-1]
    # Веса
    child1_weights, child2_weights = [graph_matrix[child1_path[i]-1][child1_path[i+1]-1] for i in range(len(child1_path)-1)], [graph_matrix[child2_path[i]-1][child2_path[i+1]-1] for i in range(len(child2_path)-1)]
    return ((child1_path, child1_weights), (child2_path, child2_weights)), T


# Мутация:
def mutation(child, Pm):
    path, weights = deepcopy(child)
    if Pm > r(1, 100):
        index1 = r(1, len(path) - 2)
        index2 = r(1, len(path) - 2)
        while index2 == index1:
            index2 = r(1, len(path) - 2)
        if index1 > index2:
            index1, index2 = index2, index1
        path[index1], path[index2] = path[index2], path[index1]
    weights = [graph_matrix[path[i] - 1][path[i + 1] - 1] for i in range(len(path) - 1)]
    return path, weights


# Выводим нужное поколение
def show_generation(txt_file, amount_of_generations):
    with open(txt_file, 'r') as file:
        while True:
            file.seek(0)
            while True:
                num = input('Вывести поколение (input num to show generation/exit - to quit programm) > ')
                if num.isdigit() and 0 <= int(num) <= amount_of_generations or num == 'exit':
                    chosen_generation = f"Поколение {num}:\n"
                    break
                else:
                    print('Incorrect input!')
                chosen_generation = f"Поколение {num}:\n"
            print()
            if num == 'exit':
                break
            generation_tree_data = file.readlines()
            new_slice = generation_tree_data[generation_tree_data.index(chosen_generation):]
            this_generation = new_slice[:new_slice.index('#\n')]
            print("".join(this_generation))
        print('Good Bye!')


# Входные данные задачи Коммивояжёра:
n = 8  # Кол-во точек
T1 = 10  # Разброс весов (левая граница)
T2 = 25  # Разброс весов (правая граница)
k = 10  # Кол-во поколений подряд при котором лучшая загрузка будет повторяться k-раз
z = 10 # Кол-во путей (особей)
Pk = 92  # Вероятность кроссовера
Pm = 93  # Вероятность мутации

# Открываем файл для записи:
txt_file = 'lab7.txt'
f = open(txt_file, 'w')

# Матрица путей:
graph_matrix = create_graph(n)
print('Матрица смежности (без петель):')
[print(*[str(el).ljust(5) for el in elem]) for elem in graph_matrix]

# Граф:
A=nx.Graph()
[A.add_node(_+1) for _ in range(n)]
[[A.add_edge(i+1, j+1, weight=[graph_matrix[j][i]]) for j in range(n) if i != j] for i in range(n)]
edges = A.edges()
nx.draw(A, pos=nx.circular_layout(A), with_labels=True, node_size=300)
labels = nx.get_edge_attributes(A,'weight')
if n <= 8:
    nx.draw_networkx_edge_labels(A, pos=nx.circular_layout(A), edge_labels=labels, label_pos=0.37)
plt.savefig("Граф.png")
plt.show()

# Выбираем город
city = input('Выберите город из которого выйдет коммивояжёр > ')
while not city.isdigit() or city not in (str(elem) for elem in range(1, n+1)):
    print('Некорректный ввод!')
    city = input('Выберите город из которого выйдет коммивояжёр > ')
city = int(city)

# Создаём путь методом жадного алгоритма (Метод Критического Пути):
greedy_path, weights = greedy_algorithm(n, city)
greedy_best = round(sum(weights), 2)
greedy_path_pairs = [(greedy_path[i], greedy_path[i+1]) for i in range(len(greedy_path)-1)]
print(f'\nЖадный Алгоритм >\nЛучшая длина пути (Жадный Алгоритм): {greedy_best}')
print(f'Лучший путь(Жадный Алгоритм): {"->".join([str(elem) for elem in greedy_path])} | {"->".join([str(elem) for elem in weights])}')
# Запись данных файл для последующего отображения:
f.write('Жадный алгоритм(Метод Критического Пути) >\n')
f.write(f'Путь: {"->".join([str(elem) for elem in greedy_path])}\nВес пути: {"+".join([str(elem) for elem in weights])}={greedy_best}\n&\n')


# Формируем граф и отрисовываем граф(Для жадного алгоритма - МКП):
plt.figure(figsize=(13, 6))
plt.subplot(122)
G=nx.Graph()
[G.add_node(_+1) for _ in range(n)]
[[G.add_edge(i+1, j+1,color='g', weight=[graph_matrix[j][i]]) if (i+1, j+1) not in greedy_path_pairs and (j+1, i+1) not in greedy_path_pairs else G.add_edge(i+1, j+1, color='r', weight=[graph_matrix[j][i]]) for j in range(n) if i != j] for i in range(n)]
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
nx.draw(G, pos=nx.circular_layout(G), edge_color=colors, with_labels=True, node_size=300)
labels = nx.get_edge_attributes(G,'weight')
if n <= 8:
    nx.draw_networkx_edge_labels(G,pos=nx.circular_layout(G), edge_labels=labels, label_pos=0.37)
plt.text(-0.66, -1.4, f'Метод Критического Поиска\n                Длина пути: {greedy_best}', family='fantasy', color='red', size=15)
#plt.savefig("Методом Критического Поиска.png")

# Формируем рандомные пути(особи) для Модели Голдберга(0 - поколение):
individuals = [create_individuals(n, city) for _ in range(z)]
newline = "\n"
all_path_length = [count_the_way(individual[1]) for individual in individuals]
best_result = min(all_path_length)
# Если лучший путь в 0 поколении хуже, то берем результат Жадного Алгоритма, иначе результат Голдберга из 0-го
best_of_all_generations_result = best_result if best_result > greedy_best else greedy_best
# Запись данных файл для последующего отображения:
f.write(f'\nАлгоритмом Голдберга(Методом Голдберга) >\nПоколение 0:\nВсе пути(особи):\n{newline.join([f"{i+1}) " + "->".join([str(el) for el in elem[0]]) + " | " + "->".join([str(el) for el in elem[1]]) for i, elem in enumerate(individuals)])}\n')
f.write(f'Их длины: {all_path_length}\n')
f.write(f'Лучший путь({all_path_length.index(min(all_path_length)) + 1}): {"->".join([str(elem) for elem in individuals[all_path_length.index(min(all_path_length))][0]])} | {"->".join([str(elem) for elem in individuals[all_path_length.index(min(all_path_length))][1]])}')
f.write(f'\nЕго длина: {best_result}\n#\n\n')

# Переменные для ГА:
counter, generation_count = 0, 0

while k != counter:
    previous_best_result = best_result
    generation = []
    generation_count += 1
    # Запись данных файл для последующего отображения:
    f.write(f'Поколение {generation_count}:\nПотенциальные родители:\n'
            f'{newline.join([f"{i + 1}) " + "->".join([str(el) for el in elem[0]]) + " | " + "->".join([str(el) for el in elem[1]]) for i, elem in enumerate(individuals)])}\n\n')
    for _ in range(z):
        # Алгоритм образования пар родителей:
        parent1 = individuals[_]
        individuals_no_repeat = deepcopy(individuals)
        individuals_no_repeat.remove(parent1)  # дабы избежать попадание рандома на первого
        parent2 = c(individuals_no_repeat)
        while r(0, 100) <= Pk:
            parent2 = c(individuals_no_repeat)

        # Алгоритм отбора детей из потенциальных особей (2 + 2 мутанта)
        goldberg_selection = []
        load_list = []
        counter_child = 0
        crossover_result, T = crossover(parent1, parent2)
        # Запись данных файл для последующего отображения:
        f.write(f'Отбор {_+1}-й особи >\n'
                f'Формируем пары родителей для последующей генерации детей:\n'
                f'1-й родитель({_+1}-особь): '
                f'{"->".join([str(elem) for elem in parent1[0]])} | {"->".join([str(elem) for elem in parent1[1]])}\n'
                f'2-й родитель({individuals.index(parent2)+1}-я особь): '
                f'{"->".join([str(elem) for elem in parent2[0]])} | {"->".join([str(elem) for elem in parent2[1]])}\n'
                f'Кроссовер при T={T}:\n'
                f'Потенциальные дети:\n{newline.join([f"{i + 1}) " + "->".join([str(el) for el in child[0]]) + " | " + "->".join([str(el) for el in child[1]]) for i, child in enumerate(crossover_result)])}\n')
        for i, child in enumerate(crossover_result):
            usual_child, usual_weights = child
            goldberg_selection.append(usual_child)
            load_list.append(usual_weights)
            muted_child, muted_weights = mutation(child, Pm)
            goldberg_selection.append(muted_child)
            load_list.append(muted_weights)
            # Запись данных файл для последующего отображения:
            f.write(f'{i+1}-й ребёнок без мутации: {"->".join([str(elem) for elem in usual_child])} | {"->".join([str(elem) for elem in usual_weights])}\n'
                    f'{i+1}-й ребёнок с мутацией: {"->".join([str(elem) for elem in muted_child])} | {"->".join([str(elem) for elem in muted_weights])}\n')
        goldberg_selection.append(parent1[0])
        load_list.append(parent1[1])
        best_load = min([count_the_way(elem) for elem in load_list])
        best_index = [count_the_way(elem) for elem in load_list].index(best_load)
        best_individual_now = (goldberg_selection[best_index], load_list[[count_the_way(elem) for elem in load_list].index(best_load)])
        generation.append(best_individual_now)
        # Запись данных файл для последующего отображения:
        f.write(f'Загрузка особей детей + родителя (4+1): {[count_the_way(elem) for elem in load_list]}\n')
        if best_index == 0:
            f.write(f'1-й ребёнок (без мутации) победил!\n')
        elif best_index == 1:
            f.write(f'1-й ребёнок (с мутацией) победил!\n')
        elif best_index == 2:
            f.write(f'2-й ребёнок (без мутации) победил!\n')
        elif best_index == 3:
            f.write(f'2-й ребёнок (с мутацией) победил!\n')
        else:
            f.write(f'Особь родителя выиграла в отборе!\n')
        f.write(f'\n')
    # Выводим лучший путь в поколении:
    best_result = min([count_the_way(elem[1]) for elem in generation])
    best_index = [count_the_way(elem[1]) for elem in generation].index(min([count_the_way(elem[1]) for elem in generation]))
    best_individual_of_generation = generation[best_index]

    # Если сквозь поколения была лучшая загрузка ждем когда она не повторится или улучшится:
    if best_result < best_of_all_generations_result:
        best_of_all_generations_result = best_result
        counter = 0

    # Если загрузка предыдущего поколения равна загрузке текущего
    if best_result == previous_best_result:
        counter += 1
    else:
        counter = 0

    # Копируем поколение для того чтоб они были родителями в будущем:
    individuals = generation

    # Запись данных файл для последующего отображения:
    f.write(f'Особи прошедшие отбор:\n{newline.join([f"{i + 1}) " + "->".join([str(el) for el in elem[0]]) + " | " + "->".join([str(el) for el in elem[1]]) for i, elem in enumerate(individuals)])}\n'
            f'Лучший путь в поколении: {best_result}\n'
            f'#\n\n')
f.close()
#plt.show()

# Округляем лучший результат по Голдбергу до x,xx (x - num)
best_result = round(best_result, 2)

print(f'\nМетод Голдберга >\nПоколений: {generation_count}\nЛучшая длина пути(Метод Голдберга): {best_result}\n'
      f'Лучший путь(Метод Годберга): {"->".join([str(elem) for elem in best_individual_of_generation[0]])} | {"->".join([str(elem) for elem in best_individual_of_generation[1]])}')

# Формируем граф и отрисовываем граф(Для Метода Голдберга - МГ):
best_of_goldberg_pairs = [(best_individual_of_generation[0][i], best_individual_of_generation[0][i+1]) for i in range(len(best_individual_of_generation[0])-1)]
plt.subplot(121)
Z=nx.Graph()
[Z.add_node(_+1) for _ in range(n)]
[[Z.add_edge(i+1, j+1,color='g', weight=[graph_matrix[j][i]]) if (i+1, j+1) not in best_of_goldberg_pairs and (j+1, i+1) not in best_of_goldberg_pairs else Z.add_edge(i+1, j+1, color='b', weight=[graph_matrix[j][i]]) for j in range(n) if i != j] for i in range(n)]
edges = Z.edges()
colors = [Z[u][v]['color'] for u,v in edges]
nx.draw(Z, pos=nx.circular_layout(Z), edge_color=colors, with_labels=True, node_size=300)
labels = nx.get_edge_attributes(Z,'weight')
if n <= 8:
    nx.draw_networkx_edge_labels(Z,pos=nx.circular_layout(Z), edge_labels=labels, label_pos=0.37)
plt.text(-0.42, -1.4, f'Метод Голдберга\n    {generation_count} поколений\n   Длина пути: {best_result}', family='fantasy', color='blue', size=15)
plt.savefig("Коммивояжёр.png")
plt.show()

show_generation(txt_file, generation_count)
