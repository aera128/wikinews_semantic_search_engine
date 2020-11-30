import csv
import json

f = open('ontology.json', 'w')


def search_child(e, f):
    child = dict()
    with open('ontology.csv') as file:
        reader = csv.reader(file, delimiter=',')
        child["name"] = e
        rows = list()
        for row in reader:
            if row[1] == e:
                rows.append(search_child(row[0], f))
        if len(rows) > 0:
            child["children"] = rows
    return child


entity = "entity"
data = search_child(entity, f)
f.write(json.dumps(data))
f.close()
