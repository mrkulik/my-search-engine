from search_engine.models import *
from search_engine.tweaks.models import *
from django.db.utils import IntegrityError


class IndexEditor:
    def __init__(self, data):
        self.data = data

    def add_words_to_url(self, words, url):
        url, is_created = Url.objects.get_or_create(url=url)
        UrlValue.objects.filter(url=url).delete()
        created_words = set()
        created_indecies = {}
        print(1)
        for word, count in words:
            word_model = get_object_or_None(Word, text=word)
            if not word_model:
                created_words.add(word)

            created_indecies[word] = count
        print(2)
        print([word for word in created_words])
        try:
            Word.objects.bulk_create((Word(text=word) for word in created_words))
            print(3)
            indecies = [UrlValue(url=url, count=count, word=Word.objects.get(text=word))
                        for word, count in created_indecies.items()]
            print(4)
            UrlValue.objects.bulk_create(indecies)
        except IntegrityError:
            print('integrity error at url {}'.format(url))
        print(5)

