from collections import defaultdict

from search_engine.models import *


def process_query(query):
    query = query.strip()
    query = query.lower()
    query = query.split()
    query = [word for word in query if len(word) > 2]
    return query


def get_urlvalues(query_list):
    words = Word.objects.filter(text__in=query_list)
    urlvalues = UrlValue.objects.filter(word__in=words)
    return urlvalues


def relevate_urlvalues(urlvalues):
    data = defaultdict(set)
    score = defaultdict(int)
    for urlvalue in urlvalues:
        word = str(urlvalue.word)
        url = str(urlvalue.url)
        if word not in data[url]:
            data[url].add(word)
            score[url] += 500 + urlvalue.count * 10
        else:
            score[url] += 5 + urlvalue.count * 2
    urls = [url for url in score.items()]
    urls.sort(key=lambda x: x[1], reverse=True)
    urls = [url[0] for url in urls]
    return urls


def search(query):
    values = get_urlvalues(query)
    return relevate_urlvalues(values)