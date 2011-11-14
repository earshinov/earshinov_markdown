from earshinov_markdown.extensions.notes.NotesMarkupTreeProcessor import \
  NotesMarkupTreeProcessor
from markdown import etree
import re
import unittest


class NotesMarkupTreeProcessorTest(unittest.TestCase):

  def setUp(self):
    self.proc = NotesMarkupTreeProcessor()

  def htmlToString(self, html):
    inputHtml = '<div>' + html + '</div>'
    inputRoot = etree.fromstring(inputHtml)
    outputRoot = self.proc.run(inputRoot)
    outputText = b''.join(etree.tostring(child, encoding="utf-8") for child in outputRoot).decode("utf-8")
    return outputText


  def test_basic(self):
    html = '''
<h1>Первая заметка</h1>
<p>Текст первой заметки</p>
<h1>Вторая заметка</h1>
<p>Текст второй заметки</p>'''
    expectedRe = re.compile(
r'''^
  <div\ class=["']note["']>\s*
    <div\ class=["']header["']>\s*
      <div\ class=["']title["']>Первая\ заметка</div>\s*
    </div>\s*
    <div\ class=["']content["']>\s*
      <p>Текст\ первой\ заметки</p>\s*
    </div>\s*
  </div>\s*
  <div\ class=["']note["']>\s*
    <div\ class=["']header["']>\s*
      <div\ class=["']title["']>Вторая\ заметка</div>\s*
    </div>\s*
    <div\ class=["']content["']>\s*
      <p>Текст\ второй\ заметки</p>\s*
    </div>\s*
  </div>
$''', re.VERBOSE)
    self.assertRegex(self.htmlToString(html), expectedRe)


  def test_content_before_first_heading_is_ignored(self):
    html = '''<p>Текст до первой заметки</p>'''
    self.assertEquals("", self.htmlToString(html))


  def test_text_content_and_markup_is_preserved(self):
    html = '''
<h1>Очень <strong>жирная</strong> заметка</h1>
Текст
<div class="empty"/>
<div class="note_meta"/>
Выделенный <em>курсивом</em> текст'''
    expectedRe = re.compile(
r'''^
<div\ class=["']note["']>\s*
  <div\ class=["']header["']>\s*
    <div\ class=["']title["']>Очень\ <strong>жирная</strong>\ заметка</div>\s*
  </div>\s*
  <div\ class=["']content["']>\s*
    Текст\s*
    <div\ class=["']empty["'] (\ */>|></div>) \s*
    Выделенный\ <em>курсивом</em>\ текст\s*
  </div>\s*
</div>\s*
$''', re.VERBOSE)
    self.assertRegex(self.htmlToString(html), expectedRe)


  def test_note_meta(self):
    html = '''
<h1>Заметка</h1>
Текст
<div class="note_meta">
  <div class="date">01.01.2000</div>
  <div class="tags">
    <a href="#" class="note_tag">метка</a>
  </div>
</div>
Продолжение текста'''
    expectedRe = re.compile(
r'''^
<div\ class=["']note["']>\s*
  <div\ class=["']header["']>\s* (
    <div\ class=["']title["']>Заметка</div>\s* <div\ class=["']date["']>01\.01\.2000</div> |
    <div\ class=["']date["']>01\.01\.2000</div>\s* <div\ class=["']title["']>Заметка</div>
  ) \s*
  </div>\s*
  <div\ class=["']content["']>\s*
    Текст\s+Продолжение\ текста\s*
  </div>\s*
  <div\ class=['"]tags['"]>\s*
    <a\ (
      href=['"]\#['"]\ class=['"]note_tag['"] |
      class=['"]note_tag['"]\ href=['"]\#['"] )
    >метка</a>\s*
  </div>\s*
</div>\s*
$''', re.VERBOSE)
    self.assertRegex(self.htmlToString(html), expectedRe)


  def test_note_meta_in_several_blocks(self):
    html = '''
<h1>Заметка</h1>
Текст
<div class="note_meta">
  <div class="date">01.01.2000</div>
</div>
Продолжение текста
<div class="note_meta">
  <div class="tags">
    <a href="#" class="note_tag">метка</a>
  </div>
</div>
'''
    expectedRe = re.compile(
r'''^
<div\ class=["']note["']>\s*
  <div\ class=["']header["']>\s* (
    <div\ class=["']title["']>Заметка</div>\s* <div\ class=["']date["']>01\.01\.2000</div> |
    <div\ class=["']date["']>01\.01\.2000</div>\s* <div\ class=["']title["']>Заметка</div>
  ) \s*
  </div>\s*
  <div\ class=["']content["']>\s*
    Текст\s+Продолжение\ текста\s*
  </div>\s*
  <div\ class=['"]tags['"]>\s*
    <a\ (
      href=['"]\#['"]\ class=['"]note_tag['"] |
      class=['"]note_tag['"]\ href=['"]\#['"] )
    >метка</a>\s*
  </div>\s*
</div>\s*
$''', re.VERBOSE)
    self.assertRegex(self.htmlToString(html), expectedRe)






