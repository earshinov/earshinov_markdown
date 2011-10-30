#!/usr/bin/env python3

from earshinov_markdown import FileOperator
from earshinov_markdown.converters import InlineMarkdownConverter, \
  SimpleMarkdownConverter
from earshinov_markdown.extensions import DefaultExtensions
import sys


DefaultExtensions.patchMarkdownGlobals()

FileOperator(
  InlineMarkdownConverter(
  SimpleMarkdownConverter(DefaultExtensions().get()))
).processConsole(sys.argv)
