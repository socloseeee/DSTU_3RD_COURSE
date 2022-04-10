rights = ('read', 'write', 'grant')
s = 5  # кол-во объектов

def check_rights(x):
    if x != '000':
        return ', '.join([rights[i] for i in range(len(x)) if x[i] == '1'])
    else:
        return 'no rights'

users = {'Белоснежка': ['111', '111', '111', '111', '111'],  # массив значений ключа - это
         'Умник': ['101', '110', '000', '100', '101'],       # массив прав доступа к объекта
         'Ворчун': ['000', '000', '000', '000', '000'],
         'Весельчак': ['110', '000', '110', '001', '101'],
         'Соня': ['101', '101', '001', '010', '101'],
         'Скромник': ['010', '000', '000', '001', '001'],
         'Чихун': ['010', '011', '000', '101', '101'],
         'Простачок': ['110', '011', '010', '011', '000']}

def all_rights(name):
    return [f'Object{i + 1}: ' + check_rights(users[name][i]) for i in range(s)]

def assignment(object2, right2, recipient2):
    users[recipient2][object2 - 1] = users[recipient2][object2 - 1][:rights.index(right2)] + '1' + users[recipient2][object2 - 1][rights.index(right2) + 1:]

flag = False
while True:
    user = input('User: ')
    if not flag:
        flag = True
        print(*all_rights(user), sep='\n')
    operation = input('Жду ваших указаний > ')
    while operation != 'quit':
        if operation != 'grant':
            object = int(input('Над каким объектом производится операция? '))
            if operation in all_rights(user)[object - 1]:
                print('Операция прошла успешно')
            else:
                print('Отказ в выполнении операции. У вас недостаточно прав.')
        else:
            object = int(input('Право на какой объект передаётся? '))
            if operation in all_rights(user)[object - 1]:
                right = input('Какое право передаётся? ')
                recipient = input('Какому пользователю передаётся право? ')
                assignment(object, right, recipient)
                print('Операция прошла успешно')
            else:
                print('Отказ в выполнении операции. У вас недостаточно прав.')
        operation = input('Жду ваших указаний > ')
    print(f'Работа пользователя {user} завершена.')
    choice = input('Желаете продолжить? ')
    flag = False
    if choice.lower() == 'нет':
        break
print('До свидания!')
