from random import randint


class Animal:
    list_obj = []
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.product = 0
        self.voice = 'Rrrrr'
        self.hungry = False
        self.animal_type = 'Животное'
        self.list_obj.append(self)

    def feed(self):
        if self.hungry == True:
            self.weight *= 1.03
            self.hungry = False
            self.say()
        else:
            print('Не голоден')

    def starvation(self):
        self.weight *= 0.99
        self.hungry = True

    def say(self):
        print(self.voice)

    def get_product(self):
        pass

    def typical_day(self):
        self.starvation()
        self.feed()
        self.starvation()
        self.feed()
        self.get_product()


class Cow(Animal):

    def __init__(self, name, weight, type_animal='Корова'):
        super().__init__(name, weight)
        self.animal_type = type_animal
        if self.animal_type == 'Корова':
            self.voice = 'Муууууууу'
        if self.animal_type == 'Коза':
            self.voice = 'Меееее'

    def get_product(self):
        item = randint(10,25)
        self.product += item
        self.weight -= item
        self.hungry = True
        print(f'{self.animal_type} дала {item} литров молока. За все время {self.product} литров')

    def typical_day(self):
        super().typical_day()
        self.feed()

class Bird(Animal):
    def __init__(self, name, weight, type_animal='Гусыня'):
        super().__init__(name, weight)
        self.animal_type = type_animal
        if self.animal_type == 'Гусыня':
            self.voice = 'Гагага'
        if self.animal_type == 'Утка':
            self.voice = 'Кря-Кря'
        if self.animal_type == 'Курица':
            self.voice = ' Кудах'

    def get_product(self):
        item = randint(0,5)
        self.product += item
        self.weight -= item*0.05
        self.hungry = True
        print(f'{self.animal_type} дала {item} яиц . За все время {self.product} яиц')


class Sheep(Animal):

    def __init__(self, name, weight):
        super().__init__(name, weight)
        self.animal_type = 'Овца'
        self.voice = 'Беееее'

    def get_product(self):
        item = randint(1,5)
        self.product += item
        self.weight -= item
        self.hungry = True
        print(f'{self.animal_type} дала {item} кг шерсти. За все время {self.product} шерсти')

goose_gray = Bird('Серый', 35)
goose_white = Bird('Белый', 30)
cow_manka = Cow('Манька', 300)
sheep_barashek = Sheep('Барашек', 150)
sheep_kudr = Sheep('Кудрявый', 170)
chicken_coco = Bird('Ко-ко', 10, 'Курица')
chicken_kuka = Bird('Кукареку', 12, 'Курица')
goat_roga = Cow('Рога', 120, 'Коза')
goat_kopyta = Cow('Копыта', 120, 'Коза')
duck_kryk = Bird('Кряква',7,'Утка')

#Смоделировать несколько дней когда животные едят и дают продукт
# for animal in Animal.list_obj:
# #     for i in range(7):
# #         animal.typical_day()

sum_weight = 0
top_weight = 0
name_top_weight = ''
for animal in Animal.list_obj:
    sum_weight += animal.weight
    if animal.weight > top_weight:
        top_weight = animal.weight
        name_top_weight = animal.name

print(f'Самый тяжелый на ферме это {name_top_weight} и он весит {top_weight} кг, все вместе весят {sum_weight}кг')

