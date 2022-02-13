# Импортируем библиотеки для работы с JSON и геокодирования адресов
import geocoder, json
# Импортируем необходимые классы для построения GEOJSON
from geojson import Feature, Point, FeatureCollection

if __name__ == '__main__':
    # Открываем пустой файл с кодировокй utf-8
    file = open('./results/tagged_news.json', encoding="utf-8")
    # Читаем файл и записываем содержимое в виде объекта
    data = json.load(file)
    # Закрываем файл
    file.close()

    # Создаем счетчик обработанных новостей
    processed_news = 0;
    # Создаем пустой список объектов GEOJSON, в который будем записывать точки со свойствами
    features = []
    #Для каждого происшествия:
    for incident in data:
        # Записываем результат работы геокодера в переменную в виде JSON
        result = geocoder.osm(incident['location']).json
        # Если результат не пусто
        if result is not None:
            # Создаем объект типа точка, записываем координаты из объекта "result" и свойства из файла
            incident_point = Feature(geometry=Point((result['lng'], result['lat'])), properties=incident)
            # Добавляем в список объектов GEOJSON точку
            features.append(incident_point)
        # Иначе
        else:
            # Выводим в консоль сообщение о том, что происшествие невозможно геокодировать
            print(f"{incident} \n cannot be geocoded..")
        #Выводим сообщение о количестве обработанных новостей
        print(f"{processed_news} news processed..")
        # Добавляем к счетчику 1
        processed_news += 1
    #Создаем объект класса FeatureCollection из точек происшествий для записи корректного GEOJOSN
    collection = FeatureCollection(features)
    #Открываем пустой файл с кодировкой utf-8
    with open('./results/geocoded_news.geojson', 'w', encoding='utf-8') as file:
            # Конвертируем объект FeatureCollection в текст и записываем в файл
            json.dump(collection, file, ensure_ascii=False)
    # Выводим в консоль информацию о том, что обработка закончена
    print("Processing finished")
