################################################################################
## 
## SVGrafZ: do all tests
## Version: $Id: all_tests.py,v 1.4 2003/05/27 15:24:09 mac Exp $
##
################################################################################

import config
import unittest
import testRegistry
import testBase
import testBar
import testInputKonverterRegistry

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testRegistry.RegistryTests, sortUsing=cmp))
    suite.addTest(unittest.makeSuite(testBase.BaseGraphTests))
    suite.addTest(unittest.makeSuite(testBar.SimpleBarGraphTests))
    suite.addTest(unittest.makeSuite(testInputKonverterRegistry.\
                                     InputKonverterRegistryTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
