################################################################################
## 
## SVGrafZ: Test of InputConverterRegistry
## Version: $Id: testInputKonverterRegistry.py,v 1.1 2003/05/27 15:24:09 mac Exp $
##
################################################################################

import config
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
    name = 'Type1'
    
class DiagramType2:
    __implements__ = IDiagramType
    name = 'Type2'

class NoDiagramKind:
    pass
class DiagramKind1:
    __implements__ = IDiagramKind
    name = 'Kind1'
    
class DiagramKind2:
    __implements__ = IDiagramKind
    name = 'Kind2'


class InputKonverterRegistryTests(unittest.TestCase):
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

        n = NoDiagramType
        a = DiagramType1
        b = DiagramType1
        c = DiagramType2
        
        self.assertRaises(RuntimeError, Registry.registerType, n)
        self.failUnless(Registry.registerType(a), 'register type1')
        self.failIf(Registry.registerType(a), 'register type1 second time')
        self.failIf(Registry.registerType(b), 'register type1 third time')
        
        self.assertEqual(['Type1'], Registry.getTypes())
        self.failUnless(Registry.registerType(c), 'register type2')
        self.assertEqual(['Type1', 'Type2'], Registry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1

        self.failIf(Registry._clear(), '1st clear')
        self.failIf(Registry.getTypes(), '1st get')
        self.failUnless(Registry.registerType(a), 'register type1')
        self.failUnless(Registry.getTypes(), '2nd get')
        self.failIf(Registry._clear(), '2nd clear')
        self.failIf(Registry.getTypes(), '3rd get')

    def test_4register_get_KindNames(self):
        """Test registerKind and getKindNames."""
        Registry._clear() # remove previously registered Things

        nt = NoDiagramType
        t1 = DiagramType1
        t2 = DiagramType2
        nk = NoDiagramKind
        k1 = DiagramKind1
        k11= DiagramKind1
        k2 = DiagramKind2
        
        self.assertRaises(RuntimeError, Registry.registerKind, nt, nk)
        self.assertRaises(RuntimeError, Registry.registerKind, t1, nk)
        self.assertRaises(RuntimeError, Registry.registerKind, nt, k1)

        self.assertEqual(None, Registry.getKindNames(t1.name), 'get 0')
        self.assertEqual([],
                         Registry.getAllKindNames(),
                         'getall 0: %s' %(Registry.getAllKindNames()))
        

        self.failUnless(Registry.registerKind(t1, k1), 'register t1,k1')
        self.failIf(Registry.registerKind(t1,k1), 'register t1,k1 second time')
        self.failIf(Registry.registerKind(t1,k11), 'register t1,k1 third time')
        
        self.assertEqual([k1.name], Registry.getKindNames(t1.name), 'get 1')
        self.assertEqual(None, Registry.getKindNames(t2.name), 'get 2')
        self.assertEqual([k1.name], Registry.getAllKindNames(), 'getall 1')
        
        
        self.failUnless(Registry.registerKind(t1,k2), 'register t1,k2')
        self.assertEqual([k1.name, k2.name], Registry.getKindNames(t1.name), 'get 3')
        self.assertEqual([k1.name,k2.name],
                         Registry.getAllKindNames(),
                         'getall 2: %s' % Registry.getAllKindNames())

        self.failUnless(Registry.registerType(t2), 'register t2')
        self.failUnless(Registry.registerKind(t2,k1), 'register t2,k1')
        self.failIf(Registry.registerKind(t2,k1), 'register t2,k1 2nd')
        self.assertEqual([k1.name], Registry.getKindNames(t2.name), 'get 4')
        self.assertEqual([k1.name,k2.name], Registry.getAllKindNames(), 'getall 3')

    def test_5getKind(self):
        "Test getKind."
        Registry._clear() # remove previously registered Things
        
        t1 = DiagramType1
        t2 = DiagramType2
        k1 = DiagramKind1
        k2 = DiagramKind2

        self.assertRaises(RuntimeError, Registry.getKind, k1.name)
        self.assertRaises(RuntimeError, Registry.getKind, k2.name)

        self.failUnless(Registry.registerKind(t1, k1), 'register t1,k1')
        self.assertEqual(k1, Registry.getKind(k1.name), 'get1 k1')
        self.assertRaises(RuntimeError, Registry.getKind, k2.name)

        self.failUnless(Registry.registerKind(t2, k1), 'register t2,k1')
        self.assertEqual(k1, Registry.getKind(k1.name), 'get2 k1')
        self.assertRaises(RuntimeError, Registry.getKind, k2.name)

        self.failUnless(Registry.registerKind(t2, k2), 'register t1,k2')
        self.assertEqual(k1, Registry.getKind(k1.name), 'get3 k1')
        self.assertEqual(k2, Registry.getKind(k2.name), 'get4 k2')


    def test_6getDefaultKindName(self):
        "Test getDefaultKindName."
        Registry._clear() # remove previously registered Things
        
        t1 = DiagramType1
        k1 = DiagramKind1
        k2 = DiagramKind2
        
        self.failIf(Registry.getDefaultKindName(), 'get 0')
        self.failUnless(Registry.registerType(t1))
        self.failIf(Registry.getDefaultKindName(), 'get 1')
        self.failUnless(Registry.registerKind(t1, k2))
        self.assertEqual(k2.name, Registry.getDefaultKindName(), 'get 2')
        self.failUnless(Registry.registerKind(t1, k1))
        self.assertEqual(k2.name, Registry.getDefaultKindName(), 'get 3')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
