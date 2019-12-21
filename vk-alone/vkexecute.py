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


def request_params(method_name, ids=None, code=None):
    params = {
        'access_token': ACCESS_TOKEN,
        'v': V_API
    }
    if method_name == 'execute':
        params['code'] = code
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


def all_friends_groups(friends_id, echo=True):
    method_name = 'execute'
    if type(friends_id) == str or type(friends_id) == int:
        friend_list = [friends_id]
    else:
        friend_list = friends_id
    start = 0
    all_groups = []
    if echo:
        print(f'Всего людей в списке {len(friend_list)}')
        print('Обработано: ', end='')
    while start < len(friend_list):
        end = start + 25
        if end > len(friend_list):
            end = len(friend_list)
        code = f'var fl = {friend_list}; var end = {end}; var start = {start};' + '''
        var gr = [];
        var resp;
        while (start != end){
            resp = API.groups.get({"user_id":fl[start]}).items;
            gr.push(resp);
            start = start+1;
        };
        return gr;
        '''
        response = requests.get(URL + method_name, params=request_params(method_name, code=code)).json()['response']
        for groups in response:
            if groups is not None:
                all_groups.append(set(groups))
        start = end
        if echo:
            print(f'{round(end/len(friend_list)*100)}%   ', end='', flush=True)
    if echo:
        print(f'\nОбработка завершена. Людей у которых открыты группы {len(all_groups)}')
    return all_groups


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
    friends_groups = all_friends_groups(friends_list)
    my_group = all_friends_groups(user_id, echo=False)[0]
    diff_group = my_group.copy()
    for groups in friends_groups:
        diff_group.difference_update(groups & my_group)
    if fp is not None:
        get_groups_info(diff_group, fp)
    return diff_group


if __name__ == '__main__':
    user = alone_group('eshmargunov', 'groups.json')

