from earshinov_markdown.extensions import AutoLinkTargetExtension
from markdown import Markdown
import re
import unittest


class AutoLinkTargetExtensionTest(unittest.TestCase):
  
  BLANK_TARGET_RE = re.compile(r""" target=['"]_blank['"]""")
  
  def assertNewWindow(self, source):
    self.assertRegex(self.md.convert(source), self.BLANK_TARGET_RE)
    
  def assertSameWindow(self, source):
    self.assertNotRegex(self.md.convert(source), self.BLANK_TARGET_RE)
    
  
  def setUp(self):
    self.md = Markdown([AutoLinkTargetExtension()])
    
  def test_absolute_links_in_new_window(self):
    self.assertNewWindow("[](http://example.com/)")
    
  def test_relative_links_in_same_window(self):
    self.assertSameWindow("[](other_page.html)")
    self.assertSameWindow("[](/index.jsp)")
    
  def test_existing_target_not_changed(self):
    ret = self.md.convert("[{@target=my_frame}](http://example.com/)")
    self.assertRegex(ret, r"""target=['"]my_frame['"]""")
    self.assertNotRegex(ret, self.BLANK_TARGET_RE)
    
  @unittest.skip
  def test_manual_markup_is_processed(self):
    self.assertNewWindow("<a href='http://example.com/'/>")