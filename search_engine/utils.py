import jsonpickle as jp


def get_score(similarities):
    similarities = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    similarities = {k: similarities[k] for k in list(similarities)}

    articles = []
    for key, value in similarities.items():
        articles.append(Article(key, value))

    return jp.encode(articles, unpicklable=False)


class Article:
    def __init__(self, title, score):
        self.title = title
        self.score = round(score, 7)
