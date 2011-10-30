from .ConverterMock import ConverterMock
from earshinov_markdown.converters import ResettingMarkdownConverter, \
  SimpleMarkdownConverter
import re
import unittest


# http://stackoverflow.com/questions/3313590#3314913
def contains_sublist(lst, sublst):
  n = len(sublst)
  return any((sublst == lst[i:i+n]) for i in range(len(lst)-n+1))
  

class ResettingMarkdownConverterTest(unittest.TestCase):
  
  def test_basic(self):
    '''
    ResettingMarkdownConverter должен выполнять reset по крайней
    мере между каждыми двумя вызовами convert
    ''' 
    
    dummy = ConverterMock()
    converter = ResettingMarkdownConverter(dummy)
    
    converter.convert("")
    converter.convert("")
    
    calledMethods = [name for name, args, kw in dummy.method_calls]
    self.assertTrue(
        contains_sublist(calledMethods, ['convert', 'reset', 'convert']),
        'Между двумя вызовами convert должен быть вызван reset')

  def test_ensures_local_references(self):
    '''Вызов reset должен обеспечивать локальность ссылок (references)'''
    chunk1 = \
      "[Google][1]\n\n" + \
      "[1]: http://google.com/"
    chunk2 = \
      "[Яндекс][1]\n\n" + \
      "[1]: http://yandex.ru/"
    def getResultsUsing(converter):
      return converter.convert(chunk1) + converter.convert(chunk2)
    def yandexOccurencesCount(str):
      return len(re.findall(r'yandex\.ru', str))
    def googleOccurencesCount(str):
      return len(re.findall(r'google\.com', str))
    
    # если не вызывать reset, references получаются глобальными, так что
    # обе ссылки в результате получают один адрес
    ret1 = getResultsUsing(SimpleMarkdownConverter())
    self.assertTrue(yandexOccurencesCount(ret1) == 2 or googleOccurencesCount(ret1) == 2)
    
    # если вызывать reset, references являются локальными для каждого куска разметки,
    # для которого вызван convert, так что каждая из ссылок получает свой (правильный) адрес 
    ret2 = getResultsUsing(ResettingMarkdownConverter(SimpleMarkdownConverter()))
    self.assertTrue(yandexOccurencesCount(ret2) == 1 and googleOccurencesCount(ret2) == 1)
    
