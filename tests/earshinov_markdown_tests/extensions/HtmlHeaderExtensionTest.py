from earshinov_markdown.extensions import HtmlHeaderExtension
from markdown import Markdown
import unittest


class HtmlHeaderExtensionTest(unittest.TestCase):

  DOCTYPE_AND_META = '^' + \
    r"""<!DOCTYPE html>\n""" + \
    r"""<meta charset=['"]utf-8['"](>|></meta>| */>)\s*"""

  def setUp(self):
    self.md = Markdown([HtmlHeaderExtension()])

  def test_basic(self):
    source = "Текст"
    expectedRe = self.DOCTYPE_AND_META + "<p>Текст</p>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_title_is_inserted_for_1st_level_heading(self):
    source = "# Заголовок"
    expectedRe = self.DOCTYPE_AND_META + \
      "<title>Заголовок</title>\s*" + \
      "<h1>Заголовок</h1>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_title_not_inserted_if_several_headings(self):
    source = "# Заголовок 1\n\n# Заголовок 2"
    expectedRe = self.DOCTYPE_AND_META + \
      "<h1>Заголовок 1</h1>\s*" + \
      "<h1>Заголовок 2</h1>\s*$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_title_tags_are_property_stripped(self):
    source = "# Заголовок со [ссылкой](http://example.com/) внутри"
    expectedRe = self.DOCTYPE_AND_META + "<title>Заголовок со ссылкой внутри</title>"
    self.assertRegex(self.md.convert(source), expectedRe)
