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
from abc import ABC, abstractmethod
from tempfile import mkdtemp
from typing import Optional
from cdnbuilder import settings
import logging

log = logging.getLogger(__name__)


class BaseDownloader(ABC):
    downloaded: bool
    folder: Optional[str]
    
    def __init__(self, lib_name: str, url: str):
        self.lib_name = lib_name
        self.url = url
        self.downloaded = False
        self.folder = None
    
    @abstractmethod
    def _download(self, url: str, destination: str = None) -> str:
        pass

    def download(self, out_dir=None) -> str:
        if not out_dir:
            out_dir = mkdtemp(prefix=self.lib_name, dir=settings.BUILD_FOLDER)
        log.info('Downloading library %s into folder "%s"', self.lib_name, out_dir)
        d = self._download(url=self.url, destination=out_dir)
        self.downloaded = True
        self.folder = d
        return d
