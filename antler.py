from re import findall
from urlparse import urlparse
from urlparse import urljoin
import urllib
import sys
import Queue
import threading


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

        if depth == 3:
            print 'stopped {0}'.format({'depth': depth, 'visited': len(self.visited)})
            return False

        childs = []
        threads = []
        for url in urls:
            if self.count > 49:
                print '\nstopped {0}'.format({'depth': depth, 'visited': len(self.visited)})
                return False
            if url in self.visited.keys():
                continue
            site = Site(url)
            site.start()
            threads.append(site)

        # loop over all sites and wait for results
        for site in threads:
            site.join()
            self.update_data(url, site.count_input())
            childs.extend(site.find_a())

        if childs:
            self.next(childs, depth+1)

        return True


class Site(threading.Thread):

    # defined here, for test mocking
    url = None

    def __init__(self, url):
        super(Site, self).__init__()
        self.html = ''
        self.url = url
        uri = urlparse(url)
        self.base = uri.scheme + '://' + uri.netloc

    def run(self):
        # write progress output
        sys.stdout.write('.')
        sys.stdout.flush()
        try:
            io = urllib.urlopen(self.url)
        except:
            print '\ncould not open url %s, timeout 1 second' % url
            return ''
        self.html = io.read()

    def count_input(self):
        matches = findall(r'<input\s', self.html)
        return len(matches)

    def find_a(self):
        # filtering and mapping
        out = []
        results = findall(r'<a.*?href="(.*?)"', self.html)
        for href in results:
            if len(href) > 0:
                if href[0] in ['#', '?'] or href.startswith('javascript'):
                    continue

                url = urljoin(self.base, href)
                out.append(url)

        return out
