################################################################################
## 
## SVGrafZ: Test of Class SimpleBarGraph
## Version: $Id: testBar.py,v 1.1 2003/04/11 13:21:08 mac Exp $
##
################################################################################

import main
import unittest
from bar import SimpleBarGraph


class SimpleBarGraphTests(unittest.TestCase):
    """Tests for the SimpleBarGraph."""

    def setUp(self):
        self.errors = [None,
                       [],
                       [[['Jugendamt', 1.4],['Jugendlicher', 2.6]]],
                       ]
        self.to_test = [[[[1,1],[2,3],[3,3]],
                         [[1,3],[2,1],[3,4]],
                         [[3,5],[5,4],[4,4]]],
                        [[[323493,34534]]],
                        [[[1,1],[1,1]],[[1,2]]],
                        [[[222,233]]],
                        [[[-1234,-2234]]],
                        [[[0,0]]],
                        [[[1000,1000]]],
                        [[[2.3, 'Eltern'],[4.2, 'andere']]],
                        ]

    def test_instantiation(self):
        "Test the instantiation of the class."
        for e in self.errors:
            self.assertRaises(RuntimeError, SimpleBarGraph, e)

        for t in self.to_test:
            self.failUnless(SimpleBarGraph(t), t)

    def test_instantiation2(self):
        "Parametertest for Instantiation."
        a = SimpleBarGraph([[[1,1]]])
        b = SimpleBarGraph([[[1,1]]], width =300)
        c = SimpleBarGraph([[[1,1]]], height=800)
        d = SimpleBarGraph([[[1,1]]], legend=['test'])

        self.failUnless(a.gridbasey == b.gridbasey, 'a,b gridbasey')
        self.failUnless(a.gridbasex >  b.gridbasex, 'a,b gridbasex')
        self.failUnless(a.gridbasey <  c.gridbasey, 'a,c gridbasey')
        self.failUnless(a.gridbasex == c.gridbasex, 'a,c gridbasex')
        self.failUnless(a.gridboundx > d.gridboundx, 'a,d gridboundx')

        print SimpleBarGraph(self.to_test[0], gridlines=4, colnames=['hallo', 'das', 'ist', 'test']).compute()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleBarGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
