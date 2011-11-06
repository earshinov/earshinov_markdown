from earshinov_markdown.extensions.tasks.ListSeparatorExtension import \
  ListSeparatorExtension
from markdown import Markdown
import unittest


class ListSeparatorExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([ListSeparatorExtension()])

  def test_basic(self):
    source = "* -----\n\n-----";
    expectedRe = r"""^<ul>\s*<li class=["']separator["'](>| */>|></li>)\s*</ul>\s*<hr(>| */>|></hr>)$"""
    self.assertRegex(self.md.convert(source), expectedRe)
