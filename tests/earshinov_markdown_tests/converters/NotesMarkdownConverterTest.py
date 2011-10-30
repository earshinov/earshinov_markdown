from .ConverterMock import ConverterMock
from earshinov_markdown.converters import NotesMarkdownConverter
import unittest


class NotesMarkdownConverterTest(unittest.TestCase):
  
  def setUp(self):
    self.maxDiff = 1000 # настройка unittest, чтобы выводил различия в длинных текстах ниже
    self.dummy = ConverterMock()
    self.converter = NotesMarkdownConverter(self.dummy)
    
  def test_basic(self):
    '''
    NotesMarkdownConverter должен запускать парсер markdown
    отдельно для каждого отрезка разметки markdown, начинающегося
    с заголовка первого уровня
    '''
    source = \
      "# Заголовок первого уровня\n\n" + \
      "Второй абзац\n\n" + \
      "## заголовок второго уровня (не учитывается)\n\n" + \
      "Третий абзац\n" + \
      "# Заголовок первого уровня сразу после текста (не учитывается)\n\n" + \
      "# Второй заголовок первого уровня\n\n" + \
      "# Заголовок первого уровня перед текстом (не учитывается)\n" + \
      "Четвёртый абзац\n\n" + \
      "#Какой-то подозрительный заголовок (не учитывается)\n\n" + \
      "# Заголовок раздела без содержимого (учитывается)"
    expected = \
      "{{{# Заголовок первого уровня\n\n" + \
      "Второй абзац\n\n" + \
      "## заголовок второго уровня (не учитывается)\n\n" + \
      "Третий абзац\n" + \
      "# Заголовок первого уровня сразу после текста (не учитывается)\n\n" + \
      "}}}{{{# Второй заголовок первого уровня\n\n" + \
      "# Заголовок первого уровня перед текстом (не учитывается)\n" + \
      "Четвёртый абзац\n\n" + \
      "#Какой-то подозрительный заголовок (не учитывается)\n\n" + \
      "}}}{{{# Заголовок раздела без содержимого (учитывается)}}}";
    self.assertEqual(expected, self.converter.convert(source))
    
  def test_markup_before_first_heading_is_ignored(self):
    source = \
      "Первый абзац\n\n" + \
      "# Заголовок первого уровня\n"
    expected = \
      "{{{# Заголовок первого уровня\n}}}"
    self.assertEqual(expected, self.converter.convert(source))
  