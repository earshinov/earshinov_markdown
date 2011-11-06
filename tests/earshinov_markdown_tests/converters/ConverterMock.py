from mock import Mock


class ConverterMock(Mock):
  '''
  Mock-объект для подмены парсера markdown.  Метод convert()
  возвращает переданную строку, окружённую тройными фигурными
  скобками ("{{{текст}}}")
  '''

  def __new__(cls, *args, **kw):
    mock = Mock(*args, **kw)
    mock.convert.side_effect = lambda text: '{{{' + text + '}}}'
    return mock
