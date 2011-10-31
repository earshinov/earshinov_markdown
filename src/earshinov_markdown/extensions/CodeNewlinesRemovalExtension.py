from markdown import Extension
from markdown.postprocessors import Postprocessor
import re


class CodeNewlinesRemover(Postprocessor):
  '''
  Удаляет начальные и конечные переносы строк в блоках <pre><code>,
  чтобы в исходнике Markdown такие блоки можно было размечать красивее:
  
  <pre><code>
    Something
    useless
  </code></pre>
  
  вместо
  
  <pre><code>  Something
    useless
  </code</pre>
  
  Необходимо реализовывать это постпроцессором, чтобы к моменту запуска
  этого кода в результат работы Markdown были вставлены куски HTML,
  заданные пользователем вручную в исходнике Markdown.
  '''
  
  __START_RE = re.compile('(<pre.*?>[^<]*<code.*?>)\n+')
  __END_RE = re.compile('\n+(</code>[^<]*</pre>)')
  
  def run(self, text):
    text = self.__START_RE.sub(r'\1', text)
    text = self.__END_RE.sub('</code></pre>', text)
    return text
      
      
class CodeNewlinesRemovalExtension(Extension):
  
  def extendMarkdown(self, md, md_globals):
    md.postprocessors.add('codenlremover', CodeNewlinesRemover(), '_end')