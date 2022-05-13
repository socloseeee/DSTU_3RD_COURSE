from prettytable import PrettyTable
from copy import deepcopy


# Отрисовка данных в виде таблицы:
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


# Расшифровка грамматики:
def grammar_deciphering(Grammar):
    N, T, P, S = Grammar[1:len(Grammar)-1].split(', ')
    N = N[1: len(N)-1].split(',')
    T = T[1: len(T)-1].split(',')
    return N, T, S


# Функция для определения финальных точек и сбора данных для таблицы:
# Примечание слово final формата: eng(fin)ru(а)eng(al) т.к. при последующей работе с данными возникали неполадки
def literal_parsing(P, N):
    finals = set()
    new_points, count = [], 0
    solo_non_terminals = []
    check = []
    for i, elem in enumerate(P):
        left, right = elem.split(' -> ')
        right = [right] if right.count('|') == 0 else right.split('|')
        for el in right:
            if left not in finals:
                if el not in N and len(el) == 1 and right.count(el) == 1 and el != chr(949):
                    if el not in solo_non_terminals:
                        count += 1
                        new_points.append(f'N{count}')
                        solo_non_terminals.append(el)
                        #print(solo_non_terminals)
                    else:
                        new_points.append(f'N{count}')
                if el == 'ε':
                    finals.add(left)
                    break
                if el.find(f'{left}') != -1 and len(el) == 2 and el[el.find(f'{left}')-1] in right:
                    finals.add(left)
                    break
    Z = [''.join([symbol if symbol not in finals else symbol.replace(symbol, '(finаl)' + symbol) for symbol in elem]) for elem in P]
    left_data, right_data = [], []
    #print(new_points)
    for elem in Z:
        left, right = elem.split(' -> ')
        right = [right] if right.count('|') == 0 else right.split('|')
        left_data.append(left)
        right_data.append(right)
    new_check = ''
    if len(new_points) > 0:
        for elem in new_points:
            if elem != new_check:
                new_check = elem
                left_data.append('(final)' + elem)
                N.append(elem)
                right_data.append([])
    count = 0
    for i, elem in enumerate(right_data):
        for j, el in enumerate(elem):
            if len(solo_non_terminals) > 0:
                for symbol in solo_non_terminals:
                    if symbol in el and len(el) == 1:
                        right_data[i][j] = symbol + new_points[count]
                        count += 1
    #print(right_data, left_data, N)
    return left_data, right_data, N


# Грамматика <N(Нетерминальные), T(Терминальные), P(Правила вывода), S(Начальный литерал)>
print('Юникод символы: ε·⟂')
#G = input('Введите грамматику G > ')
# Мой вариант(14)
G = '<{X,Y,Z,K}, {a,b,·,!,1,0}, P, X>'  # Формат: <N,пробелT,пробелP,пробелX>
# Вариант Маши(11)
#G = '<{S,A,B,C,D,E}, {a,b,c,d,e,#,$,⟂}, P, S>'
# Вариант Никиты(10)
#G = '<{I,J,K,M,N}, {0,1,~,!}, P, I>'
# Вариант Стаси(6)
#G = '<{E,A,B,C,D}, {0,1,a,b,c}, P, E>'
# Вариант Димы(5)
G = '<{K,L,M,N,Q,P,R,S}, {0,1,*,$,/}, V, K>'

# Считали грамматику:
N, T, S = grammar_deciphering(G)
#P = [elem + ' -> ' + input(f'Введите P({elem}) > ') for elem in N]
# Мой вариант(14)
P = ['X -> !Y|ε', 'Y -> ·Z|·K', 'Z -> aZ|bZ|a|b', 'K -> 0K|1K|0|1']  # Тест
# Вариант Маши(11)
#P = ['S -> aA|bB|cC', 'A -> dD', 'B -> #D|$E', 'D -> dD|dB|⟂', 'C -> cE', 'E -> eE|eB|⟂']
# Вариант Никиты(10)
#P = ['I -> 0J|1K|0M', 'J -> ~K|0M', 'K -> ~M|0J|0N', 'M -> 1K|!', 'N -> 0I|1I|!']
# Вариант Стаси(5)
#P = [f'E -> 0A|{chr(949)}', 'A -> aB|aD', 'B -> bB|1C|c', 'D -> aD|0C|c', 'C -> 0C|1C|c']
# Вариант Димы(6)
P = ['K -> 1L|0N', 'L -> 0M|0P|/Q', 'N -> 1R|1M|*S', 'Q -> 1P', 'P -> *L|$', 'M -> $', 'S -> 0R', 'R -> /N|$']

# Считываем и разделяем левые и правые части P:
left, right, N = literal_parsing(P, N)
#print(f'left: {left}\nright: {right}')
print(f'Финальные состояния: {", ".join([el[-1] if el[-1].isalpha() else el[-2:] for el in left if "final" in el])}')

# Строим таблицу и словарь связей:
print('Таблица связей автомата:')
dict = {elem: [] for elem in N}
th = ['']
td = []
[th.append(elem) for elem in T]
for i, elem in enumerate(right):  # elem = ['!Y', 'ε']
    td.append(left[i])
    for t in T:
        value = ''
        for el in elem:
            if t in el and len(el) > 1 and el[-1] not in value and el[0] == t:
                if el[-1].isalpha():
                    value += el[-1]
                else:
                    value += el[-2:]
        if value == '':
            value = chr(909)
            if left[i][-1].isalpha():
                dict[left[i][-1]].append(chr(909))
            else:
                dict[left[i][-2:]].append(chr(909))
        else:
            if left[i][-1].isalpha():
                dict[left[i][-1]].append(value)
            else:
                dict[left[i][-2:]].append(value)
        td.append(value)
        #print(elem, td)
beautiful_table(th, td)

# Детерминизируем автомат >
print('Детерминизированный автомат:')
# Создаём P - точки и P - алфавит(для последующего использования и перевода в P - таблице):
P_sets = [N[0]]
[P_sets.append(elem) for elem in td if '(finаl)' not in elem and elem not in (' ', '', chr(909)) and elem not in P_sets and 'final' not in elem]
P_points = [f'P{i}={"{" + ",".join(list(elem)) + "}"}' if 'N' not in elem else f'P{i}={"{" + elem + "}"}' for i, elem in enumerate(P_sets)]
p_dict = {elem: f'P{i}' for i, elem in enumerate(P_sets)}


# Cтроим таблицу для детерминизированного автомата:
th = ['']
td = []
[th.append(elem) for elem in T]
for i, elem in enumerate(P_sets):
    td.append(P_points[i])
    for j in range(len(T)):
        value = ''
        for el in elem:
            #print(elem)
            if elem != 'N1' and elem != 'N2' and elem != 'N3' and el.isalpha() and el not in 'final':
                if dict[el][j] != chr(909):
                    value += dict[el][j]
        if value in p_dict:
            value = p_dict[value]
        else:
            if len(value) > 0:
                new_value, word, count = '', '', 0
                while count != len(value):
                    word += value[count]
                    if word in p_dict and p_dict[word] not in new_value:
                        new_value += p_dict[word]
                        word = ''
                    count += 1
                value = new_value
                #print(value)
            else:
                value = chr(909)
        #print(value)
        td.append(value)
beautiful_table(th, td)
