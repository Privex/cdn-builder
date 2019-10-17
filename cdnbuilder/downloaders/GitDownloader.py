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
from tempfile import TemporaryDirectory
from privex.helpers import empty
from cdnbuilder.core import CommandHelper
from cdnbuilder.downloaders.BaseDownloader import BaseDownloader
from cdnbuilder.exceptions import DownloadError


class GitDownloader(BaseDownloader, CommandHelper):
    cmd_exc = DownloadError
    default_command = 'git'
    
    def _download(self, url: str, destination: str = None):
        if empty(destination):
            destination = TemporaryDirectory().name
        self.out_dir = destination
        self._call('clone', '-q', url, destination)
        return destination
