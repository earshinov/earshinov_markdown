from markdown.blockprocessors import HRProcessor
from markdown import Extension


class ListSeparatorProcessor(HRProcessor):
  '''Если горизонтальная линия находится внутри ячейки списка, этот класс
  вместо создания тега <hr> добавляет ячейке CSS-класс separator'''
  
  def run(self, parent, blocks):
    if self.parser.state.isstate('list'):
      blocks.pop(0)
      text = parent.text or ''
      parent.text = '{@class=separator}' + text
    else:
      return super(ListSeparatorProcessor, self).run(parent, blocks)
    
    
class ListSeparatorExtension(Extension):
  
  def extendMarkdown(self, md, md_globals):
    md.parser.blockprocessors['hr'] = ListSeparatorProcessor(md.parser)