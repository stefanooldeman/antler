import antler
from antler import Crawler

import unittest
from mock import Mock, call, patch


class CrawlerTestCase(unittest.TestCase):

    @patch('antler.Site.request')
    @patch('antler.Crawler.next')
    def _______test_crawler_loops_over_urls(self, next, request):
	request.return_value = '<a href="/about.html">blabla</a>'

	url = "http://google.com"
	c = Crawler(url)
	self.assertEqual(c.visited, {url: 0})
	c.next.assert_called_once_with(['http://google.com/about.html'], 1)

    @patch('antler.Site.count_input', Mock())
    @patch('antler.Site.url', Mock())
    @patch('antler.Site.request')
    @patch('antler.Site.find_a')
    def test_crawler_skips_visited(self, find_a, Site):
        find_a.return_value = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        crawler = Crawler()
        crawler.visited = dict(zip(['a', 'b', 'c'], [0,1,2]))
        crawler.find(['z'])

        self.assertEqual(Site.call_count, 6)
        Site.assert_any_call('d')
        Site.assert_any_call('e')
        Site.assert_any_call('f')
        Site.assert_any_call('g')
        Site.assert_any_call('h')
        Site.assert_any_call('z')

