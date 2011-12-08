#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='earshinov_markdown',
    package_dir={ '': 'src' },
    packages=['earshinov_markdown','earshinov_markdown.extensions','earshinov_markdown.lib','earshinov_markdown.utils'],
    py_modules=['mdx_ea_auto_link_target', 'mdx_ea_strike', 'mdx_ea_urlize'])
