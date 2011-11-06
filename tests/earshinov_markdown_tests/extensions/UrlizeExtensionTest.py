from earshinov_markdown.extensions import UrlizeExtension
from markdown import Markdown
import unittest


class UrlizeExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([UrlizeExtension()])

  def test_links_in_angle_brackets_processed(self):
    source = "<http://yandex.ru/>"
    expectedRe = r"""^<p><a href=['"]http://yandex.ru/['"]>http://yandex.ru/</a></p>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_links_starting_with_http_processed(self):
    source = "http://example.com/"
    expectedRe = r"""^<p><a href=['"]http://example.com/['"]>http://example.com/</a></p>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_links_starting_with_www_processed(self):
    source = "www.example.com"
    expectedRe = r"""^<p><a href=['"]http://www.example.com['"]>www.example.com</a></p>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_markdown_links_not_messed_up(self):
    source = "[](http://yandex.ru/)"
    expectedRe = r""" href=['"]http://yandex.ru/['"]"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_manual_links_not_messed_up(self):
    source = "<a href='http://yandex.ru/'>Яндекс</a>"
    expected = "<p>%s</p>" % source
    self.assertEqual(expected, self.md.convert(source))

