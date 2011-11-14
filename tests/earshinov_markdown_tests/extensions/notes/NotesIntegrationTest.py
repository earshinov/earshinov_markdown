from earshinov_markdown.extensions.notes.NotesExtension import NotesExtension
from markdown import Markdown
import re
import unittest


class NotesIntegrationTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([NotesExtension()])


  def test_basic(self):
    source = '''
# Заметка

Текст заметки с <strong>форматированием</strong>.

Date: 14.11.2011
Tags: заметка, тест

# Вторая заметка

Текст заметки'''
    expectedRe = re.compile(
r'''^
<div\ class=["']note["']>\s*
  <div\ class=["']header["']>\s* (
    <div\ class=["']title["']>Заметка</div>\s* <div\ class=["']date["']>14\.11\.2011</div> |
    <div\ class=["']date["']>14\.11\.2011</div>\s* <div\ class=["']title["']>Заметка</div>
  ) \s*
  </div>\s*
  <div\ class=["']content["']>\s*
    <p>Текст\ заметки\ с\ <strong>форматированием</strong>.</p>\s*
  </div>\s*
  <div\ class=['"]tags['"]>\s*
    <a\ (
      href=['"]\#['"]\ class=['"]note_tag['"] |
      class=['"]note_tag['"]\ href=['"]\#['"] )
    >заметка</a>\s*
    <a\ (
      href=['"]\#['"]\ class=['"]note_tag['"] |
      class=['"]note_tag['"]\ href=['"]\#['"] )
    >тест</a>\s*
  </div>\s*
</div>\s*
<div\ class=["']note["']>\s*
  <div\ class=["']header["']>\s*
    <div\ class=["']title["']>Вторая\ заметка</div>\s*
  </div>\s*
  <div\ class=["']content["']>\s*
    <p>Текст\ заметки</p>\s*
  </div>\s*
</div>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


