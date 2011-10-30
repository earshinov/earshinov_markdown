#!/usr/bin/env python3

from earshinov_markdown import FileOperator
from earshinov_markdown.converters import InlineMarkdownConverter, \
  ResettingMarkdownConverter, SimpleMarkdownConverter
from earshinov_markdown.extensions import DefaultExtensions
import sys


DefaultExtensions.patchMarkdownGlobals()

FileOperator(
  InlineMarkdownConverter(
  ResettingMarkdownConverter(
  SimpleMarkdownConverter(DefaultExtensions().get())))
).processConsole(sys.argv)
