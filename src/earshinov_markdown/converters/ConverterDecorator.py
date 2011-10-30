class ConverterDecorator:
  
  def __init__(self, converter):
    super(ConverterDecorator, self).__init__()
    self._converter = converter
    
  def convert(self, text):
    return self._converter.convert(text)
  
  def reset(self):
    self._converter.reset()