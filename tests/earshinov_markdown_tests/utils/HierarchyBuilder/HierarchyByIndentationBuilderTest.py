from earshinov_markdown.utils.HierarchyBuilder import \
  HierarchyByIndentationBuilder, TracingHierarchyBuilderWithQueue
import unittest


class HierarchyByIndentationBuilderTest(unittest.TestCase):

  def assertTrace(self, source, expectedTrace):
    trace = []
    builder = HierarchyByIndentationBuilder(TracingHierarchyBuilderWithQueue(trace))
    for line in source.strip('\n').split('\n'):
      builder.putLine(line)

    if type(expectedTrace) is list:
      # expectedTrace - массив
      self.assertEqual(expectedTrace, trace)
    else:
      # expectedTrace - строка
      # используем её как регулярное выражение
      trace = '#'.join(':'.join(step) for step in trace)
      expectedTrace = '^' + expectedTrace + '$'
      self.assertRegex(trace, expectedTrace)


  def test_basic(self):
    source = \
'''
1
  1.1
    1.1.1
      1.1.1.1
      1.1.1.2
  1.2
2
'''
    self.assertTrace(source, [
      [],
      ['1'],
      ['1', '1.1'],
      ['1', '1.1', '1.1.1'],
      ['1', '1.1', '1.1.1', '1.1.1.1'],
      ['1', '1.1', '1.1.1', '1.1.1.2'],
      # here 2 elements should be popped at once
      ['1', '1.1'],
      ['1', '1.2'],
      ['1'],
      ['2']
    ])


  def test_incorrect_outdent_beyond_first_column(self):
    source = \
'''
  1
2
'''
    self.assertTrace(source, '#1#(#)?2')


  def test_incorrect_outdent_inside_list(self):
    source = \
'''
1
  2
      3
    4
'''
    self.assertTrace(source, '#1#1:2#1:2:3#(1:2:4|1:2#1:4)')
