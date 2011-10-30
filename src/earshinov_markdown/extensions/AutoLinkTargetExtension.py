from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import re


class AutoLinkTargetTreeProcessor(Treeprocessor):
  '''Проставляет target=_blank абсолютным ссылкам'''   
  
  RE_HTTP = re.compile('https?://')
  
  def run(self, root):
    self.__processChildren(root)
    
  def __processChildren(self, parent):
    for child in parent:
      if child.tag == 'a' and 'target' not in child.keys():
        href = child.get('href')
        if href is not None and self.RE_HTTP.match(href):
          child.set('target', '_blank')
      self.__processChildren(child)


class AutoLinkTargetExtension(Extension):
  
  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('autotarget', AutoLinkTargetTreeProcessor(), '_end')