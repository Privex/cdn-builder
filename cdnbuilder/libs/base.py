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
from abc import abstractmethod, ABC
from os.path import basename, join
from tempfile import TemporaryDirectory
from typing import List, Tuple, Type, Optional
from importlib import import_module

from privex.helpers import is_true

from cdnbuilder import settings
from cdnbuilder.builders.base import BaseBuilder
from cdnbuilder.downloaders.BaseDownloader import BaseDownloader
from cdnbuilder.downloaders.GitDownloader import GitDownloader
import logging

log = logging.getLogger(__name__)


class FileOutput(dict):
    src: str
    version: str
    package: Optional[str]
    dest_folder: Optional[str]
    link_root: bool
    
    def __init__(self, src: str, version: str, package: str = None, **kwargs):
        """
        
        :param str src: Absolute path to the source file to copy from
        :param str version: The version of the file
        :param str package: The sub-package/component the file belongs to, if applicable
        :key str dest_folder: The sub-folder to place this file into
        :key bool link_root: (Default: ``False``) If True, symlink this file to the root of the package output folder
        """
        super().__init__(src=src, version=version, package=package, **kwargs)
        # dest_folder: str = None, link_root=False
        self.src, self.version, self.package = src, version, package
        self.dest_folder = kwargs.get('dest_folder')
        self.link_root = is_true(kwargs.get('link_root', False))
    
    @property
    def filename(self):
        return basename(self.src)
    
    @property
    def pkg_folder(self) -> str:
        """
        Returns the relative package folder, including sub-package name + dest folder if set.
        Example: 'mycomponent/1.2.3/extras' (sub pkg + dest folder)   or   '2.3.4' (main package)
        """
        df = '' if not self.dest_folder else self.dest_folder
        pkg = '' if not self.package else self.package
        return join(pkg, self.version, df)


LibIdent = Tuple[Optional[str], str, List[str]]
"""
Output format for BaseLib.identify:
1 - Name of the identified package (for creating a folder if needed to organise)
2 - Version of the identified package (for organising the file(s) into a version sub-folder)
3 - A list of one or more absolute paths to asset files or folders considered to be in this package version

Example:

    ( 'jquery', '1.2.5', ['/tmp/jq/dist/jquery.js', '/tmp/jq/dist/jquery.min.js'], )

"""


class LibBuilderHelper:
    builder: str
    args: dict

    @classmethod
    def get_builder(cls, build_folder: str) -> BaseBuilder:
        _builder = cls.import_builder(name=cls.builder)
        return _builder(build_folder=build_folder, **cls.args)

    @staticmethod
    def import_builder(name: str) -> Type[BaseBuilder]:
        builder_path = name if '.' in name else f'cdnbuilder.builders.{name}'
        log.debug('Importing builder module: %s', builder_path)
        builder = import_module(builder_path)
        log.debug('Successfully imported: %s', builder_path)
        return builder.export

    
class BaseLib(ABC, LibBuilderHelper):
    """
    Base class for library helper classes.

    Note: :py:attr:`.builder` and :py:attr:`.lib_name` generally should be defined as simple static attributes. They
    do not need to be actual property methods.

    Example:

        >>> class MyLib(BaseLib):
        ...     lib_name = 'my-lib'
        ...     builder = 'YarnBuilder'
        ...


    """

    @property
    @abstractmethod
    def builder(self) -> str:
        """Name of the builder module to use to build the distributable files"""
        pass

    @property
    @abstractmethod
    def lib_name(self) -> str:
        """The name of the library that your implementing class represents - will be used as the folder name"""
        pass
    
    url: str = None
    """URL (e.g. Git repo) to download package source code from"""

    args: dict = {}
    """Any configuration options to pass to the builder class __init__"""

    subpackages: List[str] = []
    """If the package produces multiple, individually versioned dist files, you should specify them here"""

    output_folder: str = "dist"
    """The folder (relative from the root of the git url) where the dist files would be outputted to"""
    
    downloader_cls: Type[BaseDownloader] = GitDownloader
    """Downloader class to use to load the source code from :py:attr:`.url`"""
    
    link_root: bool = True
    """Symlink all component files back to the root package folder"""
    
    include_main: bool = True
    """Include :py:meth:`.identify` without any sub-package specified in the :py:meth:`.build` output"""
    
    include_sub: bool = True
    """Include :py:meth:`.identify` for each sub-package in the :py:meth:`.build` output"""
    
    def __init__(self):
        self.downloader = self.downloader_cls(self.lib_name, self.url)
        self.temp_dir_obj = TemporaryDirectory(prefix=self.lib_name, dir=settings.BUILD_FOLDER)
        self.temp_dir = self.temp_dir_obj.name

    def download(self) -> str:
        dl = self.downloader
        return dl.download(out_dir=self.temp_dir) if not dl.downloaded else dl.folder
    
    @abstractmethod
    def identify(self, folder: str, package: str = None) -> LibIdent:
        """
        After a lib has been built / compiled etc., this method will be called with the absolute path
        to the root folder for the package source code, and optionally a sub-package name.

        This method should extract the (sub-)package version, a folder-safe sub-package name (if ``package`` is not
        None), and a ``List[str]`` of absolute paths to each asset file/folder to copy into the output folder
        for this package version.

        Example:

            >>> import os.path
            >>> def identify(folder: str, package: str = None):
            ...     pkg_ver = '1.2.5'   # Somehow identify the (sub-)package version using the source code folder.
            ...     return package, pkg_ver, [os.path.join(folder, 'dist', 'jquery.min.js')]
            >>> pkg, ver, files = identify('/tmp/jq')
            >>> print(f'Package: {pkg} - Version: {ver} - Files: {files}')
            Package: None - Version: 1.2.5 - Files: ['/tmp/jq/dist/jquery.min.js']


        :param str folder: The absolute path to the root of the package source code (e.g. the root of the git url)
        :param str package: (Optional) If specified, identify the version of this sub-package
        :return LibIdent ver: A 3-item tuple of ``(pkg_name, pkg_ver, pkg_files)`` - see below for more info.

        The ``identify`` function should return a tuple of 3 items:

         * sub-package name (used as a sub-folder name) - can be ``None`` for the main package (or if no sub-packages)
         * (sub-)package version
         * list of absolute paths to distributable files/folders to be copied to the output folder for this version.

        Return Example:

            ( 'jquery', '1.2.5', ['/tmp/jq/dist/jquery.js', '/tmp/jq/dist/jquery.min.js'] )


        """
        pass

    def build(self) -> List[FileOutput]:
        # Download the repo
        log.info('Downloading repo...')
        dest = self.download()
        log.info('Initialising builder...')
        # Initialise the builder with the repo download folder
        builder = self.get_builder(build_folder=dest)
        # Trigger the build in the repo
        log.info('Triggering build...')
        dest = builder.build()
        log.info('Scanning versions')
        # Generate the list of files to save
        versions = []
        
        if self.include_main:
            versions += [self.identify(dest)]
        
        if self.include_sub:
            versions += [self.identify(dest, package=pkg) for pkg in self.subpackages]
        
        result = []
        for pkg, ver, files in versions:
            for f in files:
                result.append(FileOutput(src=f, package=pkg, version=ver, link_root=True))
        return result
