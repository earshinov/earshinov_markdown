from markdown import etree


class IndentationLevel:

  def __init__(self, indent, char, element):
    super(IndentationLevel, self).__init__()
    self.indent = indent
    self.char = char
    self.__element = element

  def appendChild(self):
    return etree.SubElement(self.__element, 'li')

  lastChild = property(lambda self: None if not self.__element else self.__element[-1])