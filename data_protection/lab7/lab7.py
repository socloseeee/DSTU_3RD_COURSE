# -*- coding: cp1251 -*-

from tkinter import *
from tkinter import messagebox
import time

txt_file = 'lab7_passwords.txt'

registration = False
while True:
    choice = input('Войти в систему(0)/Зарегистрироваться(1) > ')
    if choice.isdigit():
        if choice in ['0', '1']:
            registration = True if choice == '1' else False
            break
    print('Incorrect input!')
if not registration:
    with open(txt_file, 'r') as file:
        file_info = file.readlines()
        while True:
            username = input('Введите имя пользователя > ')
            if username + '\n' in file_info:
                break
            print('Данный пользователь отсутствует в системе!')
        check_pass = file_info[file_info.index(username + '\n') + 1][:-1]
        print(f'check_pass(array interpretation): {check_pass}')
        check_pass = "".join([symbol for symbol in check_pass if symbol.isdigit()])
        print(f'check_pass(num chain to check): {check_pass}')
else:
    with open(txt_file, 'a') as file:
        username = input('Введите имя пользователя > ')
        file.write(username + '\n')

print('Строим граф...')
# Визуал графического ключа:
tk = Tk()
app_running = True

size_x = 600
size_y = 600
s_x = s_y = 3  # кол-во точек 3x3
step_x = size_x // s_x  # шаг по горизонтали
step_y = size_y // s_y  # шаг по вертикали
menu_y = 50
cells = []  # список точек обозначенных 0
list_ids = []  # список объектов canvas


def on_closing():
    global app_running
    if messagebox.askokcancel("Выход", "Подтвердите действие"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title('Graphic Key')
tk.resizable(width=False, height=False)  # размер окна неизменяем
tk.wm_attributes("-topmost", 1)  # окно всегда поверх других окон
canvas = Canvas(tk, width=size_x, height=size_y + menu_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_x, size_y, fill="white")
canvas.pack()
tk.update()


def draw_table():
    [canvas.create_line(step_x * i, 0, step_x * i, size_y) for i in range(0, s_x + 1)]
    [canvas.create_line(0, step_y * i, size_x, step_y * i) for i in range(0, s_y + 1)]


draw_table()


def button_save_password():
    global app_running
    app_running = False
    tk.destroy()


attempts = 3


def check_password():
    global attempts
    global app_running
    global list_ids
    if not registration:
        if check_pass == "".join(["".join([str(num) for num in tuple_]) for tuple_ in cells]):
            messagebox.showinfo(title='Проверка пароля', message='Успешных вход!')
            print(
                f'entered password(num chain to check): {"".join(["".join([str(num) for num in tuple_]) for tuple_ in cells])}')
            print(
                f'check_pass: {check_pass}\ncells: {"".join(["".join([str(num) for num in tuple_]) for tuple_ in cells])}')
            app_running = False
            tk.destroy()
        else:
            if len(list_ids) > 0:
                for el in list_ids:
                    canvas.delete(el)
                list_ids.clear()
            cells.clear()
            attempts -= 1
            messagebox.showerror(title='Проверка пароля', message=f'Пароль не совпал!\nОсталось попыток: {attempts}')
            if attempts == 0:
                app_running = False
                tk.destroy()
    else:
        messagebox.showerror(title='Проверка пароля',
                             message='Вы не можете проверить пароль!\nТак как вы находитесь в процессе регистрации!')


b0 = Button(tk, text="Закончить ввод", command=button_save_password)
b0.place(y=size_y + 10, x=340)
b1 = Button(tk, text="Проверить пароль", command=check_password)
b1.place(y=size_y + 10, x=120)


def draw_point(x, y):
    if (x, y) not in cells:
        color = 'blue'
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        cells.append((x, y))
    print(cells)


def add_to_all(event):
    coordinate_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    coordinate_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    mouse_x = coordinate_x // (size_x // s_x)
    mouse_y = coordinate_y // (size_y // s_y)
    # print(mouse_x, mouse_y)
    if coordinate_x < size_x and coordinate_y < size_y:
        draw_point(mouse_x, mouse_y)


canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)

print(f'entered password(array interpretation): {cells}')

if registration:
    with open(txt_file, 'a') as file:
        file.write(f'{cells}\n')
