from django.db import models


# Create your models here.

class Word(models.Model):
    text = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.text)


class Url(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return str(self.url)


class UrlValue(models.Model):
    count = models.IntegerField()
    url = models.ForeignKey(Url)
    word = models.ForeignKey(Word)

    def __str__(self):
        return "{} - {} - {}".format(str(self.url), str(self.word), str(self.count))