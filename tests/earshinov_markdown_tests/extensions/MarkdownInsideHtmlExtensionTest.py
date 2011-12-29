from earshinov_markdown.extensions import MarkdownInsideHtmlExtension, \
  HtmlHeaderExtension
from markdown import Markdown
import re
import unittest


class MarkdownInsideHtmlExtensionTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([MarkdownInsideHtmlExtension()])

  def test_html_is_not_parsed_by_default(self):
    source = "<div>**текст**</div>"
    self.assertEqual(source, self.md.convert(source))

  def test_basic(self):
    source = "<div><MD>**текст**</MD></div>"
    expectedRe = "^<div><(b|strong)>текст</(b|strong)></div>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_paragraphs_inside_md(self):
    source = "<div><MD>Первый параграф\n\nВторой параграф</MD></div>"
    expectedRe = "^<div><p>Первый параграф</p>\s*<p>Второй параграф</p></div>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  # KNOWN ISSUE: Если внутри <MD> имеется блок кода, по правилам Markdown
  # отформатированный с помощью отступов и отделённый от остального
  # содержимого <MD> переносами строк (\n\n), этот блок кода отрендерится
  # не в виде <pre></code>, а в виде параграфа.
  #
  # Это происходит потому, что при обработке блоков разметки, разделённых
  # \n\n, код сборки HTML-элемента внутри стандартного HtmlBlockPreprocessor
  # выполняет block.strip(), таким образом убирая отступ первой строки
  # блока кода и портя разметку Markdown.
  #
  # Багрепорт писать не хочется, потому что для нормального HTML-контента
  # выполнение strip() не несёт вреда, а вариант использования Markdown
  # внутри HTML авторы python-markdown, очевидно, не рассматривали.
  #
  # Для обхода описанной ситуации можно вручную писать <pre><code> или
  # использовать другой вариант Markdown-разметки блоков кода, предоставляемый
  # стандартным расширением python-markdown `fenced_code`.
  #
  @unittest.skip
  def test_code_block_inside_md(self):
    source = "<div><MD>Текст\n\n    code\n\nТекст</MD></div>"
    expectedRe = "^<div><p>Текст</p>\s*<pre><code>code</code></pre>\s*<p>Текст</p></div>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_parser_dont_fail_if_md_inside_md(self):
    source = "перед <div><MD>\n<p><MD>**текст**</MD></p>\n</MD></div> после"
    expectedRe = re.compile("^<p>перед <div>.*</div> после</p>$", re.DOTALL)
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_paragraph_is_not_inserted_for_html_surrounded_by_newlines(self):
    source="перед\n\n<table>...</table>\n\nпосле"
    expectedRe = "^<p>перед</p>\s*<table>\.\.\.</table>\s*<p>после</p>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_md_amongst_paragraphs(self):
    source="перед\n\n<p><MD>**текст**</MD></p>\n\nпосле"
    expectedRe = "^<p>перед</p>\s*<p><(b|strong)>текст</(b|strong)></p>\s*<p>после</p>$"
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_references(self):
    source = """
[1]: http://yandex.ru/

<div><MD>[Яндекс][1] | [Google][2]</MD></div>

[2]: http://google.com/
"""
    expectedRe = re.compile(
"""^<div>
  <a\ href=["']http://yandex.ru/["']>Яндекс</a>\ |
  \ <a\ href=["']http://google.com/["']>Google</a>
</div>$""", re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)

  def test_useless_md_without_html(self):
    source = "<MD>**текст**</MD>"

    # оригинальный Markdown конструкцию MD либо интерпретирует
    # как HTML (и оставляет весь исходник без изменений), либо понимает, что это
    # несуществующий HTML-тег и игнорирует его, при этом обрабатывая внутренности
    self.assertRegex(Markdown().convert(source), "^(<MD>\*\*текст\*\*</MD>|<p><MD><(b|strong)>текст</(b|strong)></MD></p>)$")

    # при подключении нашего расширения опять аналогичные варианты: либо Markdown
    # считает, что это HTML, и не вставляет элементы p, либо не считает, что это HTML,
    # и вставляет элементы p
    self.assertRegex(self.md.convert(source), "^(<p>)?<(b|strong)>текст</(b|strong)>(</p>)?$")

  def test_disabling_extension(self):
    # должна быть возможность отключить расширения, меняющие структуру документа,
    # чтобы эти изменения не применялись к содержимому блоков <MD>...</MD>
    md = Markdown([HtmlHeaderExtension(), MarkdownInsideHtmlExtension(
      disabledTreeProcessors=['htmlheader'], disabledPostprocessors=['htmlheader'])])

    source = "# Заголовок 1\n\n<div><MD># Заголовок 2</MD></div>"
    expectedRe = ( "^" +
      # title, добавленный расширением HtmlHeader
      ".*<title>Заголовок 1</title>\s*" +
      "<h1>Заголовок 1</h1>\s*" +
      # если не отключать расширения, title появился бы и здесь
      "<div><h1>Заголовок 2</h1></div>$" )[0]
    self.assertRegex(md.convert(source), expectedRe)

















