################################################################################
## 
## SVGrafZ: Test of Class BaseGraph
## Version: $Id: testBase.py,v 1.1 2003/04/10 13:58:50 mac Exp $
##
################################################################################

import main
import unittest
from base import BaseGraph

class BaseGraphData(BaseGraph):
    "Concrete subclass of BaseGraph, to get data into it."
    def __init__(self, data, legend=None):
        self.data = data
        self.legend = legend
    

class BaseGraphTests(unittest.TestCase):
    """Tests for the DiagramType and -Kind Registry.
    """

    def setUp(self):
        self.errors = [None,[],]
        self.to_test = [[[[1,1],[2,3],[3,3]],
                         [[1,3],[2,1],[3,4]],
                         [[3,5],[5,4],[4,4]]],
                        [[[323493,34534]]],
                        [[[1,1],[1,1]],[[1,2]]],
                        [[[222,233]]],
                        [[[-1234,-2234]]],
                        [[[0,0]]],
                        [[[1000,1000]]],                        
                        ]

    def test_hasLegend(self):
        """Test hasLegend."""
        a = BaseGraphData(None, None)
        b = BaseGraphData([1,2], None)
        c = BaseGraphData(None, 1)
        d = BaseGraphData(None, [])
        e = BaseGraphData(None, ['item1', 'item2'])

        self.failIf(a.hasLegend(), 'a')
        self.failIf(b.hasLegend(), 'b')
        self.failIf(c.hasLegend(), 'c')
        self.failIf(d.hasLegend(), 'd')
        self.failUnless(e.hasLegend(), 'e')



    def test__testFormatOfData(self):
        "Test _testFormatOfData."
        tf = [None,
              [],
              [[]],
              [[[]]],
              {},
              (),
              [{'a':[1,1]}],
              [[[1,1]],3],
              [[[1,1], 3],[[2,2]]],
              [[[1,2,3]]],
              [[[[1,2]]]],
              ]
        ts = [[[[1,1]]],
              [[[1,2],[1,3]]],
              [[[1,2],[1,3]],[[2,1],[2,2]]],
              [[['hallo', 2.34]],[['huhu', 10L]]],
              ]
        for t in tf:
            g = BaseGraphData(t)
            self.assertRaises(RuntimeError, g._testFormatOfData)

        for t in ts:
             g = BaseGraphData(t)
             self.failUnless(g._testFormatOfData(), 'error on %s' % str(t))



    def test_realMinX(self):
        "Test realMinX."
        res = [1,323493,1,222,-1234,0,1000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.realMinX)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.realMinX(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.realMinX(),
                                                 str(self.to_test[i])))

    def test_minX(self):
        "Test minX."
        res = [0,200000,0,100,-3000,0,0]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.minX)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.minX(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.minX(),
                                                 str(self.to_test[i])))


    def test_realMaxX(self):
        "Test realMaxX."
        res = [5,323493,1,222,-1234,0,1000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.realMaxX)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.realMaxX(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.realMaxX(),
                                                 str(self.to_test[i])))

    def test_maxX(self):
        "Test maxX."
        res = [6,500000,2,400,0,0,2000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.maxX)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.maxX(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.maxX(),
                                                 str(self.to_test[i])))

    def test_realMinY(self):
        "Test realMinY."
        res = [1,34534,1,233,-2234,0,1000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.realMinY)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.realMinY(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.realMinY(),
                                                 str(self.to_test[i])))

    def test_minY(self):
        "Test minY."
        res = [0,20000,0,100,-4000,0,0]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.minY)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.minY(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.minY(),
                                                 str(self.to_test[i])))


    def test_realMaxY(self):
        "Test realMaxY."
        res = [5,34534,2,233,-2234,0,1000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.realMaxY)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.realMaxY(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.realMaxY(),
                                                 str(self.to_test[i])))

    def test_maxY(self):
        "Test maxY."
        res = [6,50000,3,400,-1000,0,2000]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.maxY)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.maxY(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.maxY(),
                                                 str(self.to_test[i])))


    def test_countDistX(self):
        "Test countDistX."
        res = [5,1,1,1,1,1,1]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.countDistX)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.countDistX(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.countDistX(),
                                                 str(self.to_test[i])))


    def test_countDistY(self):
        "Test countDistY."
        res = [4,1,2,1,1,1,1]

        for j in self.errors:
            g = BaseGraphData(j)
            self.assertRaises(RuntimeError,
                              g.countDistY)

        for i in range(len(self.to_test)):
            g = BaseGraphData(self.to_test[i])
            self.assertEqual(res[i],
                             g.countDistY(),
                             '%i != %i (%s)1' % (res[i],
                                                 g.countDistY(),
                                                 str(self.to_test[i])))

    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseGraphTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')