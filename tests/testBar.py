################################################################################
## 
## SVGrafZ: Test of Class SimpleBarGraph
## Version: $Id: testBar.py,v 1.7 2003/10/08 07:47:26 mac Exp $
##
################################################################################

import config4test
import unittest
from bar import Simple


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
        for t in self.to_test:
            self.failUnless(Simple(data=t), t)

    def test_instantiation2(self):
        "Parametertest for Instantiation."
        a = Simple(data = [[[1,1]]], otherParams={'width':600, 'height':300})
        b = Simple(data = [[[1,1]]], otherParams={'width':300, 'height':300})
        c = Simple(data = [[[1,1]]], otherParams={'width':600, 'height':800})
        d = Simple(data = [[[1,1]]],
                   otherParams = {'width':600, 'height':300},
                   legend = ['test'])

        self.failUnless(a.gridbasey == b.gridbasey, 'a,b gridbasey')
        self.failUnless(a.gridbasex >  b.gridbasex, 'a,b gridbasex')
        self.failUnless(a.gridbasey <  c.gridbasey, 'a,c gridbasey')
        self.failUnless(a.gridbasex == c.gridbasex, 'a,c gridbasex')
        self.failUnless(a.gridboundx > d.gridboundx, 'a,d gridboundx')

    def test_compute(self):
        "Test SimpleBarGraph.compute for exceptions."
        for e in self.errors:
            g = Simple(data=e)
            self.failUnless(RuntimeError, g.compute)
 
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleBarGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
