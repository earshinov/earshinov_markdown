from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class HtmlHeaderTreeProcessor(Treeprocessor):

  def run(self, root):
    root.insert(0, etree.Element('meta', {'charset': 'utf-8'}))

    title = None
    for child in root:
      if child.tag == 'h1':
        if title is None:
          title = ''.join(child.itertext())
        else:
          # в документе больше одного заголовка первого уровня - не добавляем title
          title = None
          break
    if title is not None:
      titleElement = etree.Element('title')
      titleElement.text = title
      root.insert(1, titleElement)

    return root


class HtmlHeaderPostprocessor(Postprocessor):

  def run(self, text):
    return '<!DOCTYPE html>\n' + text


class HtmlHeaderExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('htmlheader', HtmlHeaderTreeProcessor(), '_end')
    md.postprocessors.add('htmlheader', HtmlHeaderPostprocessor(), '_end')
