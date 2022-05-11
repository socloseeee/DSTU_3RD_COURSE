from random import choice as c
from copy import deepcopy


# Правило вывода
def inference_rule(grammar):
    if grammar.find('^') != -1:
        grammar, bound = grammar[1:len(grammar)-1].split('|')  # Отделяем выражение и условие степени

        # Извлекаем T:
        copy_grammar = deepcopy(grammar)
        T = ''
        count = 0
        while copy_grammar != '':
            count += 1
            T += copy_grammar[:copy_grammar.find("^")]
            if copy_grammar.count('^') != 0:
                copy_grammar = copy_grammar[copy_grammar.find("^") + 2:]
            else:
                break
        T += grammar[-1] if grammar[-2] != '^' else grammar[grammar.rfind('^') + 2:]

        # Выбираем N:
        copy_T = list(deepcopy(T))
        N = ['S']
        for i in range(grammar.count('^')):
            if len([elem for elem in T if elem.isalpha()]) > 0:  # T содержит буквы/цифры?
                elem = c(copy_T).upper()
            else:
                elem = c(copy_T)
            N.append(elem)
            copy_T.remove(elem.lower())
        N = ''.join(N)

        # Правило вывода P:
        copy_grammar = deepcopy(grammar)
        P, next = '', 0
        while copy_grammar != '':
            P += copy_grammar[:copy_grammar.find("^")]
            if copy_grammar.count('^') != 0:
                P += N[-1 + next]
                copy_grammar = copy_grammar[copy_grammar.find("^") + 2:]
                next -= 1
            else:
                break
        P += grammar[-1] if grammar[-2] != '^' else grammar[grammar.rfind('^') + 2:]

        print(f'P: S -> {P}, {", ".join([letter + f"-> {chr(949)}" for letter in N[1:]])} ', end='')
        print(f'\nT: {T}\nN: {N}')

        return P, [letter + f'-> {chr(949)}' for letter in N[1:]], T, N
    elif grammar.find('...') != -1:
        grammar, bound = grammar[1:len(grammar) - 1].split('|')  # Отделяем выражение и условие степени

        # Извлекаем T:
        T = bound[bound.find('{'):][1:]
        T = ''.join([letter for letter in T[:-1] if letter.isalnum()])

        # Выбираем N:
        copy_T = list(deepcopy(T))
        N = ['S']
        N.append(grammar[0].upper())
        N = ''.join(N)

        # Правило вывода P:
        P, next = [], 0
        sort_letter = [letter for letter in grammar if letter.isalnum() or letter == '-']
        letter = ['a']
        barrier = False
        for i in range(1, len(sort_letter)):
            if sort_letter[i] == 'a':
                letter = ''.join(letter)
                P.append(letter)
                letter = []
                letter.append('a')
            else:
                letter.append(sort_letter[i])
            if i == len(sort_letter) - 1:
                P.append(''.join(letter))
        if P[0][-1].isdigit():
            P.insert(P.index(f'{N[-1].lower()}n') + 1, N[-1])
        else:
            P.insert(P.index(f'{N[-1].lower()}n'), N[-1])
        if P.count(f'{N[-1].lower()}n') > 1:
            P = ''.join([f'{T[_]}A{T[_]}' + '|' * (_ != len(T) - 1) for _ in range(len(T))])
        else:
            if P.index('A') > P.index('an'):
                P = ''.join([f'{T[_]}A' + '|' * (_ != len(T) - 1) for _ in range(len(T))])
            else:
                P = ''.join([f'{T[_]}A' + '|' * (_ != -len(T)) for _ in range(-1, -1 - len(T), -1)])

        print(f'P: S -> {P}, {", ".join([letter + f"-> {[P, chr(949)][i]}" for i, letter in enumerate(["A", "A"])])} ', end='')
        print(f'\nT: {T}\nN: {N}')

        return P, [P, chr(949)], T, N


def kholmsky_classification(P):
    # print(P.split(' -> '))
    type = 0
    if len([elem for elem in P if elem.isupper()]):  # 0 тип (проверяем наличие нетерминальных символов)
        left, right = P.split(' -> ')
        N_left = [elem for elem in left if elem.isupper()]
        # print(N_left)
        context_sensitive = False
        intractable = False
        if len(left) <= len(right):  # 1 тип НУ (если левая часть меньще или равна правой)
            intractable = True
        for elem in N_left:  # 1 тип КЗ (сравниваем у левых и правых частей их боковые элементы)
            if len(left[:left.find(elem)]) > 0:
                left_left = left[:left.find(elem)]
            else:
                left_left = chr(949)
            if len(left[left.find(elem) + 1:]) > 0:
                right_left = left[left.find(elem)+1:]
            else:
                right_left = chr(949)
            left_bound_check, right_bound_check = False, False
            if (left_left in right and left_left[0] == right[0]) or left_left == chr(949):
                left_bound_check = True
            if right_left in right and right_left[-1] == right[-1] or right_left == chr(949):
                right_bound_check = True
            if right_bound_check and left_bound_check:
                if len(right_left) + len(left_left) - (left_left==chr(949)) - (right_left==chr(949)) < len(right):
                    context_sensitive = True
                    break
        if context_sensitive or intractable:
            if len(left) == 1 and left.isupper():  # 2 тип(если слева 1 символ и он нетерминальный)
                if len([elem for elem in P if elem.isupper()]) == 2 and (right[0].isupper() or right[-1].isupper()) or right == chr(949):
                    type = 3
                    print('3-й тип (Регулярный)')
                else:
                    type = 2
                    print('2-й тип (КС)')
            else:
                type = 1
                print('1-й тип (КЗ)' if context_sensitive else '1-й тип (НУ)')

        else:
            print('Нулевой тип!')
    else:
        print('Грамматика введена некорректно!')
    return type


# Машин вариант:
# L = '{a1a2...ananan-1...a1|ai∈{0,1}}'  # ∈ - знак принадлежности

# Мой вариант:
L = '{ab^nc|n>=1}'

print(f'Грамматика согласно варианту:\nL(G)={L}')

# Собираем данные о грамматике:
P = inference_rule(L)

# Классификация грамматик и языков по Холмскому:
print('Классификация грамматик и языков по Холмскому:')
# Для моего варианта:
print('Для 13-го варианта:')
L = f'S -> {P[0]}'
kholmsky_classification(L)
# Для любого P:
print('Для любого P: ')
L = ''
# L = 'S -> aaCFD'
while L != 'exit':
    type = []
    amount = int(input('Введите кол-во строк:'))
    for i in range(amount):
        L = input('Введите грамматику L(G)/exit - для выхода: ')
        if L != 'exit':
            print(f'P{i+1}: ')
            type.append(kholmsky_classification(L))
            print(f'Тип: {min(type)}')
        else:
            break
print('Good bye!')