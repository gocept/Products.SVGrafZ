################################################################################
## 
## SVGrafZ: do all tests
## Version: $Id: all_tests.py,v 1.2 2003/04/11 13:21:08 mac Exp $
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
    suite.addTest(unittest.makeSuite(testBase.SimpleBarGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
