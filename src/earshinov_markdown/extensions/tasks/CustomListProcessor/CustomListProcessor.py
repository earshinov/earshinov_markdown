from .IndentationLevel import IndentationLevel
from .IndentationLevelsController import IndentationLevelsController
from markdown import etree
from markdown.blockprocessors import BlockProcessor
import re


class CustomListProcessor(BlockProcessor):

  class __Reset(Exception):

    def __init__(self, firstLine, lines):
      Exception.__init__(self)
      self.firstLine = firstLine
      self.lines = lines

  __RE_HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)

  def __init__(self, markdown):
    super(CustomListProcessor, self).__init__(markdown.parser)
    self.__markdown = markdown
    self.__levelsController = IndentationLevelsController()
    self.__recursionCount = 0

  def test(self, parent, block):
    shouldRun = block and not block.isspace() and block[0].isspace()
    if self.__recursionCount == 0 and not shouldRun:
      #
      # Чтобы два списка, разделённых другими блоками, не объединялись в один.
      # Здесь опираемся на то, что экземпляр этого BlockProcessor'а должен идти
      # первым в коллекции block processor'ов.  Если это не так, разделяющий
      # списки блок может проскочить и списки слипнутся
      #
      self.__levelsController.clear()
    return shouldRun

  def run(self, parent, blocks):
    # чтобы для однострочных элементов не вставлялись параграфы
    # см. markdown.blockprocessors.ParagraphProcessor
    self.parser.state.set('list')
    self.__recursionCount += 1
    self.__handleBlock(parent, blocks.pop(0))
    self.__recursionCount -= 1
    self.parser.state.reset()

  def __handleBlock(self, parent, block):
    if self.__recursionCount == 1:
      block = self.__replaceHtmlComments(block)
    lines = [line for line in block.split('\n')]
    self.__handleLines(parent, lines[0], lines[1:])

  def __replaceHtmlComments(self, text):
    # необходимо, потому что многострочные HTML-комментарии могут ломать структуру списка
    def replace(m):
      return self.__markdown.htmlStash.store(m.group())
    return self.__RE_HTML_COMMENT.sub(replace, text)

  def __handleLines(self, parent, firstLine, lines):
    while True:
      level = self.__handleFirstLine(parent, firstLine)
      try:
        self.__handleConsequentLines(lines, level)
      except self.__Reset as e:
        firstLine = e.firstLine
        lines = e.lines
        continue
      break

  def __handleFirstLine(self, parent, line):
    m = re.match('(\s*)(.)(\s*)(.*)', line)
    assert(m is not None)

    indent = m.group(1)
    char = m.group(2)
    shortText = m.group(4)
    fullText = m.group(2) + m.group(3) + m.group(4)

    ret = self.__levelsController.findLevel(indent)
    if ret.shouldCreate:
      parentElement = ret.parentElement
      if parentElement is None:
        parentElement = parent
      char, element = self.__createListElement(char)
      parentElement.append(element)
      text = shortText if char is not None else fullText
      level = IndentationLevel(indent, char, element)
      ret.appendLevel(level)
    else:
      level = ret.existingLevel
      self.__levelsController.cutNested(level)
      text = shortText if char == level.char else fullText

    self.__appendItem(level, text)
    return level

  def __createListElement(self, char):
    if char not in '*-|':
      char = None
    if char is None or char == '*':
      return char, etree.Element('ul')
    elif char == '-':
      return char, etree.Element('ol')
    elif char == '|':
      return char, etree.Element('ul', { 'class': 'details' })

  def __handleConsequentLines(self, lines, level):
    it = iter(lines)
    reuseLine = False
    while True:
      if not reuseLine:
        try:
          line = next(it)
        except(StopIteration):
          break
      reuseLine = False

      if not line.startswith(level.indent):
        raise self.__Reset(line, it)
      originalLine = line
      line = line[len(level.indent):]

      if level.char is not None and line.startswith(level.char):
        self.__appendItem(level, line[1:].lstrip())
      elif not line[0].isspace():
        self.__appendItem(level, line)
      else:
        line = self.__appendSubblock(level, originalLine, it)
        if line is None:
          break
        self.__levelsController.cutNested(level)
        reuseLine = True

  def __appendItem(self, level, text):
    self.parser.parseChunk(level.appendChild(), text)

  def __appendSubblock(self, level, firstLine, lineIterator):
    indent = re.match('\s*', firstLine).group()
    subblock = [firstLine]
    try:
      while True:
        line = next(lineIterator)
        if line.startswith(indent):
          subblock.append(line)
        else:
          break
    except(StopIteration):
      line = None
    self.parser.parseBlocks(level.lastChild, ['\n'.join(subblock)])
    return line