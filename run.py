#!/usr/bin/env python3
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
import sys
import textwrap
import argparse
from os import path, makedirs, symlink
from shutil import copyfile

from privex.helpers import ErrHelpParser, empty

from cdnbuilder import settings, VERSION
from cdnbuilder.core import load_lib
import logging

log = logging.getLogger('cdnbuilder.cli')


CMD_DESC = {
    'build': f'With no arguments, builds all libraries specified in BUILD_LIBS. Otherwise, builds (library)',
}

HELP_TEXT = textwrap.dedent(f'''\

CDN Builder Version v{VERSION}
(C) 2019 Privex Inc. ( https://wwww.privex.io )
Official Repo: https://github.com/Privex/cdn-builder


Sub-commands:

    build  (library)                - {CMD_DESC['build']}

''')

parser = ErrHelpParser(
    description='CDN Builder - Painless automatic building of JS/CSS libraries + version organisation',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=HELP_TEXT
)


def ap_build(opt):
    lib = opt.lib
    # If no library name was passed on the CLI args, then just build all libraries listed in BUILD_LIBS
    if empty(lib):
        for l in settings.BUILD_LIBS:
            try:
                build_lib(l)
            except:
                log.exception('Unexpected error while building library "%s"...', l)
        return
    build_lib(lib)


def build_lib(l, force=False):
    # Load the library helper class and build it
    lib = load_lib(l)()
    files = lib.build()
    
    lib_folder = path.join(settings.OUT_FOLDER, lib.lib_name)
    # Create the versioned directory structure for the library distribution files, and copy each file to the
    # appropriate folder within the directory structure.
    for f in files:
        pkg_folder = path.join(lib_folder, f.pkg_folder)
        out_file = path.join(pkg_folder, f.filename)
        if not path.exists(pkg_folder):
            makedirs(pkg_folder)
        if path.exists(out_file) and not force:
            log.warning('The file "%s" already exists. Skipping.', out_file)
            continue
        log.info('Copying "%s" to "%s"', f.src, out_file)
        copyfile(f.src, out_file)
        if lib.link_root:
            link_dst = path.join(lib_folder, f.filename)
            log.info('Creating symlink from "%s" to "%s"', out_file, link_dst)
            symlink(out_file, link_dst)


sp = parser.add_subparsers()

parse_build = sp.add_parser('build', description=CMD_DESC['build'])
parse_build.add_argument('lib', default=None, help='Library to build', nargs='?')

parse_build.set_defaults(func=ap_build)


# Resolves the error "'Namespace' object has no attribute 'func'
# Taken from https://stackoverflow.com/a/54161510/2648583
try:
    args = parser.parse_args()
    func = args.func
    func(args)
except AttributeError:
    parser.error('Too few arguments')
    sys.exit(1)


