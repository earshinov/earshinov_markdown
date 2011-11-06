from .CustomListProcessor import CustomListProcessor
from .EmptyListItemsRemover import EmptyListItemsRemover
from .ItemTypeExtension import ItemTypeExtension
from .ListSeparatorExtension import ListSeparatorExtension
from .TableMarkupTreeProcessor import TableMarkupTreeProcessor
from markdown import Extension
  

class TasksExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    ItemTypeExtension().extendMarkdown(md, md_globals)
    md.parser.blockprocessors.add('customlist', CustomListProcessor(md), '>empty')
    del md.parser.blockprocessors['olist']
    del md.parser.blockprocessors['ulist']
    ListSeparatorExtension().extendMarkdown(md, md_globals)
    md.treeprocessors.add('tablemarkup', TableMarkupTreeProcessor(), '<prettify')
    md.postprocessors.add('liremover', EmptyListItemsRemover(), '_end')