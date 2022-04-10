import random
import time
from pynput.keyboard import Key, Listener
import io

phrases = ['Скажи ка дядя ведь не даром',  # Лермонтов
           'Жди меня и я вернусь',  # Симонов
           'Утихла брань племен в пределах отдаленных',  # Пушкин
           'Я вяну прекрати тяжелый жизни сон',  # Пушкин
           'Белая берёза под моим окном',  # Есенин
           'Я помню чудное мгновенье',  # Пушкин
           'Люблю отчизну я но странною любовью',  # Лермонтов
           'Героини испанских преданий умирали любя',  # Цветаева
           'Мороз и солнце день чудесный',  # Пушкин
           'Не выходи из комнаты не совершай ошибку']  # Бродский


def value():
    return random.choice(phrases)


def idval_deflect(text2):  # высчитывает идеальное значение и отклонение
    values_between_keys, phrase_input = [], ''
    for _ in range(len(text2)):
        start_time = time.time()
        phrase_input += input()
        values_between_keys.append(time.time() - start_time)
    ideal_value = sum([values_between_keys[_] for _ in range(len(values_between_keys))]) / len(text2)
    deflection = sum([values_between_keys[_] - ideal_value for _ in range(len(values_between_keys))]) / len(text2)
    return ideal_value, deflection


def press_gaps():
    mas_time, text1 = [], []

    def on_press(key):
        CurrentTime = time.time()

        if key != Key.caps_lock and key != Key.alt_l and key != Key.shift and key != Key.enter:
            if key != Key.space:
                if key != Key.backspace:
                    text1.append(key)
                    # mas_time.append(CurrentTime)
                if key == Key.backspace:
                    text1.pop(-1)
                    mas_time.pop(-1)
                    mas_time.pop(-1)
            else:
                text1.append(' ')
        mas_time.append(CurrentTime)

    def on_release(key):
        # print(f'{key} release')
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    values = []
    for j in range(1, len(mas_time) - 1):
        values.append(mas_time[j] - mas_time[j - 1])

    ideal_value = sum([values[_] for _ in range(len(values))]) / len(text1[:-1])
    deflection = sum([values[_] - ideal_value for _ in range(len(values))]) / len(text1[:-1])
    text1 = ''.join([elem.char if elem != ' ' else elem for elem in text1[:-1]])
    print(' Проверка...', end='')
    return ideal_value, deflection, text1


phrases2 = ['да', 'нет', 'ок']
users = {}
while True:
    flag = input('Войти/Выйти(0/Любая клавиша)? ')
    while flag == '0':
        f = open('lab3/data_lab3.txt', 'a')  # a - дозапись, w - запись
        choice = input('Войти в аккаунт/Зарегистрироваться/Выйти из программы(0/1/Любая клавиша)? ')
        if choice == '0':
            login = input('Введите логин(имя): ')
            flag3, col = False, 0
            with io.open('lab3/data_lab3.txt', encoding='Windows 1251') as file:
                for line in file:
                    if not flag3:
                        col += 1
                    if login in line:
                        flag3 = True
            with open('lab3/data_lab3.txt') as f:
                lines = f.readlines()
                key_phrase, idval_user, deflect_user = lines[col].split(',')
            if flag3:
                print(f'Проверка пользователя. Введите кодовую фразу: {key_phrase}')
                flag2 = False
                idval, deflect = 0, 0
                while not flag2:
                    idval, deflect, text = press_gaps()
                    if text == key_phrase.lower():
                        print('Верно!\n', end='')
                        flag2 = True
                    else:
                        print('Фраза введена неверно! Попробуйте заново!')
                print('', f'{abs(float(idval_user) - idval)} < 0,15',
                      f'{abs(float(deflect_user) - deflect)} < 0,15', sep='\n')
                if abs(float(idval_user) - idval) < 0.15 and abs(float(deflect_user) - deflect) < 0.15:
                    print('\nУспешный вход!')
                else:
                    print('Проверка не пройдена!')
            else:
                print('Данный пользователь отсутствует в системе!')
            f.close()
        elif choice == '1':
            phrase = random.choice(phrases)
            name = input('Введите имя пользователя: ')
            if name not in users:
                print(f'Введите данную фразу 3 раза: {phrase}')
                flag1 = 0
                idval, deflect = [], []
                while flag1 != 3:
                    idval, deflect = [], []
                    for i in range(3):
                        flag1 += 1
                        a, b, check_text = press_gaps()
                        if check_text != phrase.lower():
                            flag1 = 0
                            print('Попробуйте заново!')
                            break
                        print('Верно!\n', end='')
                        idval.append(a)
                        deflect.append(b)
                print()
                idval = sum(idval) / len(idval)
                deflect = sum(deflect) / len(deflect)
                users[name] = (phrase, str(idval), str(deflect))
                print(users)
                f.write(name + '\n' + ', '.join(users[name]) + '\n')
                s = name + '\n' + ', '.join(users[name]) + '\n'
                print(f'<Идеальное значение> = {idval}', f'<Отклонение> = {"%0.30f" % deflect}', sep='\n')
                print('Регистрация прошла успешно!')
                f.close()
            else:
                print('Данный пользователь уже зарегистрирован!')
        else:
            print('Возврат на стартовую страницу!')
            break
    else:
        print('До свидания!')
        break
