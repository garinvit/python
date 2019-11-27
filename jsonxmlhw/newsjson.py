import json
import  xml.etree.ElementTree as ET

def make_text(filename, format='auto'):
    if format == 'auto':
        if filename[-4::] =='json':
            format = 'json'
        elif filename[-3::]=='xml':
            format = 'xml'
        else:
            print('Неизвестный формат')
    if format not in ['json', 'xml']:
        return None
    print(format)
    all_news = ''
    if format == 'json':
        with open(filename, encoding='utf8') as f:
            data = json.load(f)
        if format == 'json':
            for new in data["rss"]["channel"]["items"]:
                all_news += new.get("description") + ' '
    elif format == 'xml':
        tree = ET.parse(filename)
        root = tree.getroot()
        news = root.findall('channel/item/description')
        for new in news:
            all_news += new.text + ' '
    return all_news

def top_words(text, len_word=6, top_len=10):
    all_words = [word.lower() for word in text.split(' ') if len(word) >= len_word]
    all_words.sort()
    counts = {}
    for word in all_words:
        if word in counts.keys():
            counts[word] += 1
        else:
            counts[word] = 1
    reverse_count = {}
    for i in range(len(all_words), 0, -1):
        word_list = []
        for word in counts.keys():
            if counts.get(word) == i:
                word_list.append(word)
        if word_list:
            reverse_count[i] = word_list
    print(f'Топ {top_len} наиболее часто встречающихся слов в тексте')
    counter = 1
    for word in reverse_count.keys():
        if counter == top_len + 1:
            break
        print(f'{counter} место слово которое встречается {word} раз:', end='')
        for i in reverse_count[word]:
            print(i, end=' ')
        print('')
        counter += 1


if __name__ == '__main__':
    json_text = make_text('newsafr.json')
    xml_text = make_text('newsafr.xml')
    print('Работа с json')
    top_words(json_text)
    print('Работа с xml')
    top_words(xml_text)