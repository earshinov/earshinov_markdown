from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import re


class AutoLinkTargetTreeProcessor(Treeprocessor):
  '''Проставляет target=_blank абсолютным ссылкам'''

  RE_HTTP = re.compile('https?://')

  def run(self, root):
    self.__processSubtree(root)

  def __processSubtree(self, parent):
    for child in parent:
      if child.tag == 'a' and 'target' not in child.keys():
        href = child.get('href')
        if href is not None and self.RE_HTTP.match(href):
          child.set('target', '_blank')
      self.__processSubtree(child)


class AutoLinkTargetExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('auto_link_target', AutoLinkTargetTreeProcessor(), '_end')