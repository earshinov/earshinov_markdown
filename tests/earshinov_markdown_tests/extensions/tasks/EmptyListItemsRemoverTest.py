from earshinov_markdown.extensions.tasks.EmptyListItemsRemovalExtension import EmptyListItemsRemover
import unittest


class EmptyListItemsRemoverTest(unittest.TestCase):
  
  def setUp(self):
    self.remover = EmptyListItemsRemover()
    
  def test_basic(self):
    text = "<ul><li>first</li><li><!-- comment --></li><li>third</li></ul>"
    expected = "<ul><li>first</li><!-- comment --><li>third</li></ul>"
    self.assertEqual(expected, self.remover.run(text))
    
  def test_items_with_content_not_removed(self):
    text1 = \
      "<ul>" + \
        "<li>first</li>" + \
        "<li><!-- comment -->content</li>" + \
        "<li>content<!-- comment --></li>" + \
        "<li>fourth</li>" + \
      "</ul>"
    self.assertEqual(text1, self.remover.run(text1))

    text2 = \
      "<ul>" + \
        "<li>first</li>" + \
        "<li>content<!-- comment --></li>" + \
        "<li><!-- comment -->content</li>" + \
        "<li>fourth</li>" + \
      "</ul>"
    self.assertEqual(text2, self.remover.run(text2))