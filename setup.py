# -*- coding: utf-8 -*-
"""
Created on Satu Dec  11 23:30:00 2021

@author: ALFONSO Vincent
"""

from distutils.core import setup
import py2exe, os, sys

sys.argv.append('py2exe')

includes = ['Detection_synchrone', 'Motor']

setup(options={'py2exe': {'includes': includes,
                          'compressed': True,
                          'bundle_files': 1}},
      windows=[{'script': 'Interface.py'}])