from earshinov_markdown.lib.urlize import UrlizePattern
from markdown import Extension


URLIZE_RE = '(%s)' % '|'.join([
    #r'<(?:f|ht)tps?://[^>]*>',
      # Обрабатывается стандартным шаблончиком autolink,
      # см. UrlizeExtension.extendMarkdown
    r'\b(?:f|ht)tps?://[^)<>\s]+[^.,)<>\s]',
    r'\bwww\.[^)<>\s]+[^.,)<>\s]',
    #r'[^(<\s]+\.(?:com|net|org)\b',
      # Убираем потому что даёт ненужные срабатывания.  Например в
      # заметке о cl1p.net он матчит строку "cl1p.net" в заголовке.
])

class UrlizeExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    # 1. необходимо добавлять после html, чтобы содержимое атрибута
    #    href элементов a, вручную заданных в разметке Markdown,
    #    не заменялось на placeholder'ы
    # 2. меняем название с autolink на autolink_changed, потому что
    #    autolink - стандартный шаблончик, обрабатывающий ссылки в
    #    угловых скобках, который идёт *до* шаблончика html
    md.inlinePatterns.add('autolink_changed', UrlizePattern(URLIZE_RE, md), '>html')

