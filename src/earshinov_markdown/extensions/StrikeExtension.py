# http://sahd.lamafam.org/?p=770

from markdown import Extension
from markdown.inlinepatterns import SimpleTagPattern


class StrikePattern(SimpleTagPattern):

  STRIKE_RE = r'(--)(.+?)--'

  def __init__(self):
    super(StrikePattern, self).__init__(self.STRIKE_RE, 'strike')


class StrikeExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.inlinePatterns.add('strike', StrikePattern(), '>strong')