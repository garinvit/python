import requests
from pprint import pprint
#  документация https://yandex.ru/dev/translate/doc/dg/reference/translate-docpage/

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

OAUTH_TOKEN = 'AgAAAAAFRf7FAAYA5ado3MqC902Ak66ethrbkU0'
#для получения токена https://oauth.yandex.ru/authorize?response_type=token&client_id=c5de797f68854d968122efa24cd470d5

def save_file_yadisk(filepath, yandex_filepath='app:/new.txt', mode='upload'):
    # mode при значении 'download' скачивает файл с яндекс диска, тогда filepath следует использовтаь как путь для сохранения файла на компьютер
    resources_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    upl_params = {
        'path': yandex_filepath,
        'overwrite': 'true',
    }
    with requests.Session() as session:
        session.headers['Accept'] = "application/json"
        session.headers["Authorization"] = f'OAuth {OAUTH_TOKEN}'
        session.headers["User-Agent"] = 'Netology'
        session.get("https://cloud-api.yandex.net")
        if mode=='upload':
            res = session.get(resources_url, params=upl_params)
            url_for_upload_file = res.json()['href']
            #print(url_for_upload_file)
            session.put(url_for_upload_file, data=open(filepath, 'rb'))
            writen = session.get('https://cloud-api.yandex.net/v1/disk/resources', params={'path': yandex_filepath})
            if writen.status_code == 200:
                print('Файл успешно сохранен на Яндекс.Диске')
        if mode == 'download':
            res = session.get('https://cloud-api.yandex.net/v1/disk/resources/download', params={'path': yandex_filepath})
            url_for_download_file = res.json()['href']
            #print(url_for_download_file)
            with open(filepath, 'wb') as f:
                file = session.get(url_for_download_file)
                f.write(file.content)

def translate_it(mode='t-t', text=None, to_lang='en', from_lang='ru', f_input=None, f_output=None):
    # переменная mode задает режим работы функции
    # 't-t' - перевод текста из переменной text, функция вернет текст перевода
    # 'f-f' - перевод из файла в новый файл
    # 'f-t' - выведет в консоле переведенный текст указанного файла
    # 't-f' - принимает текст из переменной или строки text, перевод сохраняет в файл
    # 'f-ya' - принимает файл, сохраняет его компьютере и на яндекс диске
    # 'ya-f' - скачать файл с яндекс диска. f_input - путь на яндекс диске, f_output - для сохранения на компьютер
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """
    if mode == 'f-t' or mode == 'f-f' or mode == 'f-ya':
        if f_input == None:
            f_input = input('Вы забыли ввести имя входящего файла. Введите сейчас:')
        with open(f_input, encoding='utf8') as f_in:
            text = f_in.read()
    if mode == 'ya-f':
        if f_input == None:
            f_input = input('Вы забыли ввести имя файла на яндекс диске. Введите сейчас:')
    if mode == 't-f' or mode == 'f-f' or mode=='f-ya' or mode=='ya-f':
        if f_output == None:
            f_output = input('Вы забыли ввести имя нового файла. Введите сейчас:')
        if mode=='ya-f':
            return save_file_yadisk(f_output, yandex_filepath=f_input, mode='download')
    if mode == 't-t' or mode == 't-f':
        if text == None:
            text = input('Вы забыли ввести текст. Введите сейчас:')

    params = {
        'key': API_KEY,
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()

    if mode == 't-f' or mode == 'f-f' or mode == 'f-ya':
        with open(f_output, 'w', encoding='utf8') as f_out:
            f_out.write(''.join(json_['text']))
        if mode == 'f-ya':
            save_file_yadisk(f_output,'app:/'+f_output)
    if mode == 't-t' or mode == 'f-t':
        return ''.join(json_['text'])


# print(translate_it('В настоящее время доступна единственная опция — признак включения в ответ автоматически определенного языка переводимого текста. Этому соответствует значение 1 этого параметра.', 'no'))

if __name__ == '__main__':
    save_file_yadisk('DE-RU.txt', 'app:/DE-RU.txt')
    translate_it(mode='f-ya', text=None, to_lang='ru', from_lang='de', f_input='DE.txt', f_output='DE-RUS.txt')
    translate_it(mode='f-ya', text=None, to_lang='ru', from_lang='fr', f_input='FR.txt', f_output='FR-RUS.txt')
    translate_it(mode='f-ya', text=None, to_lang='ru', from_lang='es', f_input='ES.txt', f_output='ES-RUS.txt')
    pprint(translate_it(mode='f-t', text=None, to_lang='ru', from_lang='es', f_input='ES.txt', f_output='ES-RUS.txt'))
    translate_it(mode='t-f', text='Привет, мир!', f_output='EN-RUS.txt')
    save_file_yadisk('file_from_ya.txt','app:/ES-RUS.txt', mode='download')
    translate_it(mode='ya-f', f_input='app:/FR-RUS.txt', f_output='download_from_ya.txt')
