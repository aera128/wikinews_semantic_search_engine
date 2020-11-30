import json

import networkx as nx

from search_engine.models import Builder


def gen_graph(n):
    g = nx.Graph()
    for i in n:
        g.add_node(i.name)
    for i in n:
        for j in i.children:
            g.add_edge(i.name, j.name)
    return g


def get_path_len(g, entity1, entity2):
    return path[entity1][entity2] + 1


def get_sim_path(path_len):
    return 1 / path_len


def get_max_value(q, document):
    maximum = 0
    for i in document:
        path_len = get_path_len(G, q, i)
        sim_path_len = get_sim_path(path_len)
        if sim_path_len > maximum:
            maximum = sim_path_len
    return maximum


def get_mean_value(query, document):
    values = list()
    for q in query:
        h = get_max_value(q, document)
        values.append(h)
    return sum(values) / len(values)


def get_path_length_similarity(entities):
    similarities = dict()
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)
        for article in articles:
            score = get_mean_value(entities, articles[article])
            similarities[article] = score
    return similarities


f = open("data/ontology.json")
data = json.load(f)
builder = Builder()
builder.build_node(data)
nodes = builder.get_nodes()
G = gen_graph(nodes)
path = dict(nx.all_pairs_shortest_path_length(G))
