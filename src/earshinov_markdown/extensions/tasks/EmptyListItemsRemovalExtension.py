from markdown import Extension
from markdown.postprocessors import Postprocessor
import re


class EmptyListItemsRemover(Postprocessor):
  '''Заменяет элементы li, содержащие только HTML-комментарии, самим блоком
  комментария.  Такие элементы могут создаваться CustomListProcessor'ом в
  случае, когда HTML-комментарии присутствуют в разметке списка.  Такие
  элементы вредны, потому что плохо обрабатываются JavaScript'ом страницы задач.'''

  __RE_LIST_ITEM = re.compile(r'<li>(?=(<!--.*?-->))\1</li>', re.DOTALL)

  def run(self, text):
    return self.__RE_LIST_ITEM.sub(r'\1', text)


class EmptyListItemsRemovalExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.postprocessors.add('liremover', EmptyListItemsRemover(), '_end')