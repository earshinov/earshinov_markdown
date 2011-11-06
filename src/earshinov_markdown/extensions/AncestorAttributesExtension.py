from collections import namedtuple
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import re


class AncestorAttribute(namedtuple('AncestorAttribute', 'uplevel name value')):
  __slots__ = ()
  def __new__(cls, uplevel, name, value):
    assert uplevel > 0
    return super(AncestorAttribute, cls).__new__(cls, uplevel, name, value)

class AncestorAttributes(dict):
  def add(self, element, ancestorAttribute):
    #assert isinstance(ancestorAttribute, AncestorAttribute)
    self.setdefault(element, []).append(ancestorAttribute)

ANCESTOR_ATTRIBUTES = AncestorAttributes()


class AncestorAttributesExtensionTreeProcessor(Treeprocessor):

  def run(self, root):
    # Приходится обходить дерево самому, потому что библиотека ElementTree,
    # подключаемая в python-markdown, не позволяет вытаскивать родительский
    # элемент из дочернего (`element.find("..")` всегда возвращает `None`).
    # Подсунуть вместо этого ElementTree реализацию из библиотеки LXML можно,
    # но это не вариант — из-за несовместимостей с ней python-markdown не работает.
    self.__processSubtree([root])

  def __processSubtree(self, ancestorsAndRoot):
    root = ancestorsAndRoot[-1]
    for child in root:
      self.__processElement(child, ancestorsAndRoot)
      ancestorsAndRoot.append(child)
      self.__processSubtree(ancestorsAndRoot)
      ancestorsAndRoot.pop()

  def __processElement(self, element, ancestors):
    if element in ANCESTOR_ATTRIBUTES:
      for a in ANCESTOR_ATTRIBUTES[element]:
        if a.uplevel > len(ancestors):
          continue
        ancestors[-a.uplevel].set(a.name, a.value)


class AncestorAttributesExtension(Extension):
  '''
  Расширение позволяет задавать атрибуты не только текущему элементу, но и родительским.
  Без этого, насколько мне известно, невозможно проставить CSS-класс, например, элементу <dl>.
  С этим расширением решение выглядит так:

  {^@class=someclass} Term
  : Definition
  Other term
  : Other definition

  Количество крышечек определяет, на сколько уровней вверх поднимается атрибут.

  Для работы расширения необходимо пропатчить некоторые внутренние части пакета Markdown.
  Для этого перед первым использованием расширения необходимо вызвать статический метод
  patchMarkdownGlobals().  После этого вызова одновременное использование нескольких
  экземпляров парсера Markdown может привести к проблемам, особенно когда оба обрабатывают
  разметку, где присутствуют обрабатываемые этим расширением конструкции {^@...}.
  '''

  @staticmethod
  def patchMarkdownGlobals():
    import markdown.inlinepatterns as ip

    ATTR_RE = re.compile("\{(\^*)@([^\}]*)=([^\}]*)} *") # {@id=123}

    def handleAttributes(text, parent):
      def attributeCallback(match):
        name = match.group(2)
        value = match.group(3).replace('\n', ' ')
        if match.group(1):
          # В этом месте элемент `parent` с большой вероятностью ещё не вставлен в
          # результирующее дерево, так что сразу проставить атрибут элементу-предку
          # мы не можем.  Приходится сохранять атрибуты глобально и расставлять их
          # с помощью отдельного TreeProcessor'а.
          ANCESTOR_ATTRIBUTES.add(parent, AncestorAttribute(uplevel=len(match.group(1)), name=name, value=value))
        else:
          parent.set(name, value)
      return ATTR_RE.sub(attributeCallback, text)

    ip.handleAttributes = handleAttributes

  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('ancattrs', AncestorAttributesExtensionTreeProcessor(), '_end')
    md.registerExtension(self) # чтобы вызывался метод reset

  def reset(self):
    ANCESTOR_ATTRIBUTES = {}