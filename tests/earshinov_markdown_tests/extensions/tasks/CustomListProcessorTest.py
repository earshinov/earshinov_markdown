from earshinov_markdown.extensions.tasks.CustomListProcessor import \
  CustomListProcessorExtension
from markdown import Markdown
import unittest
import re


class CustomListProcessorTest(unittest.TestCase):

  def setUp(self):
    self.originalMd = Markdown()
    self.md = Markdown([CustomListProcessorExtension()])


  def test_basic(self):
    source = \
'''
  первый элемент
    вложенный элемент
      дочерний элемент
        дочерний элемент
        соседний элемент
    ещё вложенный элемент
  второй элемент'''
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ элемент<ul>\s*
    <li>вложенный\ элемент<ul>\s*
      <li>дочерний\ элемент<ul>\s*
        <li>дочерний\ элемент</li>\s*
        <li>соседний\ элемент</li>\s*
      </ul>\s*</li>\s*
    </ul>\s*</li>\s*
    <li>ещё\ вложенный\ элемент</li>\s*
  </ul>\s*</li>\s*
  <li>второй\ элемент</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_one_line_list_is_processed(self):
    source = "  элемент"
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>элемент</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_block_without_indent_not_processed(self):
    source = "элемент"
    expectedRe = r"^<p>элемент</p>$"
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_line_breaks_do_not_break_list(self):
    source = \
'''
  первый элемент
    второй элемент
      третий элемент


    четвёртый элемент'''
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ элемент<ul>\s*
    <li>второй\ элемент<ul>\s*
      <li>третий\ элемент</li>\s*
    </ul>\s*</li>\s*
    <li>четвёртый\ элемент</li>\s*
  </ul>\s*</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_other_block_breaks_list(self):
    source = \
'''
  первый элемент
    второй элемент
      третий элемент

-----

    четвёртый элемент'''
    expectedRe = re.compile(
r'''^
<ul>\s*
  <li>первый\ элемент<ul>\s*
    <li>второй\ элемент<ul>\s*
      <li>третий\ элемент</li>\s*
    </ul>\s*</li>\s*
  </ul>\s*</li>\s*
</ul>\s*
<hr(>|\ */>|></hr>)\s*
<ul>\s*
  <li>четвёртый\ элемент</li>\s*
</ul>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_multiline_comments_inside_list(self):
    source = \
'''
  первый <!-- элемент
    дочерний элемент
      дочерний --> элемент после коммента
      вложенный элемент
  второй элемент'''
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ <!--(.|\n)*?-->\ элемент\ после\ коммента<ul>\s*
    <li>вложенный\ элемент</li>\s*
  </ul>\s*</li>\s*
  <li>второй\ элемент</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_markdown_inside_list(self):
    source = "  первый **элемент**"
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ <(b|strong)>элемент</(b|strong)></li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_list_markers(self):
    source = \
'''
  * первый элемент
    - порядковый элемент 1
      | примечание 1
      | примечание 2
    - порядковый элемент 2
  * второй элемент'''
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ элемент<ol>\s*
    <li>порядковый\ элемент\ 1<[uo]l\ class=["']details["']>\s*
      <li>примечание\ 1</li>\s*
      <li>примечание\ 2</li>\s*
    </[uo]l>\s*</li>\s*
    <li>порядковый\ элемент\ 2</li>\s*
  </ol>\s*</li>\s*
  <li>второй\ элемент</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_marker_on_first_line_is_enough(self):
    source = \
'''
  - первый элемент
  второй элемент
  третий элемент'''
    expectedRe = re.compile(
r'''^<ol>\s*
  <li>первый\ элемент</li>\s*
  <li>второй\ элемент</li>\s*
  <li>третий\ элемент</li>\s*
</ol>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_incorrect_markers_on_consequent_lines_not_touched(self):
    source = \
'''
  - первый элемент
  | второй элемент
  - третий элемент
  четвёртый элемент'''
    expectedRe = re.compile(
r'''^<ol>\s*
  <li>первый\ элемент</li>\s*
  <li>| второй\ элемент</li>\s*
  <li>третий\ элемент</li>\s*
  <li>четвёртый\ элемент</li>\s*
</ol>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_markers_on_consequent_lines_not_touched_if_no_marker_on_first_line(self):
    source = \
'''
  первый элемент
  * второй элемент
  - третий элемент
  | четвёртый элемент'''
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый\ элемент</li>\s*
  <li>* второй\ элемент</li>\s*
  <li>- третий\ элемент</li>\s*
  <li>| четвёртый\ элемент</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_incorrect_outdent_beyond_first_column(self):
    source = \
'''
    первый
  второй
'''
    expectedRe = re.compile(
r'''^
<ul>\s*
  <li>первый</li>\s*
</ul>\s*
<ul>\s*
  <li>второй</li>\s*
</ul>\s*
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)


  def test_incorrect_outdent_inside_list(self):
    source = \
'''
  первый
    второй
        третий
      четвёртый'''
    # Внутри одного LI ("второй") создаётся два UL: для элементов "третий" и четвёртый"
    expectedRe = re.compile(
r'''^<ul>\s*
  <li>первый<ul>\s*
    <li>второй
      <ul>\s*
        <li>третий</li>\s*
      </ul>\s*
      <ul>\s*
        <li>четвёртый</li>\s*
      </ul>\s*
    </li>\s*
  </ul>\s*</li>\s*
</ul>$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)