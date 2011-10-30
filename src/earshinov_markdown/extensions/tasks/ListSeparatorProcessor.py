from markdown.blockprocessors import HRProcessor


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