################################################################################
## 
## SVGrafZ: Test of Registry
## Version: $Id: testRegistry.py,v 1.1 2003/04/09 12:25:55 mac Exp $
##
################################################################################

import sys
sys.path.append('/home/zagy/zope/servers/Zope-HEAD/lib/python')
sys.path.append('/home/mac/Instance/Products/SVGrafZ')


import unittest
from registry import Registry
from interfaces import IDiagramType, IDiagramKind

def pdb():
    import pdb
    pdb.set_trace()

class NoDiagramType:
    pass
class DiagramType1:
    __implements__ = IDiagramType
    def name(self): return 'Type1'
    
class DiagramType2:
    __implements__ = IDiagramType
    def name(self): return 'Type2'

class NoDiagramKind:
    pass
class DiagramKind1:
    __implements__ = IDiagramKind
    def name(self): return 'Kind1'
    
class DiagramKind2:
    __implements__ = IDiagramKind
    def name(self): return 'Kind2'


class RegistryTests(unittest.TestCase):
    """Tests for the DiagramType and -Kind Registry.
    """

    def test_1singleton(self):
        """Test if Registry is a singleton."""
        from registry import Registry
        a = Registry
        b = Registry

        self.assertEqual(str(a.__class__), 'registry.Registry', 'classtest')
        self.assertRaises(AttributeError, Registry) # failig of instanciation
        self.assertEqual(a, b, 'a==b')
        a.testAttributeWhichRegistryNeverHas = 'test'
        self.assertEqual(a.testAttributeWhichRegistryNeverHas,
                         b.testAttributeWhichRegistryNeverHas,
                         'a.attrib==b.attrib')

    def test_2register_get_Type(self):
        """Test registerType(type) and getType()."""

        n = NoDiagramType()
        a = DiagramType1()
        b = DiagramType1()
        c = DiagramType2()
        
        self.assertRaises(RuntimeError, Registry.registerType, n)
        self.failUnless(Registry.registerType(a), 'register type1')
        self.failIf(Registry.registerType(a), 'register type1 second time')
        self.failIf(Registry.registerType(b), 'register type1 third time')
        
        self.assertEqual(['Type1'], Registry.getTypes())
        self.failUnless(Registry.registerType(c), 'register type2')
        self.assertEqual(['Type1', 'Type2'], Registry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1()

        self.failIf(Registry._clear(), '1st clear')
        self.failIf(Registry.getTypes(), '1st get')
        self.failUnless(Registry.registerType(a), 'register type1')
        self.failUnless(Registry.getTypes(), '2nd get')
        self.failIf(Registry._clear(), '2nd clear')
        self.failIf(Registry.getTypes(), '3rd get')

    def test_4register_get_Kind(self):
        """Test registerKind and getKind."""
        Registry._clear() # remove previously registered Things

        nt = NoDiagramType()
        t1 = DiagramType1()
        t2 = DiagramType2()
        nk = NoDiagramKind()
        k1 = DiagramKind1()
        k11= DiagramKind1()
        k2 = DiagramKind2()
        
        self.assertRaises(RuntimeError, Registry.registerKind, nt, nk)
        self.assertRaises(RuntimeError, Registry.registerKind, t1, nk)
        self.assertRaises(RuntimeError, Registry.registerKind, nt, k1)

        self.failUnless(Registry.registerKind(t1, k1), 'register t1,k1')
        self.failIf(Registry.registerKind(t1,k1), 'register t1,k1 second time')
        self.failIf(Registry.registerKind(t1,k11), 'register t1,k1 third time')
        
        self.assertEqual({k1.name():k1}, Registry.getKinds(t1.name()), 'get 1')
        self.assertEqual(None, Registry.getKinds(t2.name()), 'get 2')
        
        self.failUnless(Registry.registerKind(t1,k2), 'register t1,k2')
        self.assertEqual({k1.name():k1, k2.name():k2},
                         Registry.getKinds(t1.name()),
                         'get 3')

        self.failUnless(Registry.registerType(t2), 'register t2')
        self.failUnless(Registry.registerKind(t2,k1), 'register t2,k1')
        self.failIf(Registry.registerKind(t2,k1), 'register t2,k1 2nd')
        self.assertEqual({k1.name():k1},
                         Registry.getKinds(t2.name()),
                         'get 4')

        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
