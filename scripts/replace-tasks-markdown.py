#!/usr/bin/env python3

from earshinov_markdown import FileOperator
from earshinov_markdown.converters import InlineMarkdownConverter, \
  ResettingMarkdownConverter, SimpleMarkdownConverter
from earshinov_markdown.extensions import DefaultExtensions
from earshinov_markdown.extensions.tasks import TasksExtension
import sys


DefaultExtensions.patchMarkdownGlobals()

FileOperator(
  InlineMarkdownConverter(
  ResettingMarkdownConverter(
  SimpleMarkdownConverter(DefaultExtensions.get() + [
    TasksExtension(),
  ])))
).processConsole(sys.argv)
