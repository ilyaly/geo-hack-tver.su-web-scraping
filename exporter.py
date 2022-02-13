import geocoder, json
from geojson import Feature, Point, FeatureCollection

if __name__ == '__main__':
    # Opening JSON file
    file = open('./results/tagged_news.json', encoding="utf-8")

    # returns JSON object as
    # a dictionary
    data = json.load(file)
    # Closing file
    file.close()

    processed_news = 0;
    features = []

    for incident in data:
        result = geocoder.osm(incident['location']).json
        if result is not None:
            incident_point = Feature(geometry=Point((result['lng'], result['lat'])), properties=incident)
            features.append(incident_point)
        else:
            print(f"{incident} \n cannot be geocoded..")
        print(f"{processed_news} news processed..")
        processed_news += 1

    collection = FeatureCollection(features)

    with open('./results/geocoded_news.geojson', 'w', encoding='utf-8') as file:
            json.dump(collection, file, ensure_ascii=False)
    print("Processing finished")
