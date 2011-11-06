from .CustomListProcessor import CustomListProcessorExtension
from .EmptyListItemsRemover import EmptyListItemsRemover
from .ItemTypeExtension import ItemTypeExtension
from .ListSeparatorExtension import ListSeparatorExtension
from .TableMarkupExtension import TableMarkupExtension
from markdown import Extension
  

class TasksExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    CustomListProcessorExtension().extendMarkdown(md, md_globals)
    ItemTypeExtension().extendMarkdown(md, md_globals)
    ListSeparatorExtension().extendMarkdown(md, md_globals)
    TableMarkupExtension().extendMarkdown(md, md_globals)
    md.postprocessors.add('liremover', EmptyListItemsRemover(), '_end')