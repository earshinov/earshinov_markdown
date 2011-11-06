from markdown import Extension
from .CustomListProcessor import CustomListProcessor


class CustomListProcessorExtension(Extension):
  
  def extendMarkdown(self, md, md_globals):
    md.parser.blockprocessors.add('customlist', CustomListProcessor(md), '>empty')
    del md.parser.blockprocessors['olist']
    del md.parser.blockprocessors['ulist']