from earshinov_markdown.extensions import CodeNewlinesRemovalExtension
from markdown import Markdown
import unittest


class CodeNewlinesRemovalExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([CodeNewlinesRemovalExtension()])

  def test_basic(self):
    source = '''<pre><code>\nНекоторый код, напечатанный на новой строке\n</code></pre>'''
    expected = '''<pre><code>Некоторый код, напечатанный на новой строке</code></pre>'''
    self.assertEqual(expected, self.md.convert(source))

  def test_attributes_are_preserved(self):
    source = '''<pre id='id'><code class='class'>\n...\n</code></pre>'''
    expected = '''<pre id='id'><code class='class'>...</code></pre>'''
    self.assertEqual(expected, self.md.convert(source))