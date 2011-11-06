from earshinov_markdown.extensions.tasks.TableMarkupExtension import \
  TableMarkupExtension
from markdown import Markdown
import re
import unittest


class TableMarkupExtensionTest(unittest.TestCase):

  def setUp(self):
    self.originalMd = Markdown()
    self.md = Markdown([TableMarkupExtension()])

  def test_basic(self):

    firstPart = "First part with two paragraphs\n\nThe second paragraph\n\n* A list"
    secondPart = "Second part"

    actual = self.md.convert(
      firstPart + \
      "\n\n-----\n\n" + \
      secondPart)
    expectedRe = \
      r"^<tr>\s*" + \
        r"<td>\s*" + re.escape(self.originalMd.convert(firstPart)) + "\s*</td>\s*" + \
        r"<td>\s*" + re.escape(self.originalMd.convert(secondPart)) + "\s*</td>\s*" + \
      r"</tr>$"""
    self.assertRegex(actual, expectedRe)

  def test_beginning_hr_is_ignored(self):
    source = "-----\n\nТекст"
    expectedRe = r"""^<tr>\s*<td>\s*<p>Текст</p>\s*</td>\s*</tr>$"""
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_ending_hr_is_ignored(self):
    source = "Текст\n\n-----"
    expectedRe = r"""^<tr>\s*<td>\s*<p>Текст</p>\s*</td>\s*</tr>$"""
    self.assertRegex(self.md.convert(source), expectedRe)