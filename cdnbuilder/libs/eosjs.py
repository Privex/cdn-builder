import json
import logging
from os.path import join
from cdnbuilder.libs.base import BaseLib, LibIdent

log = logging.getLogger(__name__)


class EosJSLib(BaseLib):
    builder = 'YarnBuilder'
    lib_name = 'eosjs'
    url = "https://github.com/EOSIO/eosjs.git"
    output_folder = 'dist-web'
    args = dict(yarn_args=['run', 'build-web'])
    
    def identify(self, folder: str, package: str = None) -> LibIdent:
        """Identify the EOS-JS version using the package.json file, then output a list of the JS files to copy"""
        files = ['eosjs-api.js', 'eosjs-jsonrpc.js', 'eosjs-jssig.js', 'eosjs-numeric.js']
        with open(join(folder, 'package.json')) as fp:
            pkg_json = json.load(fp)
            ver = pkg_json['version']
        files = [join(folder, self.output_folder, f) for f in files]
        return None, ver, files


export = EosJSLib

