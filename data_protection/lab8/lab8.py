# -*- coding: cp1251 -*-
from random import choice as c

# Вариант 14
P = 71
Q = 79

# Простые числа:
prime_numbers = [1]
for i in range(100):
    count = 0
    for j in range(2, i + 1):
        if i % j == 0:
            count += 1
    if count == 1:
        prime_numbers.append(i)

# Числовые эквиваленты русских букв, цифр и символа пробела
translate_dict = {'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Д': 5, 'Е': 6, 'Ё': 7, 'Ж': 8, 'З': 9, 'И': 10, 'Й': 11, 'К': 12,
                  'Л': 13, 'М': 14, 'Н': 15, 'О': 16, 'П': 17, 'Р': 18, 'С': 19, 'Т': 20, 'У': 21, 'Ф': 22, 'Х': 23,
                  'Ц': 24, 'Ч': 25, 'Ш': 26, 'Щ': 27, 'Ъ': 28, 'Ы': 29, 'Ь': 30, 'Э': 31, 'Ю': 32, 'Я': 33, ' ': 34,
                  '0': 35, '1': 36, '2': 37, '3': 38, '4': 39, '5': 40, '6': 41, '7': 42, '8': 43, '9': 44}

# Определим N:
N = P * Q
print(f'Определим N: P*Q = {P}*{Q} = {N}')

# Найдём функцию Эйлера:
e_func = (P-1)*(Q-1)
print(f'Найдём функцию Эйлера: (P-1)(Q-1)=({P}-1)({Q}-1)={e_func}')

# Найдём значение числа k:
dividers_e = []
k = c(prime_numbers)
for i in range(2, e_func + 1):
    if e_func % i == 0:
        dividers_e.append(i)
while k in dividers_e:
    k = c(prime_numbers)

print(f'Делители функции Эйлера: {dividers_e}\nЧисло k: {k}')

count = 1
while (k * count) % e_func != 1:
    count += 1
K = count
print(f'Число K: {K}\nПроверка: ({K}*{k})mod{e_func}={(K*k)%e_func}')

word = input('Введите слово > ')
print(f'Зашифровываем...(Используя открытый ключ K={K})')
cryptogramm = []
for i, elem in enumerate(word):
    value = str((translate_dict[elem.upper()]**K) % N)
    cryptogramm.append(value)
    print(f'C{i+1}=({translate_dict[elem.upper()]}^{K})mod{N}={value}')

max_length = max([len(elem) for elem in cryptogramm])
for i, elem in enumerate(cryptogramm):
    while len(cryptogramm[i]) != max_length:
        cryptogramm[i] = '0' + cryptogramm[i]

print(f'C = {" ".join(cryptogramm)}')
print(f'Расшифровываем...(Используя закрытый ключ k={k})')
decrypt = []
for i, elem in enumerate(cryptogramm):
    decrypt.append((int(elem)**k) % N)
    print(f'M{i+1}=({elem}^{k})mod{N}={(int(elem)**k) % N}')
word_decrypt = []
for num in decrypt:
    for elem in translate_dict:
        if num == translate_dict[elem]:
            word_decrypt.append(elem)
            break
word_decrypt = "".join(word_decrypt)
print(word_decrypt, 'Данные расшифрованы.', sep='\n')
