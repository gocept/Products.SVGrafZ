################################################################################
## 
## SVGrafZ: Test of Class SimpleBarGraph
## Version: $Id: testBar.py,v 1.5 2003/06/13 12:03:30 mac Exp $
##
################################################################################

import config4test
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
        for t in self.to_test:
            self.failUnless(SimpleBarGraph(data=t), t)

    def test_instantiation2(self):
        "Parametertest for Instantiation."
        a = SimpleBarGraph(data = [[[1,1]]], width=600, height=300)
        b = SimpleBarGraph(data = [[[1,1]]], width=300, height=300)
        c = SimpleBarGraph(data = [[[1,1]]], width=600, height=800)
        d = SimpleBarGraph(data = [[[1,1]]],
                           width=600,
                           height=300,
                           legend=['test'])

        self.failUnless(a.gridbasey == b.gridbasey, 'a,b gridbasey')
        self.failUnless(a.gridbasex >  b.gridbasex, 'a,b gridbasex')
        self.failUnless(a.gridbasey <  c.gridbasey, 'a,c gridbasey')
        self.failUnless(a.gridbasex == c.gridbasex, 'a,c gridbasex')
        self.failUnless(a.gridboundx > d.gridboundx, 'a,d gridboundx')

    def test_compute(self):
        "Test SimpleBarGraph.compute for exceptions."
        for e in self.errors:
            g = SimpleBarGraph(data=e)
            self.failUnless(RuntimeError, g.compute)
 
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleBarGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
