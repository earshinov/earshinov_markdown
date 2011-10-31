from earshinov_markdown.extensions import AncestorAttributesExtension
from markdown import Markdown
import unittest


class ExtensionsIntegrationTests(unittest.TestCase):

  def test_ancestor_attribute_for_dl(self):
    '''
    Используем одновременно наше расширение AncestorAttributesExtension
    и поставляемое вместе с python-markdown расширение def_list
    для разметки definition lists
    '''
    AncestorAttributesExtension.patchMarkdownGlobals()
    md = Markdown(['def_list', AncestorAttributesExtension()])
    source = "{^@class=dl} Term\n:    Definition"
    expectedRe = r"""^<dl class=['"]dl['"]>\s*<dt>Term</dt>\s*<dd>Definition</dd>\s*</dl>$"""
    self.assertRegex(md.convert(source), expectedRe)