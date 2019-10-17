#!/usr/bin/env python3
import unittest
from cdnbuilder.libs.scatterjs import ScatterJSLib


class TestLibScatterJS(unittest.TestCase):
    version_header = "/*!\n *\n * ScatterJS - plugin-eosjs2 v1.5.28\n * https://github.com/GetScatter/scatter-js/\n" \
                     " * Released under the MIT license.\n *\n */\n"
    
    def test_ident_version(self):
        pkg, ver = ScatterJSLib._get_version(self.version_header)
        self.assertEqual(pkg, 'plugin-eosjs2')
        self.assertEqual(ver, '1.5.28')


if __name__ == "__main__":
    unittest.main()
