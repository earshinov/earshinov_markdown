#!/usr/bin/env python3

from earshinov_markdown import FileOperator
from earshinov_markdown.converters import InlineMarkdownConverter, \
  NotesMarkdownConverter, SimpleMarkdownConverter
from earshinov_markdown.extensions import DefaultExtensions
from earshinov_markdown.extensions.notes import NotesExtension
import sys


DefaultExtensions.patchMarkdownGlobals()

FileOperator(
  InlineMarkdownConverter(
  NotesMarkdownConverter(
  SimpleMarkdownConverter(DefaultExtensions.get() + [
    NotesExtension(),
  ])))
).processConsole(sys.argv)