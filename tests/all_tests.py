################################################################################
## 
## SVGrafZ: do all tests
## Version: $Id: all_tests.py,v 1.5 2003/05/28 07:06:00 mac Exp $
##
################################################################################

import config
import unittest
import testRegistry
import testBase
import testBar
import testInputConverterRegistry

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testRegistry.RegistryTests, sortUsing=cmp))
    suite.addTest(unittest.makeSuite(testBase.BaseGraphTests))
    suite.addTest(unittest.makeSuite(testBar.SimpleBarGraphTests))
    suite.addTest(unittest.makeSuite(testInputConverterRegistry.\
                                     InputConverterRegistryTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
