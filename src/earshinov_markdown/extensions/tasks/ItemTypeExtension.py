from markdown import Extension
from markdown.inlinepatterns import Pattern

class ItemTypePattern(Pattern):
  '''Позволяет задавать типы задач, поддерживаемые в tasks, в виде [normal], [freetime] и т.д.'''

  KNOWN_TYPES = (
    'deferred', 'grayed', 'normal', 'important',
    'freetime', 'wait', 'hard', 'stats', 'sometime' )

  def __init__(self, **kwargs):
    super(ItemTypePattern, self).__init__(r'(\s+|^)\[(%s)\](\s+|$)' % '|'.join(self.KNOWN_TYPES), **kwargs)

  def handleMatch(self, m):
    return '%s{@class=type_%s}' % (m.group(2), m.group(3))


class ItemTypeExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.inlinePatterns.add('itemtype', ItemTypePattern(), '<reference')
