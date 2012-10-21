from .CustomHtmlListBuilder import CustomHtmlListBuilder
from earshinov_markdown.utils.HierarchyBuilder import \
  HierarchyByIndentationBuilder
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class CustomListProcessor(BlockProcessor):

  _RE_HTML_COMMENT = re.compile(r'<!--.*?-->', re.DOTALL)

  def __init__(self, markdown):
    super(CustomListProcessor, self).__init__(markdown.parser)
    self._markdown = markdown
    self._last = None

  def test(self, parent, block):
    return block and not block.isspace() and block[0].isspace()

  def run(self, parent, blocks):

    builder = self._tryReuseLast(parent)
    if builder is None:
      builder = HierarchyByIndentationBuilder(CustomHtmlListBuilder(self.parser, parent))

    block = blocks.pop(0)
    # многострочные HTML-комментарии могут поломать структуру списка
    block = self._replaceHtmlComments(block)

    for line in block.split('\n'):
      builder.putLine(line)

    self._storeLast(parent, builder)

  def _storeLast(self, parent, builder):
    self._last = (parent, builder)

  def _tryReuseLast(self, parent):
    if self._last:
      lastParent, builder = self._last
      if parent is lastParent and \
          len(parent) > 0 and parent[-1] is builder.underlyingBuilder.rootUl:
        return builder
    return None

  def _replaceHtmlComments(self, text):
    def replace(m):
      return self._markdown.htmlStash.store(m.group())
    return self._RE_HTML_COMMENT.sub(replace, text)
