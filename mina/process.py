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

from .compat import basestring
from subprocess import PIPE
from subprocess import Popen

import logging
import os


DEVNULL = open(os.devnull, "w")


class Proc(Popen):
    def communicate(self, **kwargs):
        if kwargs.get("input") and isinstance(kwargs["input"], basestring):
            kwargs["input"] = kwargs["input"].encode("utf-8")
        return super(Proc, self).communicate(**kwargs)

    def __exit__(self, *args, **kwargs):
        if hasattr(super(Proc, self), "__exit__"):
            super(Proc, self).__exit__(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        if hasattr(super(Proc, self), "__enter__"):
            return super(Proc, self).__enter__(*args, **kwargs)
        return self


def call(*args, **kwargs):
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        stderr = PIPE
    else:
        stderr = DEVNULL

    kwargs.setdefault("stderr", stderr)
    kwargs.setdefault("stdout", PIPE)
    kwargs.setdefault("stdin", PIPE)
    kwargs.setdefault("shell", False)
    kwargs_input = kwargs.pop("input", None)

    with Proc(*args, **kwargs) as proc:
        logging.debug(" ".join(args[0]))
        output, error = proc.communicate(input=kwargs_input)
        try:
            output = output.decode("utf-8")
            error = error.decode("utf-8")
        except AttributeError:
            pass
        return output, error
