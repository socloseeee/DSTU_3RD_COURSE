# -*- coding: cp1251 -*-
from random import choice as c

# ������� 14
P = 71
Q = 79

# ������� �����:
prime_numbers = [1]
for i in range(100):
    count = 0
    for j in range(2, i + 1):
        if i % j == 0:
            count += 1
    if count == 1:
        prime_numbers.append(i)

# �������� ����������� ������� ����, ���� � ������� �������
translate_dict = {'�': 1, '�': 2, '�': 3, '�': 4, '�': 5, '�': 6, '�': 7, '�': 8, '�': 9, '�': 10, '�': 11, '�': 12,
                  '�': 13, '�': 14, '�': 15, '�': 16, '�': 17, '�': 18, '�': 19, '�': 20, '�': 21, '�': 22, '�': 23,
                  '�': 24, '�': 25, '�': 26, '�': 27, '�': 28, '�': 29, '�': 30, '�': 31, '�': 32, '�': 33, ' ': 34,
                  '0': 35, '1': 36, '2': 37, '3': 38, '4': 39, '5': 40, '6': 41, '7': 42, '8': 43, '9': 44}

# ��������� N:
N = P * Q
print(f'��������� N: P*Q = {P}*{Q} = {N}')

# ����� ������� ������:
e_func = (P-1)*(Q-1)
print(f'����� ������� ������: (P-1)(Q-1)=({P}-1)({Q}-1)={e_func}')

# ����� �������� ����� k:
dividers_e = []
k = c(prime_numbers)
for i in range(2, e_func + 1):
    if e_func % i == 0:
        dividers_e.append(i)
while k in dividers_e:
    k = c(prime_numbers)

print(f'�������� ������� ������: {dividers_e}\n����� k: {k}')

count = 1
while (k * count) % e_func != 1:
    count += 1
K = count
print(f'����� K: {K}\n��������: ({K}*{k})mod{e_func}={(K*k)%e_func}')

word = input('������� ����� > ')
print(f'�������������...(��������� �������� ���� K={K})')
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
print(f'��������������...(��������� �������� ���� k={k})')
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
print(word_decrypt, '������ ������������.', sep='\n')
