import json

import networkx as nx


class Node:

    def _init_(self, name=None, children=None):
        self.name = name
        if children is None:
            self.children = []
        else:
            self.children = children

    def get_name(self):
        return self.name

    def get_children(self):
        tmp = []
        for i in self.children:
            tmp.append(i.name)
        return tmp


class Implementation:
    nodes = []

    def build_node(self, ob):

        node1 = Node()
        node1.name = ob['name']
        node1.children = []
        if "children" in ob:
            for children in ob['children']:
                node1.children.append(self.build_node(children))

        self.nodes.append(node1)
        return node1

    def get_nodes(self):
        return self.nodes


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
    highest = 0

    for i in document:
        path_len = get_path_len(G, q, i)

        sim_path_len = get_sim_path(path_len)
        if sim_path_len > highest:
            highest = sim_path_len
    return highest


def get_mean_value(query, document):
    tmp = []
    for q in query:
        h = get_max_value(q, document)

        tmp.append(h)

    return sum(tmp) / len(tmp)


def get_pah_length_similarity(entities):
    d = {}
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)

        for article in articles:
            score = get_mean_value(entities, articles[article])

            d[article] = score

    return d


f = open("data/ontology.json")
data = json.load(f)
builder = Implementation()
builder.build_node(data)

nodes = builder.get_nodes()
G = gen_graph(nodes)
path = dict(nx.all_pairs_shortest_path_length(G))
