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
    contents = None

    for child in root:
      if child.tag == 'h1':
        note = etree.Element('div', { 'class': 'note' })
        header = etree.SubElement(note, 'div', { 'class': 'header' })
        if 'id' in child.keys():
          note.set('id', child.get('id'))
        self.__copyTitle(header, child)
        content = etree.SubElement(note, 'div', { 'class': 'content' })
        contents = []
        notes.append((note, content, contents))
      elif child.tag == 'div' and child.get('class') == 'note_meta':
        self.__reorganizeNoteMeta(note, header, child)
      else:
        contents.append(child)
        
    root.clear()
    for note, content, contents in notes:
      root.append(note)
      for child in contents:
        content.append(child)
    return root
  
  def __copyTitle(self, noteHeader, h1):
    title = etree.SubElement(noteHeader, 'div', { 'class': 'title' })
    title.text = h1.text
    children = list(h1)
    h1.clear()
    for child in children:
      title.append(child)

  def __reorganizeNoteMeta(self, note, noteHeader, noteMeta):
    date = None
    tags = None
    for child in noteMeta:
      if child.get('class') == 'date':
        date = child
      elif child.get('class') == 'tags':
        tags = child
    noteMeta.clear()
    if date is not None:
      noteHeader.insert(0, date)
    if tags is not None:
      note.append(tags)