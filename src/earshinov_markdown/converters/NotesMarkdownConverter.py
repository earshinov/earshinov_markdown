from .ConverterDecorator import ConverterDecorator
import re


class NotesMarkdownConverter(ConverterDecorator):
  '''Отдельный запуск Markdown на каждую заметку для локальности ссылок (reference)'''
  
  __NOTE_HEADER_RE = re.compile(r'(?<=\n\n)(# .*)(?=$|\n$|\n\n)')
  
  def convert(self, text):
    # На случай, если заголовок располагается в первой или второй строке,
    # чтобы в регулярном выражении сработал lookbehind.  Использовать "|"
    # в lookbehind, как в lookahead, не получается из-за ошибки
    # "look-behind requires fixed-width pattern", которую выдаёт Python.
    # Добавленные символы всё равно ни на что не влияют, потому что вся
    # разметка до первого заголовка игнорируется
    text = '\n\n' + text
    
    blocks = self.__NOTE_HEADER_RE.split(text)
    if not blocks:
      return ''
    
    result = []
    it = iter(blocks[1:])
    for header, body in zip(it, it):
      result.append(self._converter.convert(header + body))
    return ''.join(result)