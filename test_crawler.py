import antler
from antler import Crawler

import unittest
from mock import Mock, call, patch


class CrawlerTestCase(unittest.TestCase):

    @patch('antler.Site.run')
    @patch('antler.Crawler.next')
    def _______test_crawler_loops_over_urls(self, next, run):
	run.return_value = '<a href="/about.html">blabla</a>'

	url = "http://google.com"
	c = Crawler(url)
	self.assertEqual(antler.isited, {url: 0})
	c.next.assert_called_once_with(['http://google.com/about.html'], 1)

    @patch('antler.Site.count_input', Mock(return_value=0))
    @patch('antler.Site.url', Mock())
    @patch('antler.Site.find_a')
    def test_crawler_skips_visited(self, find_a):
        find_a.return_value = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        crawler = Crawler()

        antler.visited = ['a', 'b', 'c']
        crawler.find(['z'])

        self.assertEqual(find_a.call_count, 6)
        #run.assert_any_call('d')
        #run.assert_any_call('e')
        #run.assert_any_call('f')
        #run.assert_any_call('g')
        #run.assert_any_call('h')
        #run.assert_any_call('z')

