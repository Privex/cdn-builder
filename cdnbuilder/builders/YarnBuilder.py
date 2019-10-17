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
from typing import Type, List
from cdnbuilder.builders.base import BaseBuilder
from cdnbuilder.core import CommandHelper
import logging

log = logging.getLogger(__name__)


class YarnBuilder(BaseBuilder, CommandHelper):
    # def __init__(self, library: BaseLib):
    #     super().__init__(library=library, args=args)
    yarn_args: List[List[str]]
    out_dir: str
    default_command = 'yarn'
    
    def __init__(self, build_folder: str, yarn_args: List[List[str]], **kwargs):
        super().__init__(build_folder=build_folder, **kwargs)
        self.yarn_args = yarn_args
        self.out_dir = build_folder
    
    def build(self):
        # self.out_dir = self.download()
        self._call('install')
        # If there's just a flat list of arguments, e.g. ['run', 'pack'] - then we're just running a single command
        if type(self.yarn_args[0]) is str:
            self._call(*self.yarn_args)
            return self.out_dir
        # Otherwise, assume it's a list of yarn commands to run
        for cmd in self.yarn_args:   # type: List[str]
            self._call(*cmd)
        return self.out_dir


export = YarnBuilder
