#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Description :
   Author :        Asdil
   date：          2018/10/26
-------------------------------------------------
   Change Activity:
                   2018/10/26:
    version = 1.7.2.0
-------------------------------------------------
"""
__author__ = 'Asdil'

from setuptools import setup

setup(name='Asdil',
      version='1.7.2.0',
      description='Tool of Asdil',
      author='Asdil',
      author_email='jpl4job@126.com',
      maintainer='Asdil',
      maintainer_email='jpl4job@126.com',
      license="MIT",
      packages=['Asdil'],
      platforms=["all"],
      url='https://github.com/Asdil/Asdil',
      install_requires=["paramiko",
                        "ConcurrentLogHandler",
                        "mailthon",
                        "scp",
                        "progressbar2",
                        "rsa",
                        "Crypto"],
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Text Processing :: Indexing",
          "Topic :: Utilities",
          "Topic :: Internet",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",])

#  python setup.py check
#  python setup.py sdist
#  python setup.py register -r pypi
#  python setup.py sdist upload -r pypi
