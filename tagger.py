import json

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


INCIDENTS_CLASSES = {
    "убийство" : ["убийство", "смерть"],
    "кража" : ["кража", "похищение", "грабитель"],
    "мошенничество" : ["обман", "мошенник", "мошенничество"],
    "угон" : ["угон"],
    "побои" : ["побои","драка","избиения"],
    "наркотики" : ["наркотики"]
}



segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)

def getLocation(doc):
    raw_location = []
    for span in doc.spans:
        span.normalize(morph_vocab)
        if (span.type == 'LOC'):
            raw_location.append(span.normal)
    location = ",".join(raw_location)
    return location

def getIncidentType(doc):
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        for incident_class in INCIDENTS_CLASSES:
            examples = INCIDENTS_CLASSES[incident_class]
            if token.lemma in examples:
                return incident_class

if __name__ == '__main__':
    # Opening JSON file
    file = open('./results/news.json', encoding="utf-8")

    # returns JSON object as
    # a dictionary
    data = json.load(file)
    # Closing file
    file.close()

    processed_news = 0;
    news_with_locations_list = []
    #Extracting location info from headlines
    for incident in data:
        doc = Doc(incident['incidentNewsHeadline'])

        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)


        news_with_locations_list.append({
            "incidentDate": incident['incidentDate'],
            "incidentNewsHeadline": incident['incidentNewsHeadline'],
            "incidentNewsContent": incident['incidentNewsContent'],
            "incidentType": getIncidentType(doc),
            "incidentLocation" : getLocation(doc)
        })

        print(f"{processed_news} news processed..")
        processed_news += 1

    with open('./results/tagged_news.json', 'w', encoding='utf-8') as file:
            json.dump(news_with_locations_list, file, ensure_ascii=False)
    print("Processing finished")