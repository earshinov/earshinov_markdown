from .ConverterDecorator import ConverterDecorator


class ResettingMarkdownConverter(ConverterDecorator):
    
  def convert(self, text):
    self._converter.reset()
    return self._converter.convert(text)