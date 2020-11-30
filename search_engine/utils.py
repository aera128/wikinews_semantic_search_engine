import jsonpickle as jp

from search_engine.models import Article


def get_score(similarities):
    similarities = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    similarities = {k: similarities[k] for k in list(similarities)}
    articles = list()
    for key, value in similarities.items():
        articles.append(Article(key, value))
    return jp.encode(articles, unpicklable=False)
