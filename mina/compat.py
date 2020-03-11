"""
The MIT License (MIT)

Copyright (c) 2014-2016 Marcwebbie, <http://github.com/marcwebbie>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys


try:
    from shutil import which as _which
except ImportError:
    from distutils.spawn import find_executable as _which

try:
    basestring = basestring
except NameError:
    basestring = str

try:
    unicode = unicode
except NameError:
    unicode = str


def which(binary):
    path = _which(binary)
    if path:
        realpath = os.path.realpath(path)
        return realpath
    return None


def is_python2():
    return sys.version_info < (3,)


class FileNotFoundError(OSError):
    def __init__(self, message="No such file or directory"):
        super(FileNotFoundError, self).__init__(2, message)


class FileExistsError(OSError):
    def __init__(self, message="File exists"):
        super(FileExistsError, self).__init__(17, message)
