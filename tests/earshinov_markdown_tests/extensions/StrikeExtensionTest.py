from earshinov_markdown.extensions import StrikeExtension
from markdown import Markdown
import unittest


class StrikeExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([StrikeExtension()])

  def test_basic(self):
    source = "--Вычеркнутый текст--"
    expectedRe = "<s(trike)?>Вычеркнутый текст</s(trike)?>"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_spaces_are_preserved(self):
    source = "-- Вычеркнутый текст --"
    expectedRe = "<s(trike)?> Вычеркнутый текст </s(trike)?>"
    self.assertRegex(self.md.convert(source), expectedRe)
