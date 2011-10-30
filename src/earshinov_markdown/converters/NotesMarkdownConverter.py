from .ConverterDecorator import ConverterDecorator
import re


class NotesMarkdownConverter(ConverterDecorator):
  '''Отдельный запуск Markdown на каждую заметку для локальности ссылок (reference)'''
  
  __NOTE_HEADER_RE = re.compile(r'\n\n(# .*\n\n)')
  
  def convert(self, text):
    blocks = self.__NOTE_HEADER_RE.split(text)
    if not blocks:
      return ''
    
    result = []
    it = iter(blocks[1:])
    for header, body in zip(it, it):
      result.append(self._converter.convert(header + body))
    return '\n'.join(result)