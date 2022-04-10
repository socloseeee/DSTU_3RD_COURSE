print('Введите N:')
N, ost, odd, counter, ostMas, word, flag, flagOne, flagTwo, flagThree = input(), 0, 0, 0, [], '', False, False, False, False
if N.isdigit() != True:
    flagThree = True
    print('Некорректный ввод числа N!')
if flagThree == False:
    if int(N) != 0:
        N = int(N)
        print('Введите алфавит:')
        i, alphabet, counterTwo = 0, [i for i in list(input())], 0
        power = len(alphabet)
        if ''.join(alphabet).isalpha() != True:
            flagThree = True
            print('Алфавит не может содержать числа!')
        if flagThree != True:
            Ru, Eng = [chr(1072 + i) for i in range(32)], [chr(97 + i) for i in range(26)]
            for i in range(len(alphabet)):
                if alphabet[i] in ''.join(Ru):
                    flagOne = True
                if alphabet[i] in ''.join(Eng):
                    flagTwo = True
                if flagOne == flagTwo == True:
                    print('Смешение алфавитов')
                    flagThree = True
                    break
            if flagThree == False:
                while N > power:
                    odd, ost = N // power, N - ((N // power) * power)
                    if ost == 0:
                        ost += power
                        odd -= 1
                        N -= 1
                        #print(f'({odd} * {power}) + {ost}')
                    ostMas.append([ost])
                    N //= power
                    counter += 1
                ostMas = ostMas[::-1]
                ostMas.insert(0, [odd])
                #print(ostMas)
                for i in range(counter + 1):
                    for j in range(i):
                        ostMas[j].append(power)
                 #print(ostMas)
                for i in range(len(ostMas)):
                    word += alphabet[ostMas[i][0] - 1]
                formula = ''
                for elem in ostMas:
                     formula += f'{elem[0]} * {power}^{str(len(elem) - 1)}'
                     if elem != ostMas[len(ostMas) - 1]:
                         formula += ' + '
                print(formula)
                print(word)
    else:
        print(chr(949))