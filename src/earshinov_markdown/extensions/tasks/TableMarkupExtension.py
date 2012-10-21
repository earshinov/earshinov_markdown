from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class TableMarkupTreeProcessor(Treeprocessor):
  '''Оборачивает результаты работы парсера Markdown в элементы tr и td, так чтобы
  список задач можно было оформить в несколько столбцов.  Переход к новому столбцу
  осуществляется там, где в результирующей разметке встречается элемент hr'''

  def run(self, root):
    groups = []
    group = None
    for child in root:
      if child.tag == 'hr':
        group = None
        continue
      if group is None:
        group = []
        groups.append(group)
      group.append(child)

    # делаем в два этапа, чтобы избежать параллельного обхода и модификации
    root.clear()
    tr = etree.SubElement(root, 'tr')
    for group in groups:
      td = etree.SubElement(tr, 'td')
      for child in group:
        td.append(child)
    return root


class TableMarkupExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('tablemarkup', TableMarkupTreeProcessor(), '<prettify')
