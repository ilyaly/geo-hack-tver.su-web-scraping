#Импортируем библиотеку для работы с JSON
import json
# Из библиотеки natasha импортируем необходимые для анализа текста классы
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)

# Определяем классы происшествий и соответствующие им ключевые слова
INCIDENTS_CLASSES = {
    "убийство" : ["убийство", "смерть"],
    "кража" : ["кража", "похищение", "грабитель"],
    "мошенничество" : ["обман", "мошенник", "мошенничество"],
    "угон" : ["угон"],
    "побои" : ["побои","драка","избиения"],
    "наркотики" : ["наркотики"]
}


# Создаем объект для сегментации текста на токены
segmenter = Segmenter()
# Создаем объект для морфологического анализа текста
morph_vocab = MorphVocab()
#Создаем объект для обработки новостей
emb = NewsEmbedding()
#Создаем объект для тэгирования по морфологии
morph_tagger = NewsMorphTagger(emb)
# Создаем обработчик синтаксиса
syntax_parser = NewsSyntaxParser(emb)
# Создаем семантический классификатор
ner_tagger = NewsNERTagger(emb)

#Создаем извлекатели имен, дат, денег и адресов
names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)

# Определяем функцию, принимающую объект типа doc и возвращающую местоположение
def getLocation(doc):
    # Создаем пустой список местоположений
    raw_location = []
    # Для каждого найденного фрагмента текста:
    for span in doc.spans:
        # Если тип фрагмента - топоним:
        if (span.type == 'LOC'):
            # Добовляем фрагмент в список
            raw_location.append(span.normal)
        # Иначе
        else:
            # Добавляем в список пустой объект
            raw_location.append(None)
    # Приводим список к строке, с разделителем запятая, что-бы ее можно было передать в геокодер
    location = ",".join(raw_location)
    # Возвращаем местоположение
    return location

# Определяем функцию, принимающую объект типа doc и возвращающую тип происшествия
def getIncidentType(doc):
    # Для каждого слова/знака препинания в тексте:
    for token in doc.tokens:
        # Приводим его к нормальной форме
        token.lemmatize(morph_vocab)
        # Для каждого класса происшествия
        for incident_class in INCIDENTS_CLASSES:
            # Записываем список его ключевых слов
            examples = INCIDENTS_CLASSES[incident_class]
            # Если в тексте найдено слово совподающее с одним из ключевых слов данног просшествия
            if token.lemma in examples:
                # Возврашаем класс инцедента
                return incident_class

if __name__ == '__main__':
    # Открываем пустой файл с кодировокй utf-8
    file = open('./results/news.json', encoding="utf-8")

    # Читаем файл и записываем содержимое в виде объекта
    data = json.load(file)
    # Закрываем файл
    file.close()

    # Создаем счетчик обработанных новостей
    processed_news = 0;
    # Создаем пустой список обработанных новостей
    processed_news_list = []
    #Для каждой новости
    for incident in data:
        # Создаем из ее заголовка объект типа Doc, для дальнейшего анализа
        doc = Doc(incident['incidentNewsHeadline'])
        # Сегментируем тект на слова/знаки препинания
        doc.segment(segmenter)
        # Определяем морфологию составляющих текста
        doc.tag_morph(morph_tagger)
        # Определяем синтаксис составляющих текста
        doc.parse_syntax(syntax_parser)
        # Определяем семантические свойства составляющих текста
        doc.tag_ner(ner_tagger)

        # В список обработанных новостей добавляем объект с ее:
        processed_news_list.append({
            # Датой из файла
            "incidentDate": incident['incidentDate'],
            # Заголовком из файла
            "incidentNewsHeadline": incident['incidentNewsHeadline'],
            # Содержимым из файла
            "incidentNewsContent": incident['incidentNewsContent'],
            # Типом, получаемым в результате работы функции
            "incidentType": getIncidentType(doc),
            # Местоположением, получаемым в результате работы функции
            "incidentLocation" : getLocation(doc)
        })
        # Выводим количестве обработанных новостей
        print(f"{processed_news} news processed..")
        # Прибавляем к счетчику 2
        processed_news += 1
    # Открываем пустой файл в режиме записи с кодировкой utf-8
    with open('./results/tagged_news.json', 'w', encoding='utf-8') as file:
            # Конвертируем список объектов новостей в текст и записываем в файл
            json.dump(processed_news_list, file, ensure_ascii=False)
    # Выводим в консоль информацию о том, что обработка закончена
    print("Processing finished")