from markdown import Markdown


class SimpleMarkdownConverter:

  def __new__(cls, extensions=[]):
    # по умолчанию используем html4, а не xhtml, потому что первый я использую намного чаще
    return Markdown(extensions, output_format='html4')