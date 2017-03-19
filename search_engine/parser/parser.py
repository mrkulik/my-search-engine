import urllib.request
import re

from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import Counter, defaultdict
from urllib.robotparser import RobotFileParser
from .index import IndexEditor
from threading import Thread


class Parser:
    def __init__(self, *urls, depth=1, width=1):
        self.urls = urls
        self.depth = depth
        self.width = width

        self.robot_dict = {}
        self.depth_urls = {}
        self.visited = set()
        self.current_depth = 1
        self.visit_to = []

    def _fetch_url(self, url):
        try:
            html = urllib.request.urlopen(url).read(1024 * 500)
            print('downloaded', url)
        except TimeoutError:
            return None
        except HTTPError:
            return None
        except URLError:
            print("url error {}".format(url))
            return None
        except ValueError:
            print("value error {}".format(url))
            return None

        return html

    def start(self):
        res = {}
        for url in self.urls:
            self.depth_urls[url] = self.current_depth
        self.visit_to.extend([url for url in self.depth_urls.keys()])
        print(self.visit_to)
        while len(self.visit_to):
            url = self.visit_to.pop(0)
            data = self.process_url(url)
            if data:
                url, text = data
                print(url)
                res[url] = text
                print(text)
        return res

    def process_url(self, url):
        if url not in self.visited and self._check_robot(url):
            print(url, self.depth_urls[url])
            if 0 < self.depth_urls[url] <= self.depth and url not in self.visited:
                page_res = self.run(url)
                self.visited.add(url)
                if page_res:
                    page_url, text, page_urls = page_res
                    page_urls = self.get_correct_urls(page_urls)
                    for add_page_url in page_urls:
                        if add_page_url not in self.depth_urls or \
                           self.depth_urls[add_page_url] > self.depth_urls[url] + 1:
                            self.depth_urls[add_page_url] = self.depth_urls[url] + 1
                        self.visit_to.append(add_page_url)

                    return page_url, text

    def run(self, url):
        html = self._fetch_url(url)
        if html is not None:
            parsed_data = self._parse(html, url)
            if parsed_data is None:
                return None
            text, urls = parsed_data
            return url, text, urls

    def clear_words(self, elems):
        word_regexp = re.compile('\w+', re.UNICODE)
        for elem in elems:
            res = word_regexp.findall(elem)
            if res is not None:
                for word in res:
                    yield word

    def _check_robot(self, url):
        base_url = self.get_base_url(url)
        if not base_url:
            return False
        try:
            if base_url not in self.robot_dict:
                robot_file = RobotFileParser()
                robot_file.set_url(base_url + '/robots.txt')
                robot_file.read()
                self.robot_dict[base_url] = robot_file
            return self.robot_dict[base_url].can_fetch('Yandex', url) or \
                   self.robot_dict[base_url].can_fetch('*', url)
        except (URLError, ValueError):
            return False

    def _parse(self, html, current_url):

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif isinstance(element, Comment):
                return False
            elif str(element) in "\n\t ":
                return False
            return True

        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify().encode('utf-8')
        if soup.html is None:
            return None
        whole_text = soup.findAll(text=True)

        visible_text = filter(visible, whole_text)
        visible_text = self.clear_words(visible_text)
        visible_text = (elem.lower() for elem in visible_text if len(elem) > 2)
        visible_text = (elem.replace('ё', 'е') for elem in visible_text)
        visible_text = Counter(visible_text)
        urls = self._get_all_urls(soup, current_url)
        return visible_text, urls

    def get_correct_urls(self, urls):
        page_urls = [url for url in urls
                     if self._check_robot(url) and
                     url not in self.visited and
                     url not in self.visit_to]

        return page_urls[:self.width]

    def _get_all_urls(self, soup, current_url):
        urls = []
        for url in soup.findAll('a', href=True):
            url = str(url['href'])
            if url.startswith('/'):
                url = current_url + url
            urls.append(url)
        return urls

    def is_correct_url(self, url):
        pass

    @staticmethod
    def get_base_url(url):
        regexp = re.compile(r'^.+?[^/:](?=[?/]|$)')
        base_url = regexp.match(url)
        if base_url:
            return base_url.group()
        else:
            return None


def start_worker(url, depth, width):
    Thread(target=_parse, args=(url, depth, width)).start()


def _parse(url, depth, width):
    parser = Parser(*url, depth=depth, width=width)
    res = parser.start()
    editor = IndexEditor(res)
    for url, words in res.items():
        print("add url " + url)
        editor.add_words_to_url(words.items(), url)
    print("FINISHED")


if __name__ == '__main__':
    p = Parser('http://filmix.net', width=3, depth=3)
    for i in p.start().items():
        print(i)
