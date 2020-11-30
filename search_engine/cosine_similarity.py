import csv
import json

from sklearn.metrics.pairwise import cosine_similarity


def format_entity(entities):
    for i in range(0, len(entities)):
        if "." in entities[i]:
            entities[i] = entities[i].split(".")[1]
    return entities


def get_child_entity(entities):
    sub_entities = list()

    def get_leaves(e):
        with open('data/ontology.csv') as file:
            reader = csv.reader(file, delimiter=',')
            found = False
            for row in reader:
                if row[1] == e:
                    found = True
                    get_leaves(row[0])

            if not found:
                sub_entities.append(e)

    for entity in entities:
        get_leaves(entity)
    sub_entities = format_entity(sub_entities)
    return sub_entities


def get_wordnet(entities):
    wordnet_types = list()
    with open('data/typeid_name_wordnet.json') as typeid_name_wordnet:
        wordnet = json.load(typeid_name_wordnet)
        for e in entities:
            for w in wordnet.values():
                if e == w["name"]:
                    wordnet_types.append(w["type"])
                    break
    return wordnet_types


def get_query_vector(wordnet):
    vector = list()
    with open('data/dimension_name.txt') as dimension_name:
        lines = dimension_name.readlines()
        for line in lines:
            found = False
            for w in wordnet:
                if w == line.strip():
                    found = True
                    break
            if found:
                vector.append(1)
            else:
                vector.append(0)
    return vector


def get_cosine_similarity(query_vector):
    results = dict()
    with open('data/article_vector.json') as article_vector:
        articles = json.load(article_vector)
        for (k, v) in articles.items():
            cos = cosine_similarity([query_vector], [v])
            if cos > 0:
                results[k] = float(cos[0][0])
    return results
