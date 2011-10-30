import re


class InlineMarkdownConverter:
  
  DEFAULT_START_MARKER = '<!-- START MARKDOWN -->'
  DEFAULT_END_MARKER = '<!-- END MARKDOWN -->'
  
  def __init__(self, converter):
    self.startMarker = self.DEFAULT_START_MARKER
    self.endMarker = self.DEFAULT_END_MARKER
    self.__converter = converter
    
  def convert(self, text):
    regexp = re.compile(re.escape(self.startMarker) + '(.*?)' + re.escape(self.endMarker), re.DOTALL)
    def replace(m):
      return self.__converter.convert(m.group(1))
    return regexp.sub(replace, text)
    