from collections import namedtuple
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import re


ANCESTOR_ATTRIBUTES = {}
AncestorAttribute = namedtuple('AncestorAttribute', 'uplevel name value')

def addAncestorAttribute(element, ancestorAttribute):
  ANCESTOR_ATTRIBUTES.setdefault(element, []).append(ancestorAttribute)


class AncestorAttributesExtensionTreeProcessor(Treeprocessor):
  
  def run(self, root):
    # Приходится обходить дерево самому, потому что библиотека ElementTree,
    # подключаемая в python-markdown, не позволяет вытаскивать родительский
    # элемент из дочернего (`element.find("..")` всегда возвращает `None`).
    # Подсунуть вместо этого ElementTree реализацию из библиотеки LXML можно,
    # но это не вариант — из-за несовместимостей с ней python-markdown не работает.
    self.__processChildren([root])
    
  def __processChildren(self, parents):
    for child in parents[-1]:
      self.__handleChild(child, parents)
      parents.append(child)
      self.__processChildren(parents)
      parents.pop()
      
  def __handleChild(self, child, parents):
    if child in ANCESTOR_ATTRIBUTES:
      for a in ANCESTOR_ATTRIBUTES[child]:
        if a.uplevel > len(parents):
          continue
        parents[-a.uplevel].set(a.name, a.value)


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
          addAncestorAttribute(parent, AncestorAttribute(uplevel=len(match.group(1)), name=name, value=value))
        else:
          parent.set(name, value)
      return ATTR_RE.sub(attributeCallback, text)
    
    ip.handleAttributes = handleAttributes
  
  def extendMarkdown(self, md, md_globals):
    md.treeprocessors.add('ancattrs', AncestorAttributesExtensionTreeProcessor(), '_end')
    md.registerExtension(self) # чтобы вызывался метод reset
    
  def reset(self):
    ANCESTOR_ATTRIBUTES = {}