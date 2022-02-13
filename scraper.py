# Импортируюем библиотеки для выполнения запросов, обработки страниц и работы с JSON
import requests, bs4, json

BASE_URL = "https://69.xn--b1aew.xn--p1ai/news/rubric/287/"
# Параметры фильтрации новостей на сайте
FILTER_PARAMS = {
    "date_from" : "2021-01-01",
    "date_to" : "2022-01-01"
}
# Количество страниц с новостями при заданном фильтре
NUMBER_OF_PAGES = 91

# Заголовки запроса
headers = {
    'authority': 'https://69.xn--b1aew.xn--p1ai/',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

# Функция принимает базовый путь к веб сайту, параметры фильтраци, пеедаваемые в URL и номер отфильтрованной выборки.
# Функция возвращает текст HTML страницы по запросу
def getNewsFromOnePage(base_url, filter_params, page):
    # Создаем сессию для работы с сайтом
    session = requests.session()
    # Делаем HTTP запрос
    response = session.get(f"{base_url}{page}", headers=headers, params=filter_params)
    # Если веб сайт отвечает, возвращаем текст HTML страницы
    if response.status_code == 200:
        print("Success")
        return response.text
    # Если не отвечает, печатаем ошибку
    else:
        print("Bad result")

# Функция принимает текст HTML страницы и переменную типа "список", в которую будут записаны структурированные новости
# Функция записывает в переменную типа список, в которую будут записаны структурированные новости
def getNews(html, news_list):
    # Создаем объект "Soup", с которым можно работать далее
    soup = bs4.BeautifulSoup(html, 'html.parser')
    # Ищем каждый элемент с классом "sl-item" и:
    for element in soup.find_all('div', class_='sl-item'):
        # Записываем в переменную содержимое элемента с классом "sl-item-date"
        date = element.find('div', class_="sl-item-date").text.strip()
        # Записываем в переменную содержимое элемента с классом "sl-item-title"
        headline = element.find('div', class_="sl-item-title").text.strip()
        # Записываем в переменную содержимое элемента с классом "sl-item-text"
        content = element.find('div', class_="sl-item-text").text.strip()
        # Добавляем в список "news_list" объект с датой, заголовком и содержимым новости
        news_list.append({
            "incidentDate" : date,
            "incidentNewsHeadline" : headline,
            "incidentNewsContent" : content
        })



if __name__ == '__main__':
    # Создаем список, в котором будем хранить объекты новостей
    news_list = []
    # Создаем счетчик, по которому будет отслеживать сколько новостей было обработано
    processed_news = 0;
    # Для каждой страниц из заданного количества страниц:
    for page in range(NUMBER_OF_PAGES):
        # Создаем переменную и записываем в нее текст HTML страницы
        html = getNewsFromOnePage(base_url=BASE_URL, filter_params=FILTER_PARAMS, page=page)
        # Запускаем функцию, которая принимает текст страницы и добавляет в объект "news_list" все новости на данной странице
        getNews(html,news_list)
        # Выводим в консоль информацию о том, сколько новосте обработано
        print(f"{processed_news} news processed..")
        # Добавляем к счетчику 1
        processed_news += 1

    # Открываем пустой файл в режиме записи с кодировкой utf-8
    with open('./results/news.json', 'w', encoding='utf-8') as file:
            # Конвертируем список объектов новостей в текст и записываем в файл
            json.dump(news_list, file, ensure_ascii=False)
    # Выводим в консоль информацию о том, что обработка закончена
    print("Processing finished")