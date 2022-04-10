from itertools import product

pairs, h = set(), int(input('Введите кол-во пар: '))
i = 0
while len(pairs) < h:
    i += 1
    x = list(product('012', repeat=i+1))
    #print(x)
    for i in range(len(x)):
        if len(x[i]) % 2 == 0:
            for j in range(len(x[i])):
                if x[i][j] == '1':
                    x[i] = list(x[i])
                    x[i][j] = str(x[i][j]) + '.'
                    #print(x[i][j])
                    x[i] = tuple(x[i])
                    #print(x[i])
            pairs.add(x[i])
        if len(pairs) >= h:
            break
length, sorted_pairs = sorted([len(elem) for elem in pairs]), []
pairs = list(pairs)
for i in range(len(pairs)):
    for j in range(len(pairs)):
        if length[i] == len(pairs[j]) and pairs[j] not in sorted_pairs:
            sorted_pairs.append(pairs[j])
print('Пары:', *[''.join(elem) for elem in sorted_pairs], sep = '\n')
