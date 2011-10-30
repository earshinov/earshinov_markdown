#!/usr/bin/env python3

from earshinov_markdown import FileOperator
from earshinov_markdown.converters import SimpleMarkdownConverter
from earshinov_markdown.extensions import DefaultExtensions, HtmlHeaderExtension
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*')
parser.add_argument('--no-header', dest='header', action='store_false', help='skip HTML header')
args = parser.parse_args()

DefaultExtensions.patchMarkdownGlobals()
extensions = DefaultExtensions().get()
if args.header:
  extensions.append(HtmlHeaderExtension())

FileOperator(
  SimpleMarkdownConverter(extensions)
).processConsole([sys.argv[0]] + args.files)
