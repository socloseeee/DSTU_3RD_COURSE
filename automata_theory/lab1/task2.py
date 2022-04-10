print('Введите слово:' )
word, Ru, Eng, flagOne, flagTwo, flagThree = input(), [chr(1072 + i) for i in range(32)], [chr(97 + i) for i in range(26)], False, False, False
if word.isalpha() == False:
    flagThree = True
    print('Ошибка ввода слова!')
if flagThree == False:
    print('Введите алфавит:')
    i, alphabet = 0, [i for i in list(input())]
    if ''.join(alphabet).isalpha() != True:
        flagThree = True
        print('Неккоректный ввод алфавита')
    err = ''
    if flagThree == False:
        for i in range(len(word)):
            if not word[i] in alphabet:
                flagThree = True
                err += str(word[i]) + ' '
        if flagThree == True:
            print(f'{err}не присутствует в алфавите. Ошибка ввода!')
if flagThree == False:
    for i in range(len(word)):
        if word[i] in ''.join(Ru):
            flagOne = True
        if word[i] in ''.join(Eng):
            flagTwo = True
        if flagOne == flagTwo == True:
            print('Смешение алфавитов')
            flagThree = True
            break
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
    odds, formula = '', ''
    for i in range(len(word)):
        odds += str(alphabet.index(word[i]) + 1)
    N = sum([(len(alphabet) ** (len(word) - i - 1)) * int(odds[i]) for i in range(len(word))])
    for i in range(len(odds)):
        formula += f'{odds[i]} * {len(alphabet)}^{(len(word) - i - 1)}'
        if i <= len(odds) - 2:
            formula += ' + '
    print(f'{formula} = {N}')