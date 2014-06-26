from re import findall
from urlparse import urlparse
from urlparse import urljoin
import urllib
import sys



class Crawler(object):


    def __init__(self, start_url=None):
        """
        collect a dictoinary of visited sites and the the count of <input.. tags.
        """
        self.count = 0
        self.visited = {}
        if start_url:
            self.find([start_url])

    def update_data(self, url, count):
        self.count += 1
        self.visited[url] = count

    def next(self, urls, depth):
        self.find(urls, depth)

    def find(self, urls, depth=0):
        print '\nurls %d depth %d' % (len(urls), depth)

        if depth == 3 or self.count > 49:
            print 'stopped {0}'.format({'depth': depth, 'visited': len(self.visited)})
            return False

        sample = [x for x in urls if x not in self.visited.keys()]
        childs = []
        for url in sample[:50]:
            if self.count > 49:
                print '\nstopped {0}'.format({'depth': depth, 'visited': len(self.visited)})
                return False
            if url in self.visited.keys():
                continue
            site = Site(url)
            body = site.request()
            self.update_data(url, site.count_input(body))
            childs.extend(site.find_a(body))

        if childs:
            self.next(childs, depth+1)


class Site(object):

    # defined here, for test mocking
    url = None

    def __init__(self, url):
        self.url = url
        uri = urlparse(url)
        self.base = uri.scheme + '://' + uri.netloc

    def request(self):
        sys.stdout.write('.')
        sys.stdout.flush()
        io = urllib.urlopen(self.url)
        return io.read()

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
                out.append(url)

        return out
