################################################################################
## 
## SVGrafZ: do all tests
## Version: $Id: all_tests.py,v 1.1 2003/04/10 13:58:50 mac Exp $
##
################################################################################

import main
import unittest
import testRegistry
import testBase

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(testRegistry.RegistryTests, sortUsing=cmp))
    suite.addTest(unittest.makeSuite(testBase.BaseGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
