# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: do all tests
## $Id: all_tests.py,v 1.8 2003/10/15 07:08:34 mac Exp $
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
