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
import logging
import dotenv
from os.path import dirname, abspath, join
from os import getenv as env
from privex.helpers import env_csv

dotenv.load_dotenv()

MOD_DIR = dirname(abspath(__file__))
BASE_DIR = dirname(MOD_DIR)

OUT_FOLDER = env('OUT_FOLDER', join(BASE_DIR, 'output'))
BUILD_FOLDER = env('BUILD_FOLDER', '/tmp')

BUILD_LIBS = env_csv('BUILD_LIBS', ['eosjs', 'scatterjs'])

# Valid environment log levels (from least to most severe) are:
# DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
LOG_LEVEL = env('LOG_LEVEL', None)
LOG_LEVEL = logging.getLevelName(str(LOG_LEVEL).upper()) if LOG_LEVEL is not None else None

if LOG_LEVEL is None:
    LOG_LEVEL = logging.INFO

