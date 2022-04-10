from itertools import product

#  регулярное выражение(14-й вариант) = (a^* . bb(bb)^* . a^*)^*

pairs, h = set(), int(input('Введите кол-во пар: '))
i = 0
while len(pairs) < h:
    i += 1
    x = list(product('ab', repeat=i))
    for l in range(len(x)):
        count, flag = 0, False
        for k in range(1, len(x[l])):
            if flag == True:
                flag = False
                continue
            if x[l][k] == x[l][k - 1] == 'b':
                count += 1
                flag = True
        if count == x[l].count('b') / 2 and x[l].count('b') != 0:
            pairs.add(x[l])
            if len(pairs) >= h:
                break
length, sorted_pairs = sorted([len(elem) for elem in pairs]), []
pairs = list(pairs)
for i in range(len(pairs)):
    for j in range(len(pairs)):
        if length[i] == len(pairs[j]) and pairs[j] not in sorted_pairs:
            sorted_pairs.append(pairs[j])
print('Пары:', *[elem for elem in sorted_pairs])