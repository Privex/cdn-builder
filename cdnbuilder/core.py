"""

Copyright::

    +===================================================+
    |                 © 2019 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        CDN Builder                                |
    |        License: GNU AGPL v3                       |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+

    CDN Builder - A tool written in Python for building and version organising compiled JS/CSS assets
    Copyright (c) 2019    Privex Inc. ( https://www.privex.io )

    This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
    Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
    details.

    You should have received a copy of the GNU Affero General Public License along with this program.
    If not, see <https://www.gnu.org/licenses/>.


"""
import subprocess
from importlib import import_module
from typing import Type
import logging

from privex.helpers import NotConfigured
from cdnbuilder.exceptions import BuildError


log = logging.getLogger(__name__)


def get_builder(name: str):
    """
    
    :param name: Flat, or absolute module name for a builder class e.g. ``YarnBuilder``
    :returns: A builder class, implementing :class:`cdnbuilder.builders.base.BaseBuilder`
    :rtype: Type[cdnbuilder.builders.base.BaseBuilder]
    """
    builder_path = name if '.' in name else f'cdnbuilder.builders.{name}'
    log.debug('Importing builder module: %s', builder_path)
    builder = import_module(builder_path)
    log.debug('Successfully imported: %s', builder_path)
    from cdnbuilder.builders.base import BaseBuilder
    b: BaseBuilder = builder.export
    return b


def load_lib(name: str):
    lib_path = name if '.' in name else f'cdnbuilder.libs.{name}'
    log.debug('Importing library meta module: %s', lib_path)
    _lib = import_module(lib_path)
    log.debug('Successfully imported: %s', lib_path)
    
    from cdnbuilder.libs.base import BaseLib
    lib: Type[BaseLib] = _lib.export
    
    return lib


def call_sys(command: str, *args, cwd=None, **kwargs):
    c = [command] + list(args)
    kw = {
        'cwd': cwd, **kwargs, 'stdout': kwargs.get('stdout', subprocess.PIPE),
        'stderr': kwargs.get('stderr', subprocess.STDOUT)
    }
    return subprocess.Popen(c, **kw)


class CommandHelper:
    out_dir: str
    """The working directory to execute commands within. Set this to ``None`` if it doesn't matter."""
    default_command: str
    """The command to pass arguments to, when using _call. This must be set for :py:meth:`._call` to work."""
    cmd_exc = BuildError
    """The exception to raise when a non-zero return code is detected"""
    
    def _call_raw(self, command: str, *args):
        if not hasattr(self, 'out_dir'):
            raise NotConfigured('Cannot use CommandHelper._call as out_dir was never set!')
        log.debug('Running "%s" with args: %s in working dir: "%s"', command, args, self.out_dir)
        h = call_sys(command, *args, cwd=self.out_dir)
        stdout, stderr = h.communicate()
        log.debug('%s stdout: %s', command.capitalize(), stdout)
        log.debug('%s stderr: %s', command.capitalize(), stderr)
        if h.returncode != 0:
            raise self.cmd_exc(f"{command.capitalize()} returned non-zero return code: {h.returncode}")
        return stdout, stderr, h
    
    def _call(self, *args):
        if not hasattr(self, 'default_command'):
            raise NotConfigured('Cannot use CommandHelper._call as default_command was never set!')
        return self._call_raw(self.default_command, *args)

