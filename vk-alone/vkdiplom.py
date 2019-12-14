import json
import requests
import time
from sys import argv
from pprint import pprint

with open('token.txt', 'r') as token:
    ACCESS_TOKEN = token.read()
    if len(ACCESS_TOKEN) == 0:
        print('Файл с токеном пуст.')
        ACCESS_TOKEN = input('Введите токен:')
        with open('token.txt', 'w') as new_token:
            new_token.write(ACCESS_TOKEN)

URL = 'https://api.vk.com/method/'
V_API = '5.103'

def request_params(method_name, ids):
    params = {
        'access_token': ACCESS_TOKEN,
        'v': V_API
    }
    if method_name == 'users.getSubscriptions':
        params['user_id'] = ids
        params['extended'] = 1
    elif method_name == 'friends.get':
        params['user_id'] = ids
    elif method_name == 'groups.getById':
        params['group_ids'] = ids
        params['fields'] = 'members_count'
    elif method_name == 'users.get':
        params['user_ids'] = ids
    return params


def get_id(user_id=None):
    """
    Функция возвращает числовой id пользователя, если ей передано имя короткого домена ВК
    Пример: get_id('eshmargunov') вернет значение '171691064'.
    Если функции не передать никакого значения, то сначала функция проверит не был ли передан id
    вместе с вызовом скрипта в командной строке. Если такой аргумент был передан то функция вернет id
    даже если аргумент был коротки именем.
    Пример:python.exe vk_diplom.py eshmargunov
    get_id() вернет значение '171691064'.
    Если не передать никакого значение ни через аргумент функции и командную строку. То функция попросит
    ввести пользователя короткое имя или числовой id пользователя.
    """
    if user_id is None:
        try:
            vk_id = argv[1]
            return get_id(vk_id)
        except IndexError:
            user_input = input('Введите ID пользователя ВК:')
            return get_id(user_input)
    try:
        vk_id = int(user_id)
    except (ValueError, TypeError):
        method_name = 'users.get'
        time.sleep(0.5)
        response = requests.get(URL + method_name, params=request_params(method_name, user_id))
        vk_id = response.json()['response'][0]['id']
    return str(vk_id)


def get_friends_list(user_id):
    # Функция принимает id пользователя, возвращает список id друзей
    method_name = 'friends.get'
    time.sleep(0.5)
    response = requests.get(URL + method_name, params=request_params(method_name, user_id))
    try:
        if response.json()['error']['error_code'] == 30:
            # У пользователя скрыты друзья
            return []
    except KeyError:
        pass
    friends_list = response.json()['response']['items']
    return friends_list


def get_groups(user_id):
    # Функция принимает id пользователя, возвращает id групп
    method_name = 'users.getSubscriptions'
    response = requests.get(URL + method_name, params=request_params(method_name, user_id))
    try:
        if response.json()['error']['error_code'] == 30 or response.json()['error']['error_code'] == 18:
            # У пользователя скрыты группы или пользователь удален
            return set()
        elif response.json()['error']['error_code'] == 6:
            time.sleep(0.5)
            return get_groups(user_id)
    except KeyError:
        pass
    try:
        groups = response.json()['response']['items']
    except:
        pass
    groups_id = [group['id'] for group in groups]
    return set(groups_id)


def alone_group(vk_id=None, fp=None):
    # Функция использует функцию get_id() для получения id
    # из аргументов, из командной строки или ввода пользователя
    # возвращает множество групп в которых
    # состоит пользователь и не состоят его друзья
    # возможна запись в файл при указании fp, через функцию
    user_id = get_id(vk_id)
    time.sleep(0.5)
    friends_list = get_friends_list(user_id)
    time.sleep(0.5)
    user_group = get_groups(user_id)
    diff_group = user_group.copy()
    print('▐', ' ' * 50, '▌', sep='', end='')
    for i, friend in enumerate(friends_list):
        f_group = get_groups(friend)
        diff_group.difference_update(f_group & user_group)
        chr_mul = round((i + 1) / len(friends_list) * 50)
        print('\r', '▐', '█' * chr_mul, ' ' * (50 - chr_mul), '▌', sep='', end='')
    print()
    if fp is not None:
        get_groups_info(diff_group, fp)
    return diff_group


def get_groups_info(groups, fp=None):
    # Функция принимает ids группы (строка или число)
    # или групп (список, кортеж, множество),
    # возвращает id, имя и количество участников групп
    # может записать в json файл если указать путь get_groups_info()
    method_name = 'groups.getById'
    if type(groups) != str and type(groups) != int:
        group_ids = ''
        for i in groups:
            group_ids += f'{str(i)},'
    else:
        group_ids = groups
    response = requests.get(URL + method_name, params=request_params(method_name, group_ids))
    info = response.json()['response']
    groups_dict = {'groups': []}
    for i in info:
        groups_dict['groups'].append({
            'gid': i['id'],
            'name': i['name'],
            'members_count': i['members_count'],
        })
    if fp is not None:
        with open(fp, 'w') as json_file:
            json.dump(groups_dict, json_file)
    return groups_dict


if __name__ == '__main__':
    user = alone_group('eshmargunov', 'groups.json')
