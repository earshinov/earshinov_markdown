from .NoteMetaProcessor import NotesMetaProcessorExtension
from .NotesMarkupTreeProcessor import NotesMarkupTreeProcessor
from markdown import Extension


class NotesExtension(Extension):

  def extendMarkdown(self, md, md_globals):
    NotesMetaProcessorExtension().extendMarkdown(md, md_globals)
    md.treeprocessors.add('notesmarkup', NotesMarkupTreeProcessor(), '<prettify')