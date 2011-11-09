from markdown import etree, Extension
from markdown.blockprocessors import BlockProcessor


class NoteMetaProcessor(BlockProcessor):

  def test(self, parent, block):
    for line in block.split('\n'):
      if line.startswith('Date: ') or line.startswith('Tags: '):
        continue
      return False
    return True

  def run(self, parent, blocks):
    block = blocks.pop(0);

    div = etree.SubElement(parent, 'div', { 'class': 'note_meta' })

    for line in block.split('\n'):
      if line.startswith('Date: '):
        dateDiv = etree.SubElement(div, 'div', { 'class': 'date' })
        dateDiv.text = line[len('Date: '):]
      elif line.startswith('Tags: '):
        tagsDiv = etree.SubElement(div, 'div', { 'class': 'tags' })
        tags = line[len('Tags: '):]
        for tag in tags.split(','):
          a = etree.SubElement(tagsDiv, 'a', { 'class': 'note_tag', 'href': '#' })
          a.text = tag.strip()
          # разделяем теги пробелами, иначе в вёрстке отступ
          # между ними будет меньше положенного
          a.tail = ' '


class NotesMetaProcessorExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.parser.blockprocessors.add('notemeta', NoteMetaProcessor(md), '<paragraph')