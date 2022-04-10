import random

rights = ('Совершенно секретно', 'Секретно', 'Открытые данные')
s = 5  # кол-во объектов
users = ['Белоснежка', 'Умник', 'Ворчун', 'Весельчак', 'Соня', 'Скромник', 'Чихун', 'Простачок']

print('\nУровни конфиденциальности объектов (О):')
O = {f'Объект_{_ + 1}': rights[random.randint(0, len(rights)) - 1] for _ in range(s)}
print(*[f'{key}: {value}' for key, value in O.items()], sep='\n')
print('\nУровни допуска пользователей (S):')
S = {users[_]: rights[random.randint(0, len(rights)) - 1:] for _ in range(len(users))}
print(*[f'{key}: {value[0]}' for key, value in S.items()], '',sep='\n')


def check_rights(name):
    return [key for key, value in O.items() if value in S[name]]

while True:
    user = input('User: ')
    if user not in O:
        print('Идентификация прошла успешно, добро пожаловать в систему')
        rights_objects = check_rights(user)
        print('Перечень доступных объектов:', ', '.join(rights_objects))
        operation = ''
        while operation != 'quit':
            operation = input('Жду ваших указаний> ')
            if operation == 'request':
                object_ = input('К какому объекту хотите осуществить доступ? ')
                if f'Объект_{object_}' in rights_objects:
                    print('Операция прошла успешно')
                else:
                    print('Отказ в выполнении операции. Недостаточно прав.')
            else:
                if operation != 'quit':
                    print('Некорректнный ввод операции.')
        print(f'Работа пользователя {user} завершена. До свидания.')
    else:
        print('Данный пользователь отсутствует в системе. Введите корректное имя пользователя!')
