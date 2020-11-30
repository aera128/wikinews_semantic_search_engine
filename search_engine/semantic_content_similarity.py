import math

from search_engine.pathlength_similarity import *

nodes = builder.get_nodes()


def gen_digraph():
    di_g = nx.DiGraph()
    for i in nodes:
        di_g.add_node(i.name)
    for i in nodes:
        for j in i.children:
            di_g.add_edge(i.name, j.name)
    return di_g


def get_entity_frequency():
    d = {}
    with open('data/article_typeid.json') as article_type:
        articles = json.load(article_type)

        for i in articles:
            for j in articles[i]:
                if j in d:

                    d[j] = d[j] + 1
                else:
                    d[j] = 1

    with open("data/typeid_name_wordnet.json") as wordnet:
        words = json.load(wordnet)
        for i in words:
            if i not in d:
                d[i] = 0

    return d


def frequency():
    freq = 0
    for i in entitiesFrequency:
        freq = freq + entitiesFrequency[i]
    return freq


def get_concepts_frequency():
    dictionary = {}
    for i in nodes:
        if i.name in entitiesFrequency:

            dictionary[i.name] = entitiesFrequency[i.name]
        else:
            for j in nx.descendants(graph, i.name):
                if j in entitiesFrequency:
                    if i.name in dictionary:
                        dictionary[i.name] += entitiesFrequency[j]
                    else:
                        dictionary[i.name] = entitiesFrequency[j]

    return dictionary


# P(c)
def get_proba():
    probabilities = {}
    for i in nodes:
        p = everyConceptFrequency[i.name] / N
        probabilities[i.name] = p
    return probabilities


# -log P(c)
def get_info_content():
    informations = {}
    probabilities = get_proba()
    for i in probabilities:
        if probabilities[i] > 0:
            informations[i] = abs(math.log(probabilities[i]))
        else:
            informations[i] = 0
    return informations


# Resnik Method
def get_similarity(e1, e2):
    tup = (e1, e2)
    if tup in lowestCommonAncestor:
        lca = lowestCommonAncestor[(e1, e2)]
    else:
        lca = lowestCommonAncestor[(e2, e1)]

    return informationContent[lca]


def get_max_value_content(q, document):
    highest = 0
    for i in document:
        similarity = get_similarity(q, i)
        if similarity > highest:
            highest = similarity
    return highest


def get_mean_content(query, document):
    liste = []
    for q in query:
        h = get_max_value_content(q, document)
        liste.append(h)
    return sum(liste) / len(liste)


def get_semantic_content_similarity(entities):
    dico = {}
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)

        for article in articles:
            score = get_mean_content(entities, articles[article])
            dico[article] = score
    return dico


graph = gen_digraph()
entitiesFrequency = get_entity_frequency()
N = frequency()
everyConceptFrequency = get_concepts_frequency()
informationContent = get_info_content()
lowestCommonAncestor = dict(nx.all_pairs_lowest_common_ancestor(graph))
