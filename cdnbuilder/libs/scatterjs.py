import re
import logging
from os.path import join
from typing import Tuple
from cdnbuilder.exceptions import VersionNotFound
from cdnbuilder.libs.base import BaseLib, LibIdent

log = logging.getLogger(__name__)


class ScatterJSLib(BaseLib):
    builder = 'YarnBuilder'
    lib_name = 'scatter-js'
    url = "https://github.com/GetScatter/scatter-js.git"
    output_folder = 'bundles'
    args = dict(yarn_args=['run', 'pack'])
    subpackages = ["core", "plugin-eosjs", "plugin-eosjs2", "plugin-lynx", "plugin-tron", "plugin-web3"]
    include_main = False
    
    vreg = re.compile(r'ScatterJS - ([a-zA-Z0-9-]+) v([0-9.-]+)')

    @classmethod
    def _get_version(cls, contents: str, package: str = None) -> Tuple[str, str]:
        """
        Extract the package name and version number from the version comment within the contents of
        a generated JS file.
        
        :param str contents: The contents of a JS file as a string, to be regex'd for the actual package + version
        :param str package: Optional - the name of the package being identified. Only used for more specific exceptions.
        
        :raises VersionNotFound: Raised if regex search can't find the version info.
        
        :return tuple ver: The package name + version ``('plugin-eosjs2', '1.5.28')``
        """
        r = cls.vreg.findall(contents)
        if len(r) < 1:
            p_err = ' for ScatterJS' if not package else f' for ScatterJS sub-package "{package}"'
            raise VersionNotFound(f'{__name__} - could not find version{p_err}')
        return r[0]
    
    def identify(self, folder: str, package: str = None) -> LibIdent:
        f_loc = join(folder, self.output_folder, f"scatterjs-{package}.min.js")
        with open(f_loc, 'r') as fp:
            data = fp.read()
            pkg, ver = self._get_version(contents=data, package=package)
            return pkg, ver, [f_loc]


export = ScatterJSLib

