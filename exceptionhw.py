class WrongLenght(Exception):
   pass

user_input = input('Польская нотация. Введите операцию и два числа через пробел: ').split(' ')
try:
    assert user_input[0] in ['+','-','*','/'], 'No operator'
    num_1 = int(user_input[1])
    num_2 = int(user_input[2])
    if user_input[0] == '/' and num_2 == 0:
        raise ZeroDivisionError
    if len(user_input) != 3:
        raise WrongLenght
except AssertionError :
    print('Не выбрано арифметическое действие!')
except ValueError:
    print('Вы ввели не число!')
except WrongLenght:
    print('Неверное количество чисел')
except ZeroDivisionError:
    print('Нельзя делить на 0')
except Exception as exc_name:
    print(f'Какая то другая ошибка. {exc_name}')
else:
    print('Вычисляю...')
    if user_input[0] == '+':
        print(f'Результат сложения: {num_1 + num_2}')
    elif user_input[0] == '-':
        print(f'Результат вычитания: {num_1 - num_2}')
    elif user_input[0] == '*':
        print(f'Результат умножения: {num_1 * num_2}')
    elif user_input[0] == '/':
        print(f'Результат деления: {num_1 / num_2}')