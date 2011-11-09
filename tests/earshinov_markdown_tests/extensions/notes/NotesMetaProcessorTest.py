from earshinov_markdown.extensions.notes.NoteMetaProcessor import \
  NotesMetaProcessorExtension
from markdown import Markdown
import re
import unittest


class NotesMetaProcessorTest(unittest.TestCase):

  __FIRST_SECOND_TAGS_RE = r'''
    <div\ class=['"]tags['"]>\s*
      <a\ (
        href=['"]\#['"]\ class=['"]note_tag['"] |
        class=['"]note_tag['"]\ href=['"]\#['"] )
      >first</a>\s*
      <a\ (
        href=['"]\#['"]\ class=['"]note_tag['"] |
        class=['"]note_tag['"]\ href=['"]\#['"] )
      >second</a>\s*
    </div>'''

  def setUp(self):
    self.md = Markdown([NotesMetaProcessorExtension()])


  def test_date_and_tags(self):
    source = \
'''Date: 01.01.2000
Tags: first, second'''
    expectedRe = re.compile(
r'''^
<div\ class=['"]note_meta['"]>\s*
  <div\ class=['"]date['"]>01\.01\.2000</div>\s*
  ''' + self.__FIRST_SECOND_TAGS_RE + r'''\s*
</div>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_tags_and_date(self):
    source = \
'''Tags: first, second
Date: 01.01.2000'''
    expectedRe = re.compile(
r'''^
<div\ class=['"]note_meta['"]>\s*
 ''' + self.__FIRST_SECOND_TAGS_RE + r'''\s*
  <div\ class=['"]date['"]>01\.01\.2000</div>\s*
</div>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_only_date(self):
    source = 'Date: 01.01.2000'
    expectedRe = re.compile(
r'''^
<div\ class=['"]note_meta['"]>\s*
  <div\ class=['"]date['"]>01\.01\.2000</div>\s*
</div>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_only_tags(self):
    source = '''Tags: first, second'''
    expectedRe = re.compile(
r'''^
<div\ class=['"]note_meta['"]>\s*
  ''' + self.__FIRST_SECOND_TAGS_RE + r'''\s*
</div>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_inside_text(self):
    source = '''
First paragraph

Date: 01.01.2000
Tags: first, second

Second paragraph'''
    expectedRe = re.compile(
r'''^
<p>First\ paragraph</p>\s*
<div\ class=['"]note_meta['"]>\s*
  <div\ class=['"]date['"]>01\.01\.2000</div>\s*
  ''' + self.__FIRST_SECOND_TAGS_RE + r'''\s*
</div>\s*
<p>Second\ paragraph</p>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)
