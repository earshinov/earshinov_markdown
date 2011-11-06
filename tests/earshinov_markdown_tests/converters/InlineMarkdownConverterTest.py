from .ConverterMock import ConverterMock
from earshinov_markdown.converters import InlineMarkdownConverter
import unittest


class InlineMarkdownConverterTest(unittest.TestCase):

  def setUp(self):
    self.dummy = ConverterMock()
    self.converter = InlineMarkdownConverter(self.dummy)

  def test_basic(self):
    '''
    InlineMarkdownConverter должен заменять куски разметки
    Markdown, внедрённые в другой документ
    '''
    source = \
      "<!-- START MARKDOWN -->Начало<!-- END MARKDOWN -->\n\n" + \
      "Некоторый <!-- START MARKDOWN -->текст<!-- END MARKDOWN --> в середине\n\n" + \
      "<!-- START MARKDOWN -->\nМногострочный\n\nтекст\n<!-- END MARKDOWN -->\n\n" + \
      "<!-- START MARKDOWN -->Конец<!-- END MARKDOWN -->"
    expected = \
      "{{{Начало}}}\n\n" + \
      "Некоторый {{{текст}}} в середине\n\n" + \
      "{{{\nМногострочный\n\nтекст\n}}}\n\n" + \
      "{{{Конец}}}"
    self.assertEqual(expected, self.converter.convert(source))