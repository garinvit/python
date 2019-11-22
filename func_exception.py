documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "passport", "number": "3344 667788" } #документ с отсуствующим полем name
]
directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006', '5400 028765', '5455 002299'],
    '3': []
}


def all_names(docs):#Новая функция к заданию про исключения можно вызвать командой an
    try:
        for doc in docs:
           print(doc['name'])
    except KeyError:
        print(f'Документ никому не принадлежит')

def people(docs, answer=False):
    if answer == False:
        answer = input('Введите номер документа: ')
    for doc in docs:
        if doc['number'] == answer:
            # print(f'Документ принадлежит {doc["name"]}')
            return doc['name']
    return 0


def doc_list(docs):#переделал с исключениями
    for doc in docs:
        try:
            print(f'{doc["type"]} "{doc["number"]}" "{doc["name"]}"')
        except KeyError:
            print(f'Документ {doc["number"]} никому не принадлежит')

def shelf_list(shelfs):
    for shelf in shelfs.keys():
        print(f'\nНа полке {shelf} документы:{shelfs[shelf]}')


def search_shelf(shelfs, answer=False):
    if answer == False:
        answer = input('Введите номер документа: ')
    if answer:
        for shelf in shelfs.items():
            if answer in shelf[1]:
                return shelf[0]
    return 0


def doc_add(docs, shelfs, answer=False):
    if answer == False:
        answer = input('Для добавления документа введите через запятую его номер, тип, имя владельца и номер полки: ')
    answer = answer.split(', ')
    if people(docs, answer[0]) != 0:
        return f'Документ с таким номером принадлежит {people(docs, answer[0])}'
    docs.append({"type": answer[1], "number": answer[0], "name": answer[2]})
    shelfs[answer[3]].append(answer[0])
    return docs, shelfs


# print(doc_add(documents, directories, '66 778899, passport, Петр Иванов, 3'))

def doc_del(docs, shelfs, answer=False):
    if answer == False:
        answer = input('Для удаления документа введите его номер: ')
    if people(docs, answer) == 0:
        print('Документа для удаления нет')
        return None
    for doc in docs:
        if doc['number'] == answer:
            docs.remove(doc)
    shelfs[search_shelf(shelfs, answer)].remove(answer)
    return docs, shelfs


# print(doc_del(documents, directories, '66 778899'))

def doc_move(shelfs, answer=False):
    if answer == False:
        answer = input('Для перемещения документа введите его номер и новую полку через запятую: ')
    answer = answer.split(', ')
    if answer[1] not in shelfs.keys():
        print('Полки не существует')
        return None
    if search_shelf(shelfs, answer[0]) == 0:
        print('Нет такого документа')
        return None
    shelfs[search_shelf(shelfs, answer[0])].remove(answer[0])
    shelfs[answer[1]].append(answer[0])
    return shelfs


# print(doc_move(directories, '66 778899, 2'))

def shelf_add(shelfs, answer=False):
    if answer == False:
        answer = input('Введите номер новой полки: ')
    if answer in shelfs.keys():
        print('Такая полка уже существует')
        return None
    shelfs[answer] = []
    return shelfs


# print(shelf_add(directories, '4'))

while True:
    answer = input('''
Программа для документооборота
Список комнад:
an-выводят имена всех документов;
p-выводит имя по номеру документа;
l-выводит список всех документов;
ld-выводит перечень всех полок;
s-выводит номер полки по номеру документа;
a-добавить новый документ;
d-удалить документ
m-изменить полку документ;
as-добавить полку;
q-выход.
'''
                   )
    if answer == 'p':
        owner = people(documents)
        if owner != 0:
            print(f'Документ принадлежит {owner}')
        else:
            print('Документ не найден')
    elif answer == 'l':
        doc_list(documents)
    elif answer == 'an':
        all_names(documents)
    elif answer == 'ld':
        shelf_list(directories)
    elif answer == 's':
        search = search_shelf(directories)
        if search != 0:
            print(f'Документ на полке {search}')
        else:
            print('Документ не найден')
    elif answer == 'a':
        doc_add(documents, directories)
    elif answer == 'd':
        doc_del(documents, directories)
    elif answer == 'm':
        doc_move(directories)
    elif answer == 'as':
        shelf_add(directories)
    elif answer == 'q':
        print('Досвидания')
        break