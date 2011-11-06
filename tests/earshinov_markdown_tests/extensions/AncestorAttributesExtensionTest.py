from earshinov_markdown.extensions import AncestorAttributesExtension
from markdown import Markdown
import unittest


class Test(unittest.TestCase):

  def setUpMarkdown(self):
    AncestorAttributesExtension.patchMarkdownGlobals()
    return Markdown([AncestorAttributesExtension()])


  def test_self_attribute_still_works(self):
    source = "текст {@class=para}"
    expectedRe = r"""^<p class=['"]para['"]>текст *</p>$"""
    originalRet = Markdown().convert(source)

    md = self.setUpMarkdown()
    ret = md.convert(source)
    self.assertEqual(originalRet, ret)
    self.assertRegex(ret, expectedRe)

  def test_parent_attribute(self):
    md = self.setUpMarkdown()
    source = "* элемент списка {^@class=list}"
    expectedRe = r"""^<ul class=['"]list['"]>\s*<li>элемент списка *</li>\s*</ul>$"""
    self.assertRegex(md.convert(source), expectedRe)

  def test_useless_grandparent_attribute(self):
    md = self.setUpMarkdown()
    source = "* [Ссылка {^^@class=list}](http://example.com/)"
    expectedRe = r"""^<ul class=['"]list['"]>"""
    self.assertRegex(md.convert(source), expectedRe)

  def test_space_stripped_if_first_element(self):
    md = self.setUpMarkdown()
    source = "* {^@class=list} элемент списка"
    #                         ^
    # этот пробел должен -----|
    # отсутствовать в результирующей вёрстке -------|
    #                                               V
    expectedRe = r"""^<ul class=['"]list['"]>\s*<li>элемент списка</li>\s*</ul>$"""
    self.assertRegex(md.convert(source), expectedRe)