import math

from search_engine.path_length_similarity import *


def gen_digraph():
    di_g = nx.DiGraph()
    for i in nodes:
        di_g.add_node(i.name)
    for i in nodes:
        for j in i.children:
            di_g.add_edge(i.name, j.name)
    return di_g


def get_entity_frequency():
    d = dict()
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


def get_frequency():
    freq = 0
    for i in entities_frequency:
        freq = freq + entities_frequency[i]
    return freq


def get_concepts_frequency():
    dictionary = dict()
    for i in nodes:
        if i.name in entities_frequency:
            dictionary[i.name] = entities_frequency[i.name]
        else:
            for j in nx.descendants(graph, i.name):
                if j in entities_frequency:
                    if i.name in dictionary:
                        dictionary[i.name] += entities_frequency[j]
                    else:
                        dictionary[i.name] = entities_frequency[j]
    return dictionary


def get_info_content():
    infos = dict()
    probabilities = dict()
    for i in nodes:
        p = every_concept_frequency[i.name] / N
        probabilities[i.name] = p
    for i in probabilities:
        if probabilities[i] > 0:
            infos[i] = abs(math.log(probabilities[i]))
        else:
            infos[i] = 0
    return infos


def get_similarity(e1, e2):
    entities = (e1, e2)
    if entities in lowes_common_ancestor:
        lca = lowes_common_ancestor[(e1, e2)]
    else:
        lca = lowes_common_ancestor[(e2, e1)]

    return info_content[lca]


def get_max_value_content(q, document):
    maximum = 0
    for i in document:
        similarity = get_similarity(q, i)
        if similarity > maximum:
            maximum = similarity
    return maximum


def get_mean_content(query, document):
    content = list()
    for q in query:
        h = get_max_value_content(q, document)
        content.append(h)
    return sum(content) / len(content)


def get_semantic_content_similarity(entities):
    similarities = dict()
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)
        for article in articles:
            score = get_mean_content(entities, articles[article])
            similarities[article] = score
    return similarities


nodes = builder.get_nodes()
graph = gen_digraph()
entities_frequency = get_entity_frequency()
N = get_frequency()
every_concept_frequency = get_concepts_frequency()
info_content = get_info_content()
lowes_common_ancestor = dict(nx.all_pairs_lowest_common_ancestor(graph))
