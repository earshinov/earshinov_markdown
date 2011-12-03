from earshinov_markdown.utils.HierarchyBuilder import HierarchyBuilderWithQueue
from markdown.blockprocessors import HRProcessor

class CustomHtmlListBuilder(HierarchyBuilderWithQueue):

  class Level:
    def __init__(self, char, element):
      self.char = char
      self.element = element

  def __init__(self, etree, root):
    super(CustomHtmlListBuilder, self).__init__()
    self._etree = etree
    self._root = root
    self._hrProcessor = HRProcessor()

  rootUl = property(lambda self: None if not self._levels else self._levels[0].element)

  @staticmethod
  def _parseLine(line, level=None):
    assert line and not line[0].isspace()

    if level is not None:
      if line[0] == level.char:
        char = level.char
        text = line[1:].lstrip()
      else:
        char = None
        text = line
    else:
      if line[0] in '*-|':
        char = line[0]
        text = line[1:].lstrip()
      else:
        char = None
        text = line
    return (char, text)

  def _createUl(self, parent, char):
    if char is None or char == '*':
      return self._etree.SubElement(parent, 'ul')
    elif char == '-':
      return self._etree.SubElement(parent, 'ol')
    elif char == '|':
      return self._etree.SubElement(parent, 'ul', { 'class': 'details' })
    else:
      raise Exception("Invalid char")

  def _createLi(self, parent, text):

    # Кастомная обработка: если текст соответствует Markdown-разметке горизонтальной линии,
    # вместо использования этого текста добавляем элементу списка класс "separator"
    shouldBeSeparator = self._hrProcessor.test(parent, text)

    li = self._etree.SubElement(parent, 'li')
    if shouldBeSeparator:
      li.set('class', 'separator')
    else:
      li.text = text
    return li


  def push(self, line):
    char, text = self._parseLine(line, level=None)
    parentElement = self._root if not self._levels else \
      self._levels[-1].element[-1] # последний LI текущего UL

    ul = self._createUl(parentElement, char)
    self._createLi(ul, text)
    self._levels.append(self.Level(char, ul))

  def put(self, line):
    level = self._levels[-1]
    unused_char, text = self._parseLine(line, level)
    self._createLi(level.element, text)
