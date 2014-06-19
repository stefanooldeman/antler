from re import findall
from urlparse import urlparse
from urlparse import urljoin
import urllib


visited = []


class Site(object):

    def __init__(self, url):
        self.url = url
        uri = urlparse(url)
        self.base = uri.scheme + '://' + uri.netloc

    def count_input(self, body):
        matches = findall(r'<input\s', body)
        return len(matches)

    def find_a(self, body):
        # filtering and mapping
        out = []
        results = findall(r'<a.*?href="(.*?)"', body)
        for href in results:
            if len(href) > 0:
                if href[0] in ['#', '?'] or href.startswith('javascript'):
                    continue

                url = urljoin(self.base, href)
                if url not in visited:
                    out.append(url)

        return out
