from django import forms


class UrlValueForm(forms.Form):
    word = forms.CharField(max_length=100)
    url = forms.URLField()
    count = forms.IntegerField()
    id = forms.IntegerField()
