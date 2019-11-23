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
            ingridient_dict[ingridient['ingridient_name']]={'measure': ingridient['measure'],'quantity':ingridient['quantity']*person_count}

    return ingridient_dict

print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
pprint(get_shop_list_by_dishes(['Фахитос', 'Омлет'], 3))