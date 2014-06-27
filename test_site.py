import antler
from antler import Site

import unittest
from mock import Mock, call, patch

dummy_html = "<!doctype html><img alt=\"WK Voetbal 2014\" border=\"0\" height=\"225\" src=\"/logos/doodles/2014/world-cup-2014-15-5971113733521408-hp.gif\" title=\"WK Voetbal 2014\" width=\"680\" id=\"hplogo\" onload=\"window.lol&&lol()\"><br></a><br></div><form action=\"/search\" name=\"f\"><table cellpadding=\"0\" cellspacing=\"0\"><tr valign=\"top\"><td width=\"25%\">&nbsp;</td><td align=\"center\" nowrap=\"\"><input name=\"ie\" value=\"ISO-8859-1\" type=\"hidden\"><input value=\"nl\" name=\"hl\" type=\"hidden\"><input name=\"source\" type=\"hidden\" value=\"hp\"><div class=\"ds\" style=\"height:32px;margin:4px 0\"><input style=\"color:#000;margin:0;padding:5px 8px 0 6px;vertical-align:top\" autocomplete=\"off\" class=\"lst\" value=\"\" title=\"Google zoeken\" maxlength=\"2048\" name=\"q\" size=\"57\"></div><br style=\"line-height:0\"><span class=\"ds\"><span class=\"lsbb\"><input class=\"lsb\" value=\"Google zoeken\" name=\"btnG\" type=\"submit\"></span></span><span class=\"ds\"><span class=\"lsbb\"><input class=\"lsb\" value=\"Ik doe een gok\" name=\"btnI\" onclick=\"if(this.form.q.value)this.checked=1; else top.location='/doodles/'\" type=\"submit\"></span></span></td><td class=\"fl sblc\" align=\"left\" nowrap=\"\" width=\"25%\"><a href=\"/advanced_search?hl=nl&amp;authuser=0\">Geavanceerd zoeken</a><a href=\"/language_tools?hl=nl&amp;authuser=0\">Google Taalhulpmiddelen</a></td></tr></table><input id=\"gbv\" name=\"gbv\" type=\"hidden\" value=\"1\"></form><div id=\"gac_scont\"></div><div style=\"font-size:83%;min-height:3.5em\"><br></div><span id=\"footer\"><div style=\"font-size:10pt\"><div style=\"margin:19px auto;text-align:center\" id=\"fll\"><a href=\"/intl/nl/ads/\">Advertentieprogramma's</a><a href=\"http://www.google.nl/intl/nl/services/\">Bedrijfsoplossingen</a><a href=\"https://plus.google.com/117275729676813513015\" rel=\"publisher\">+Google</a><a href=\"/intl/nl/about.html\">Alles over Google</a><a href=\"http://www.google.nl/setprefdomain?prefdom=US&amp;sig=0_4r_ZO3FEUrhPz4rP5aUSwg2cn5g%3D\" id=\"fehl\">Google.com</a></div></div><p style=\"color:#767676;font-size:8pt\">&copy; 2013 - <a href=\"/intl/nl/policies/\">Privacy en voorwaarden</a></p></span></center><div id=xjsd></div><div id=xjsi data-jiis=\"bp\"></body></html>"

antler.urllib.urlopen = Mock()
class IO(object):
    def read(*args, **kwargs):
        return ''
antler.urllib.urlopen.return_value = IO()


class SiteTestCase(unittest.TestCase):

    def setUp(self):
	antler.visited = []

    def test_find_a_returns_all_matches(self):
        site = Site("http://example.com")
        site.run()
        site.html = dummy_html 
        matches = site.find_a()
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 8)

    @patch('antler.findall')
    def test_find_a_filters_out_bad_links(self, findall):
        antler.visited = ['http://example.com/index.html']
	findall.return_value = ['#menu2', '?foo=bar', '/about.html', '', 'javascript:MyFunction();']

        site = Site("http://example.com")
        site.run()
	matches = site.find_a()
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 1)
	self.assertEqual(matches[0], "http://example.com/about.html")

    def test_count_input(self):
	site = Site("http://example.com")
        site.run()
        site.html = dummy_html 
	count = site.count_input()
	self.assertEqual(count, 7)
