from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, ListView, View
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http.response import HttpResponseRedirect
from .parser.parser import start_worker
from .parser.Search import *
from .models import UrlValue, Url
from .forms import UrlValueForm


# Create your views here.

MAX_FILE_SIZE = 1024 * 30  # 30 kb

class Search(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        self.request = request
        if 'query' not in request.GET:
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        request = self.request
        query = request.GET['query']
        query = process_query(query)
        urls = search(query)
        paginator = Paginator(urls, 25)
        page = request.GET.get('page', 1)
        try:
            context['urls'] = paginator.page(page)
        except PageNotAnInteger:
            context['urls'] = paginator.page(1)
        except EmptyPage:
            context['urls'] = paginator.page(1)
        context['query'] = " ".join(query)
        return context


class ParseView(TemplateView):
    template_name = 'parse.html'

    def handle_file(self, file):
        print('handle file')
        data = file.read(MAX_FILE_SIZE)
        data = data.decode('utf-8')
        data = data.split('\n')
        print(data)
        return data

    def post(self, request, *args, **kwargs):
        urls = []
        if 'url' in request.POST:
            urls.append(request.POST['url'])
        print(request.FILES.keys())
        if 'file' in request.FILES:
            urls.extend(self.handle_file(request.FILES['file']))
        try:
            depth = int(request.POST.get('depth_limit', 1))
        except ValueError:
            depth = 1
        try:
            width = int(request.POST.get('width_limit', 1))
        except ValueError:
            width = 1
        start_worker(urls, depth=depth, width=width)
        return HttpResponseRedirect('/')


class GetUrlListView(ListView):
    template_name = 'url_list.html'
    model = Url
    context_object_name = 'urls'
    paginate_by = 50


class GetUrlValueListView(ListView):
    template_name = 'index_list.html'
    context_object_name = 'indecies'
    paginate_by = 50

    def get_queryset(self):
        url = get_object_or_404(Url, id=int(self.args[0]))
        return UrlValue.objects.filter(url=url)


class EditUrlValueView(TemplateView):
    template_name = 'url_value_edit.html'

    def post(self, request, *args, **kwargs):
        form = UrlValueForm(data=request.POST)
        if form.is_valid():
            form_id = form.cleaned_data['id']
            form_word = form.cleaned_data['word']
            form_count = form.cleaned_data['count']
            form_url = form.cleaned_data['url']

            url, state = Url.objects.get_or_create(url=form_url)
            word, state = Word.objects.get_or_create(text=form_word)
            if form_id == -1:
                index = UrlValue()
            else:
                index = get_object_or_404(UrlValue, id=form_id)
            index.url, index.word, index.count = url, word, form_count
            index.save()
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(EditUrlValueView, self).get_context_data(**kwargs)
        if self.args[0] == 'create':
            context['urlvalue'] = {'id': -1}
        else:
            context['urlvalue'] = get_object_or_404(UrlValue, id=int(self.args[0]))
        return context


def index_page(request):
    return render_to_response("index.html")
