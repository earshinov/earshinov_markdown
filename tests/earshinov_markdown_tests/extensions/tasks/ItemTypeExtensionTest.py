from earshinov_markdown.extensions.tasks.ItemTypeExtension import ItemTypeExtension
from markdown import Markdown
import unittest


class ItemTypeExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([ItemTypeExtension()])

  def test_beginning(self):
    source = "* [deferred] элемент списка";
    expectedRe = r"""^<ul>\s*<li class="type_deferred">элемент списка</li>\s*</ul>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_middle(self):
    source = "* элемент [wait] списка";
    expectedRe = r"""^<ul>\s*<li class="type_wait">элемент +списка</li>\s*</ul>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_end(self):
    source = "* элемент списка [freetime]";
    expectedRe = r"""^<ul>\s*<li class="type_freetime">элемент списка *</li>\s*</ul>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_unknown_is_not_replaced(self):
    source = "* элемент [списка]";
    expectedRe = r"""^<ul>\s*<li>элемент \[списка\]</li>\s*</ul>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_references_not_messed_up(self):
    source = "Тестовая [freetime][deferred] ссылка\n\n[deferred]: http://example.com"
    expectedRe = r"""^<p>Тестовая <a href=["']http://example.com["']>freetime</a> ссылка</p>$"""
    self.assertRegex(self.md.convert(source), expectedRe)