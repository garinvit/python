import requests
from pprint import pprint

ACCESS_TOKEN = '4a72e919308ec960aed7666c49d11e56efddb316b8b40abc3ce4657449e145dd766512612f4eb832557f4'
URL = 'https://api.vk.com/method/'
V_API = '5.103'
#oauth_url = 'https://oauth.vk.com/authorize?client_id=7230720&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.103'

class VkUser():
    def __init__(self, id):
        self.id = str(id)
        method_name = 'users.get'
        params = {
            'user_ids': self.id,
            'fields' : 'bdate,city,domain',
            'access_token': ACCESS_TOKEN,
            'v': V_API
        }
        response = requests.get(URL+method_name, params=params)
        try:
            self.first_name = response.json()['response'][0]['first_name']
        except:
            self.first_name = None
        try:
            self.last_name = response.json()['response'][0]['last_name']
        except:
            self.last_name = None
        try:
            self.bdate = response.json()['response'][0]['bdate']
        except:
            self.bdate = None
        try:
            self.domain = response.json()['response'][0]['domain']
        except:
            self.domain = 'id'+ self.id
        try:
            self.city = response.json()['response'][0]['city']['title']
        except:
            self.city = None
        self.friend_list = []

    def __str__(self):
            return f'https://vk.com/{self.domain}'

    def __and__(self, other):
        self_set = set(self.all_friends().keys())
        other_set = set(other.all_friends().keys())
        mutual_friends = []
        for user in (self_set & other_set):
            mutual_friends.append(VkUser(user))
        return mutual_friends

    def get_friend_list(self):
# Возвращает список друзей где каждый элемент экземляр класса VkUser
        method_name = 'friends.get'
        params = {
            'user_id' : self.id,
            'order' : 'name',
            'access_token': ACCESS_TOKEN,
            'v': V_API
        }
        response = requests.get(URL+method_name, params=params)
        friends_list = response.json()['response']['items']
        users_obj_list = []
        for friend in friends_list:
            users_obj_list.append(VkUser(friend))
        self.friend_list = users_obj_list
        return users_obj_list

    def all_friends(self):
        method_name = 'friends.get'
        params = {
            'user_id' : self.id,
            'order' : 'name',
            'fields' : 'nickname',
            'access_token': ACCESS_TOKEN,
            'v': V_API
        }
        all_friend = {}
        response = requests.get(URL+method_name, params=params)
        for user in response.json()['response']['items']:
            all_friend[user['id']] = f'{user["first_name"]} {user["last_name"]}'
        return all_friend

    def info(self):
        print(f'Ссылка на пользователя: https://vk.com/{self.domain}\n{self.first_name} {self.last_name}')
        if self.bdate:
            print(f'День рождения: {self.bdate}')
        if self.city:
            print(f'Город: {self.city}')


if __name__ == '__main__':
    user_68648809 = VkUser('68648809')
    user_96852197 = VkUser('96852197')
    for user in user_68648809 & user_96852197:
        user.info()
        print('-' * 25)