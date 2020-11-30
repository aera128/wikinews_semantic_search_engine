class Node:

    def _init_(self, name=None, children=None):
        self.name = name
        if children is None:
            self.children = list()
        else:
            self.children = children

    def get_name(self):
        return self.name

    def get_children(self):
        tmp = list()
        for i in self.children:
            tmp.append(i.name)
        return tmp


class Builder:
    nodes = list()

    def build_node(self, ob):
        node1 = Node()
        node1.name = ob['name']
        node1.children = list()
        if "children" in ob:
            for children in ob['children']:
                node1.children.append(self.build_node(children))
        self.nodes.append(node1)
        return node1

    def get_nodes(self):
        return self.nodes


class Article:
    def __init__(self, title, score):
        self.title = title
        self.score = round(score, 7)
