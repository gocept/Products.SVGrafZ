################################################################################
## 
## SVGrafZ: do all tests
## Version: $Id: all_tests.py,v 1.3 2003/04/11 13:22:53 mac Exp $
##
################################################################################

import main
import unittest
import testRegistry
import testBase
import testBar


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testRegistry.RegistryTests, sortUsing=cmp))
    suite.addTest(unittest.makeSuite(testBase.BaseGraphTests))
    suite.addTest(unittest.makeSuite(testBar.SimpleBarGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
