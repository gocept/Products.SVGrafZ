################################################################################
## 
## SVGrafZ: do all tests
## $Id: all_tests.py,v 1.7 2003/06/13 12:03:30 mac Exp $
##
################################################################################

import config4test
import unittest
import testRegistry
import testBase
import testBar
import testICRegistry

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testRegistry.RegistryTests, sortUsing=cmp))
    suite.addTest(unittest.makeSuite(testBase.BaseGraphTests))
    suite.addTest(unittest.makeSuite(testBar.SimpleBarGraphTests))
    suite.addTest(unittest.makeSuite(testICRegistry.ICRegistryTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
