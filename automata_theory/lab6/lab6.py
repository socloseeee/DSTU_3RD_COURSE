from prettytable import PrettyTable
from copy import deepcopy


def beautiful_table(head, values):
    columns = len(head)  # Подсчитаем кол-во столбцов на будущее.
    table = PrettyTable(head)  # Определяем таблицу.
    # Cкопируем список td, на случай если он будет использоваться в коде дальше.
    td_data = values[:]  # Входим в цикл который заполняет нашу таблицу. Цикл будет выполняться до тех пор пока
    # у нас не кончатся данные для заполнения строк таблицы (список td_data).
    while td_data:
        table.add_row(td_data[:columns])  # Используя срез добавляем первые три элементов в строку (columns = 3).
        td_data = td_data[columns:]  # Используя срез переопределяем td_data так, чтобы он
        # больше не содержал первых 3 элементов.

    print(table)  # Печатаем таблицу


def p_check(graph, p_points):
    p_in = set()
    p_in.add('P0')
    for key, value in graph.items():
            for elem in value:
                if elem[:2] not in p_in:
                    p_in.add(elem[:2])
    count = 0
    while len(p_in) != len(graph):
        if p_points[count] not in p_in:
            del graph[p_points[count]]
        count += 1
    return graph


def index(p_class, graph):
    index = [[], []]
    for _ in (0, 1):
        for i, class_ in enumerate(p_class):
            index[_].append([])
            for k, elem in enumerate(class_):
                for j, check_class in enumerate(p_class):
                    if graph[elem][_][:2] in check_class:
                        # print(j)
                        index[_][i].append(j)
    return index


def minimi (p_class, graph):
    classes, last_classes, enumerator  = p_class, [], 1
    while classes != last_classes:
        new_class = []
        index_ = index(classes, graph)
        # print(index_)
        count = 0
        for _ in (0, 1):
            new_class.append([])
            for i, class_ in enumerate(classes):
                # print(f'class_: {class_}')
                set_ = set()
                for k, elem in enumerate(class_):
                    # print(f'class_: {elem}', f'index: {index_[_][i][k]}')
                    set_.add(index_[_][i][k])
                # print(set_)
                set_ = list(set_)
                for o, el in enumerate(set_):
                    new_class[_].append([])
                    for k, elem in enumerate(class_):
                        if el == index_[_][i][k]:
                            new_class[_][count].append(elem)
                    count += 1
            count = 0
        new_class = [[set(elem) for elem in new_class[_]] for _ in (0, 1)]
        last_classes = classes
        classes = []
        #print(new_class)
        for elem in new_class[0]:
            for el in new_class[1]:
                 if len(el & elem) != 0:
                    classes.append(el & elem)
        print(f'≡{enumerator} {classes}')
        classes = [sorted(elem) for elem in classes]
        #print(f'≡{enumerator} {classes}')
        enumerator += 1
    return classes



if __name__ == "__main__":

    # Bogdan
    alphabet = 'ab'
    p_connections = {
                     'P0': ['P1:a', 'P4:b'],
                     'P1': ['P4:a', 'P2:b'],
                     'P2': ['P5:a', 'P3:b'],
                     'P3': ['P3:a', 'P5:b'],
                     'P4': ['P4:a', 'P2:b'],
                     'P5': ['P3:a', 'P5:b'],
                     'P6': ['P3:a', 'P5:b']
                     }
    endpoints = 'P3 P5 P6'

    # Masha
    # alphabet = '01'
    # p_connections = {
    #     'P0': ['P1:0', 'P4:1'],
    #     'P1': ['P2:0', 'P1:1'],
    #     'P2': ['P3:0', 'P2:1'],
    #     'P3': ['P3:0', 'P2:1'],
    #     'P4': ['P5:0', 'P6:1'],
    #     'P5': ['P2:0', 'P1:1'],
    #     'P6': ['P2:0', 'P5:1'],
    #     'P7': ['P3:0', 'P6:1']
    # }
    # endpoints = 'P2 P3 P7'

    print('ГРАФ:')
    print(*[key + ': [' + ', '.join(value) + ']' for key, value in p_connections.items()], sep='\n')

    th = ['P', alphabet[0], alphabet[1]]
    td = []
    for key, value in p_connections.items():
        if key in endpoints:
            td.append('(final)' + key)
        else:
            td.append(key)
        for elem in value:
            td.append(elem)
    beautiful_table(th, td)

    p_points = [elem for elem in p_connections]

    print('Удаляем вершины в которые мы не можем прийти.')

    p_check(p_connections, p_points)

    th = ['P', alphabet[0], alphabet[1]]
    td = []
    for key, value in p_connections.items():
        if key in endpoints:
            td.append('(final)' + key)
        else:
            td.append(key)
        for elem in value:
            td.append(elem)
    beautiful_table(th, td)

    print('Решение:')
    class_p = [set() for _ in range(2)]
    for key, value in p_connections.items():
        if key in endpoints:
            class_p[0].add(key)
        else:
            class_p[1].add(key)
    print('≡0', class_p)
    class_p = [sorted(elem) for elem in class_p]
    #print(class_p)

    minimized_automata = minimi(class_p, p_connections)

    th = ['P', alphabet[0], alphabet[1]]
    td = []

    print('Минимизированный автомат:')

    # Cтроим словарь для объединения точек в будущем
    new_points = {}
    for elem in minimized_automata:
        #print(elem)
        if len(elem) > 1:
            mas = []
            for el in elem:
                #print(el, p_connections[el])
                for e in p_connections[el]:
                    if el == e[:2]:
                        #mas.append(elem[0] + ':' + e[-1])
                        mas.append(e)
            #print(elem)
            for el in elem:
                for e in p_connections[el]:
                    if e[:2] not in elem:
                        #print(e)
                        mas.append(e)
            mas = set(mas)
            mas = list(mas)
            new_points[''.join(elem)] = mas
    # print(new_points)

    # Массив для проверки точек
    points = [[elem[e:e + 2] for e in range(0, len(elem), 2)] for elem in new_points]
    new_del_points = []
    for elem in points:
        for el in elem:
            new_del_points.append(el)
    # print(new_del_points)

    # Компануем данные для отрисовки
    for elem in p_connections:
        if elem not in new_del_points:
            td.append(elem)
            for el in p_connections[elem]:
                #print(el)
                if el[:2] not in new_del_points:
                    td.append(el[:2])
                else:
                    for e in new_points:
                        #print([e[s:s+2] for s in range(0, len(e), 2)])
                        if el[:2] in [e[s:s+2] for s in range(0, len(e), 2)]:
                            #print(e + el[:-2])
                            #td.append(e + ':' + el[-1])
                            td.append(e)
    for elem in new_points:
        # td.append(elem)
        #print([elem[el:el + 2] for el in range(0, len(elem), 2)])
        for el in [elem[el:el + 2] for el in range(0, len(elem), 2)]:
            if el in endpoints.split(' '):
                td.append('(final)' + elem)
                break
            else:
                td.append(elem)
                break
        for el in new_points[elem]:
            #print(el)
            if el[:2] not in new_del_points:
                td.append(el[:2])
            else:
                for e in new_points:
                    # print([e[s:s+2] for s in range(0, len(e), 2)])
                    if el[:2] in [e[s:s + 2] for s in range(0, len(e), 2)]:
                        # print(e + el[:-2])
                        #td.append(e + ':' + el[-1])
                        td.append(e)
    #print(td)
    #print(endpoints.split(' '))

    beautiful_table(th, td)
