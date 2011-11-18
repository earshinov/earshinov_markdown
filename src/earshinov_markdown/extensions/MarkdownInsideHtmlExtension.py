from markdown import Extension, etree
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
import markdown
import re


class MarkdownInsideHtmlPostprocessor(Postprocessor):
  """По умолчанию Markdown не позволяет использовать разметку внутри
  HTML-тегов, однако иногда HTML бывает удобнее, чем синтаксис Markdown
  (например, при разметке больших таблиц).  Для этого случая полезно
  это расширение: оно позволяет внутри HTML заключать разметку в теги
  <MD> </MD> (обязательно в верхнем регистре, чтобы отличались от обычных
  тегов HTML); в конце преобразования документа из Markdown в HTML
  расширение обработает содержимое этих тегов, сами теги при этом
  удаляются.  Вложенности тегов <MD> не допускается"""

  RE = re.compile('<MD>(.*?)</MD>', re.DOTALL)

  def __init__(self, md, disabledTreeProcessors=None, disabledPostprocessors=None):
    """
    @param disabledTreeProcessors
        Список/множество названий tree-процессоров, которые
        нужно отключать для дополнительных запусков Markdown
    @param disabledPostprocessors
        Список/множество названий постпроцессоров, которые
        нужно отключать для дополнительных запусков Markdown

    Аргументы disabled* предназначены для того, чтобы для дополнительных запусков Markdown
    отключать расширения, изменяющие структуру результирующего документа, иначе эти
    изменения структуры будут применены к содержимому блоков <MD>...</MD>
    """
    super(MarkdownInsideHtmlPostprocessor, self).__init__()
    self.markdown = md
    self.__recursionCount = 0

    # store self.__disabled*
    self.__disabledTreeProcessors = {} if disabledTreeProcessors is None else \
      dict((name, None) for name in disabledTreeProcessors)
    self.__disabledPostprocessors = {} if disabledPostprocessors is None else \
      dict((name, None) for name in disabledPostprocessors)

  def run(self, text):
    if self.__recursionCount > 0:
      return text
    self._prepareMarkdown()
    self.__recursionCount += 1
    try:
      text = re.sub(self.RE, lambda match: self.markdown.convert(match.group(1)), text)
    finally:
      self.__recursionCount -= 1
      self._restoreMarkdown()
    return text

  def _prepareMarkdown(self):
    #
    # По умолчанию парсер Markdown, даже если в исходнике одна строка текста,
    # добавляет в результирующий HTML элемент p.  Мы должны это предотвратить,
    # потому что <MD>...</MD> может использоваться для вставки inline-элементов.
    # Временно подключаем наше расширение, которое уберёт элемент p, если он
    # единственный.  Почему два раза, см. в комментариях к классу расширения.
    #
    # В CustomListProcessor для той же цели мы переводили парсер Markdown в
    # состояние "list" (`markdown.parser.state.set("list")`).  Здесь этот способ
    # использовать не получается — если корневой элемент содержит только текст,
    # но не дочерние элементы (в нашем примере, элемент p), отказывается работать
    # InlineProcessor — часть python-markdown, обеспечивающая рендеринг inline-
    # элементов разметки (таких как **жирный текст** и пр.).  Наше расширение
    # добавляем в конец (`_end`), чтобы оно работало *после* InlineProcessor
    #
    proc = StripSingleParagraphTreeProcessor()
    self.markdown.treeprocessors.add('stripsinglep', proc, '_end')
    self.markdown.treeprocessors.add('stripsinglep2', proc, '_end')

    # disable self.__disabled*
    # вместо удаления расширений подставляем ничего не делающие реализации,
    # чтобы не приходилось запоминать  позиции, в которых располагались расширения
    for k in self.__disabledTreeProcessors:
      self.__disabledTreeProcessors[k] = self.markdown.treeprocessors[k]
      self.markdown.treeprocessors[k] = NoopTreeProcessor()
    for k in self.__disabledPostprocessors:
      self.__disabledPostprocessors[k] = self.markdown.postprocessors[k]
      self.markdown.postprocessors[k] = NoopPostprocessor()

  def _restoreMarkdown(self):
    del self.markdown.treeprocessors['stripsinglep']
    del self.markdown.treeprocessors['stripsinglep2']

    # restore self.__disabled*
    for k, v in self.__disabledTreeProcessors.items():
      self.markdown.treeprocessors[k] = v
    for k, v in self.__disabledPostprocessors.items():
      self.markdown.postprocessors[k] = v


class MarkdownInsideHtmlExtension(Extension):

  def __init__(self, disabledTreeProcessors=None, disabledPostprocessors=None):
    """
    @param disabledTreeProcessors
        Список/множество названий tree-процессоров, которые
        нужно отключать для дополнительных запусков Markdown
    @param disabledPostprocessors
        Список/множество названий постпроцессоров, которые
        нужно отключать для дополнительных запусков Markdown

    Аргументы disabled* предназначены для того, чтобы для дополнительных запусков Markdown
    отключать расширения, изменяющие структуру результирующего документа, иначе эти
    изменения структуры будут применены к содержимому блоков <MD>...</MD>
    """
    super(MarkdownInsideHtmlExtension, self).__init__()
    self.__disabledTreeProcessors = disabledTreeProcessors
    self.__disabledPostprocessors = disabledPostprocessors

  def extendMarkdown(self, md, md_globals):
    proc = MarkdownInsideHtmlPostprocessor(md,
      self.__disabledTreeProcessors,
      self.__disabledPostprocessors)
    md.postprocessors.add('mdinsidehtml', proc, '_end')


class StripSingleParagraphTreeProcessor(Treeprocessor):
  """Вспомогательная штука, которая удаляет из результирующего HTML элемент p, если он единственный.
  ВНИМАНИЕ! Один экзепляр этого класса должен добавляться в цепочку tree-процессоров Markdown дважды,
  так чтобы он вызвался последовательно дважды!"""

  def __init__(self):
    # отслеживание вызовов - первый/второй
    self.called = False
    self.dummyElement = None

  def run(self, root):
    if not self.called:
      # первый вызов
      self.called = True
      return self._runFirst(root)
    else:
      # второй вызов
      self.called = False
      return self._runSecond(root)

  def _runFirst(self, root):
    if (not root.text or root.text.isspace()) and len(root) == 1 and root[0].tag == 'p':
      p = root[0]
      if (not p.tail or p.tail.isspace()) and len(p.attrib) == 0:
        # Делаем p корневым элементом
        p.tag = markdown.DOC_TAG
        if len(p) == 0:
          # Нюанс, из-за которого этот tree-процессор необходимо добавлять дважды.
          # Чтобы Markdown подхватил новый корневой элемент, он должен быть непуст
          # (из-за проверки `if newRoot` в коде метода `Markdown.convert`).
          # Добавляем временный элемент, который удаляем при втором вызове
          self.dummyElement = etree.SubElement(p, 'span')
        return p
    return root

  def _runSecond(self, root):
    if self.dummyElement is not None:
      root.remove(self.dummyElement)
      self.dummyElement = None
    return root


class NoopTreeProcessor(Treeprocessor):
  """Ничего не делающий Tree-процессор"""
  pass

class NoopPostprocessor(Postprocessor):
  """Ничего не делающий постпроцессор"""
  def run(self, text):
    return text