from earshinov_markdown.lib.urlize import UrlizePattern
from markdown import Extension


URLIZE_RE = '(%s)' % '|'.join([
    r'<(?:f|ht)tps?://[^>]*>',
    r'\b(?:f|ht)tps?://[^)<>\s]+[^.,)<>\s]',
    r'\bwww\.[^)<>\s]+[^.,)<>\s]',
    # Убираем четвёртый/последний паттерн из urlize.URLIZE_RE,
    # потому что он даёт ненужные срабатывания.  Например в
    # заметке о cl1p.net он матчит строку "cl1p.net" в заголовке.
])

class UrlizeExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    # необходимо добавлять после html, чтобы содержимое атрибута
    # href элементов a, вручную заданных в разметке Markdown,
    # не заменялось на placeholder'ы 
    md.inlinePatterns.add('autolink', UrlizePattern(URLIZE_RE, md), '>html')

