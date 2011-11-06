from earshinov_markdown.extensions.tasks import TasksExtension
from markdown import Markdown
import re
import unittest


class TasksIntegrationTest(unittest.TestCase):

  def setUp(self):
    self.md = Markdown([TasksExtension()])
    
  def tests_basic(self):
    source = '''
  Домашние дела
  
    Проблемы с сетью
      <!-- завершено: Сменить адреса DNS-серверов -->
      [sometime] Купить беспроводную точку доступа
      
    Велосипед
      Смазать цепь

-------

  Программирование
    Самообразование
      Освоение Python
        - Расширения для [python-markdown][]
        - Собрать в пакет (distutils?)

    -----
    
    Работа
      Освоение C# 4.0
        | C# in Depth
        | C# in a Nutshell
        
-------

[python-markdown]: http://www.freewisdom.org/projects/python-markdown/
'''
    expectedRe = re.compile(
r'''^
<tr>\s*
  <td>\s*
    <ul>\s*
      <li>Домашние\ дела<ul>\s*
        <li>Проблемы\ с\ сетью<ul>\s*
          <!-- .*? -->\s*
          <li\ class=["']type_sometime["']>Купить\ беспроводную\ точку\ доступа</li>\s*
        </ul>\s*</li>\s*
        <li>Велосипед<ul>\s*
          <li>Смазать\ цепь</li>\s*
        </ul>\s*</li>\s*
      </ul>\s*</li>\s*
    </ul>\s*
  </td>\s*
  <td>\s*
    <ul>\s*
      <li>Программирование<ul>\s*
        <li>Самообразование<ul>\s*
          <li>Освоение\ Python<ol>\s*
            <li>Расширения\ для\ <a\ href=["']http://www.freewisdom.org/projects/python-markdown/["']>python-markdown</a></li>\s*
            <li>Собрать\ в\ пакет\ \(distutils\?\)</li>\s*
          </ol>\s*</li>\s*
        </ul>\s*</li>\s*
        <li\ class=["']separator["'](>|\ */>|></li>)\s*
        <li>Работа<ul>\s*
          <li>Освоение\ C\#\ 4.0<[uo]l\ class=["']details["']>\s*
            <li>C\#\ in\ Depth</li>\s*
            <li>C\#\ in\ a\ Nutshell</li>\s*
          </[uo]l>\s*</li>\s*
        </ul>\s*</li>\s*
      </ul>\s*</li>\s*
    </ul>\s*
  </td>\s*
</tr>
$''', re.VERBOSE)
    self.assertRegex(self.md.convert(source), expectedRe)