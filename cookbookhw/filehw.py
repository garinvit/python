from pprint import pprint

def make_cookbook(filename):
    cookbook = {}
    with open(filename, encoding='utf8') as file:
        while True:
            rec_name = file.readline().strip()
            if rec_name == '':
                break
            cookbook[rec_name] = []
            amount = file.readline()
            for i in range(int(amount)):
                dish = file.readline().strip().split(' | ')
                cookbook[rec_name].append({'ingridient_name': dish[0], 'quantity': int(dish[1]), 'measure': dish[2]})
            file.readline()
    return cookbook


def get_shop_list_by_dishes(dishes, person_count):
    cookbook = make_cookbook('recipes.txt')
    ingridient_dict = {}
    for dish in dishes:
        for ingridient in cookbook[dish]:
            if ingridient['ingridient_name'] in ingridient_dict.keys():
                upd_dict = {ingridient['ingridient_name']:{'measure': ingridient['measure'],
                            'quantity': ingridient_dict[ingridient['ingridient_name']]['quantity'] + ingridient['quantity'] * person_count}}
                ingridient_dict.update(upd_dict)
            else:
                upd_dict = {ingridient['ingridient_name']:{'measure': ingridient['measure'],'quantity': ingridient['quantity'] * person_count}}
                ingridient_dict.update(upd_dict)
    return ingridient_dict

#print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
#pprint(get_shop_list_by_dishes(['Фахитос', 'Омлет'], 3))
pprint(get_shop_list_by_dishes(['Омлет', 'Омлет'], 3))
pprint(get_shop_list_by_dishes(['Омлет', 'Фахитос', 'Омлет', 'Фахитос'], 3))
pprint(get_shop_list_by_dishes(['Омлет', 'Омлет', 'Омлет'], 3))