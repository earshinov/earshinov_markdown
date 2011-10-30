class ResettingMarkdownConverter:
  
  def __init__(self, converter):
    super(ResettingMarkdownConverter, self).__init__()
    self.__converter = converter
    
  def convert(self, text):
    self.__converter.reset()
    return self.__converter.convert(text)