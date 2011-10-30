from .CustomListProcessor import CustomListProcessor
from .EmptyListItemsRemover import EmptyListItemsRemover
from .ItemTypePattern import ItemTypePattern
from .ListSeparatorProcessor import ListSeparatorProcessor
from .TableMarkupTreeProcessor import TableMarkupTreeProcessor
from markdown import Extension
  

class TasksExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.inlinePatterns.add('itemtype', ItemTypePattern(), '<reference')
    md.parser.blockprocessors.add('customlist', CustomListProcessor(md), '>empty')
    del md.parser.blockprocessors['olist']
    del md.parser.blockprocessors['ulist']
    md.parser.blockprocessors['hr'] = ListSeparatorProcessor(md.parser)
    md.treeprocessors.add('tablemarkup', TableMarkupTreeProcessor(), '<prettify')
    md.postprocessors.add('liremover', EmptyListItemsRemover(), '_end')