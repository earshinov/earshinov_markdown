from earshinov_markdown.converters import SimpleMarkdownConverter
import unittest


class SimpleMarkdownConverterTest(unittest.TestCase):

  def setUp(self):
    self.converter = SimpleMarkdownConverter()

  def test_basic(self):
    '''SimpleMarkdownConverter должен просто вызывать markdown'''
    source = "Текст"
    expected = "<p>Текст</p>"
    self.assertEqual(expected, self.converter.convert(source))