import datetime
from random import randint

class PrintTime:
    def __init__(self):
        self.enter_time = 0
        self.exit_time = 0
        self.delta_time = 0

    def __enter__(self):
        self.enter_time = datetime.datetime.now()
        print(f'Enter time: {self.enter_time}')
        return self

    def __exit__(self, type, value, traceback):
        self.exit_time = datetime.datetime.now()
        print(f'Exit time: {self.exit_time}')
        self.delta_time = self.exit_time - self.enter_time
        print(f'Delta time: {self.delta_time}')


def game(number): #небольшая игра которая оценивает с помощью ProntTime скорость ответа игрока
    input('''
    Для победы необходимо найти на игровом поле символ '|'
    В ответе необходимо ввести номер строки 
    и номер элемента через пробел (например Ответ:5 4). 
    Для старта нажмите Enter.''')
    field = []
    answer = [randint(0,number-1), randint(0,number-1)]
    for i in range(number):
        field.append([])
        for f in range(number):
            field[i].append('/')
    field[answer[0]][answer[1]] = '|'
    print(field)
    for i in range(number):
        print()
        for f in range(number):
            print(field[i][f], end='')
    print()
    user_answer = []
    with PrintTime() as timer:
        while answer != user_answer:
            try:
                user_answer = list(map(int,input('Ответ:').split(' ')))
            except ValueError:
                print('Вы ввели не число')
            else:
                user_answer = [x-1 for x in user_answer]
            if answer != user_answer:
                print('Неправильно')
    print(f'Вы победили! Ваш результат: {timer.delta_time}')

game(5)


print('Узнать что быстрее генератор списков или цикл for')
print('Генератор списков')
with PrintTime() as genlist:
    gen_list = [x for x in range(200000)]
print('Цикл for для созщдания списка')
with PrintTime() as forlist:
    for_list = []
    for x in range(200000):
        for_list.append(x)
if genlist.delta_time < forlist.delta_time:
    print(f'Генератор списка быстрее на {forlist.delta_time - genlist.delta_time}')
else:
    print(f'Цикл for быстрее на {genlist.delta_time - forlist.delta_time}')