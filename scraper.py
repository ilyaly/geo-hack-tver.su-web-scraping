import requests, bs4, json

BASE_URL = "https://69.xn--b1aew.xn--p1ai/news/rubric/287/"
FILTER_PARAMS = {
    "date_from" : "2021-01-01",
    "date_to" : "2022-01-01"
}
NUMBER_OF_PAGES = 91

headers = {
    'authority': 'www.kith.com',
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

def getNewsFromOnePage(base_url, filter_params, page):

    session = requests.session()

    response = session.get(f"{base_url}{page}", headers=headers, params=filter_params)

    if response.status_code == 200:
        print("Success")
        return response.text
    else:
        print("Bad result")


def getNews(html, news_list):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for element in soup.find_all('div', class_='sl-item'):
        date = element.find('div', class_="sl-item-date").text.strip()
        headline = element.find('div', class_="sl-item-title").text.strip()
        content = element.find('div', class_="sl-item-text").text.strip()
        news_list.append({
            "incidentDate" : date,
            "incidentNewsHeadline" : headline,
            "incidentNewsContent" : content
        })
    return



if __name__ == '__main__':
    news_list = []
    processed_news = 0;
    for page in range(NUMBER_OF_PAGES):
        html = getNewsFromOnePage(base_url=BASE_URL, filter_params=FILTER_PARAMS, page=page)
        getNews(html,news_list)
        print(f"{processed_news} news processed..")
        processed_news += 1

    with open('./results/news.json', 'w', encoding='utf-8') as file:
            json.dump(news_list, file, ensure_ascii=False)
    print("Processing finished")