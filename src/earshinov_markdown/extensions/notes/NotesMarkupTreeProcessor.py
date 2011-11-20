from markdown import etree
from markdown.treeprocessors import Treeprocessor


class NotesMarkupTreeProcessor(Treeprocessor):

  def run(self, root):

    # список собранных заметок
    notes = []

    # содержимое текущей заполняемой заметки
    note = None
    header = None
    content = None

    for child in root:
      if child.tag == 'h1':
        note = etree.Element('div', { 'class': 'note' })
        header = etree.SubElement(note, 'div', { 'class': 'header' })
        if 'id' in child.keys():
          note.set('id', child.get('id'))
        self.__copyTitle(header, child)
        content = etree.SubElement(note, 'div', { 'class': 'content' })
        self.__appendText(child.tail, content)
        notes.append(note)
      elif child.tag == 'div' and child.get('class') == 'note_meta':
        self.__reorganizeNoteMeta(note, header, child)
        self.__appendText(child.tail, content)
      elif content is not None:
        content.append(child)

    root.clear()
    for note in notes:
      root.append(note)
    return root

  def __copyTitle(self, noteHeader, h1):
    title = etree.SubElement(noteHeader, 'div', { 'class': 'title' })
    title.text = h1.text
    children = list(h1)
    for child in children:
      title.append(child)

  def __appendText(self, text, elementWhereToAppend):
    if text is None:
      return
    e = elementWhereToAppend
    if len(e) > 0:
      if e[-1].tail:
        e[-1].tail += text
      else:
        e[-1].tail = text
    else:
      if e.text:
        e.text += text
      else:
        e.text = text

  def __reorganizeNoteMeta(self, note, noteHeader, noteMeta):
    date = None
    tags = None
    for child in noteMeta:
      if child.get('class') == 'date':
        date = child
      elif child.get('class') == 'tags':
        tags = child
    if date is not None:
      noteHeader.append(date)
    if tags is not None:
      note.append(tags)