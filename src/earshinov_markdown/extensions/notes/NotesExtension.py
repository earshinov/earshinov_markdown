from .NoteMetaProcessor import NoteMetaProcessor
from .NotesMarkupTreeProcessor import NotesMarkupTreeProcessor
from markdown import Extension


class NotesExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    md.parser.blockprocessors.add('notemeta', NoteMetaProcessor(md), '<paragraph')
    md.treeprocessors.add('notesmarkup', NotesMarkupTreeProcessor(), '<prettify')