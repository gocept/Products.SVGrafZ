################################################################################
## 
## SVGrafZ: Test of Registry
## Version: $Id: testRegistry.py,v 1.10 2003/10/08 07:47:26 mac Exp $
##
################################################################################

import config4test
import unittest
from registry import Registry
from interfaces import IDiagramType, IDiagramKind, IDefaultDiagramKind

class NoDiagramType: pass
class DiagramType1:
    __implements__ = IDiagramType
    name = 'Type1'
    
class DiagramType2:
    __implements__ = IDiagramType
    name = 'Type2'

class NoDiagramKind: pass
class DiagramKind1:
    __implements__ = IDiagramKind
    name = 'Kind1'
    def registration():
        return []
    registration = staticmethod(registration)
    
class DiagramKind2:
    __implements__ = IDiagramKind
    name = 'Kind2'
    def registration():
        return [NoDiagramType]
    registration = staticmethod(registration)
    
class DiagramKind3:
    __implements__ = IDefaultDiagramKind
    name = 'Kind3'
    def registration():
        return [DiagramType1]
    registration = staticmethod(registration)
    
class DiagramKind4:
    __implements__ = IDiagramKind
    name = 'Kind4'
    def registration():
        return [DiagramType1, DiagramType2]
    registration = staticmethod(registration)

class DiagramKind5:
    __implements__ = IDefaultDiagramKind
    name = 'Kind5'
    def registration():
        return [DiagramType2]
    registration = staticmethod(registration)

class DiagramKind6:
    __implements__ = IDiagramKind
    name = 'Kind6'
    def registration():
        return [DiagramType1, DiagramType2]
    registration = staticmethod(registration)



class RegistryTests(unittest.TestCase):
    """Tests for the DiagramType and -Kind Registry.
    """

    def assertNone(self, expr, msg=None):
        """Fail the test unless the expression is None."""
        if expr is not None: raise self.failureException, msg


    def test_1singleton(self):
        """Test if Registry is a singleton."""
        from registry import Registry
        a = Registry
        b = Registry

        self.assertEqual(str(a.__class__), 'registry.Registry', 'classtest')
        self.assertRaises(AttributeError, Registry) # failing of instanciation
        self.assertEqual(a, b, 'a==b')
        a.testAttributeWhichRegistryNeverHas = 'test'
        self.assertEqual(a.testAttributeWhichRegistryNeverHas,
                         b.testAttributeWhichRegistryNeverHas,
                         'a.attrib==b.attrib')

    def test_2_register_get_Type(self):
        """Test _registerType(type) and getType()."""

        n = NoDiagramType
        a = DiagramType1
        b = DiagramType1
        c = DiagramType2

        self.assertEqual([], Registry.getTypes(), 'get from empty reg')
        self.assertRaises(RuntimeError, Registry._registerType, n)
        self.failUnless(Registry._registerType(a), 'register type1')
        self.failIf(Registry._registerType(a), 'register type1 second time')
        self.failIf(Registry._registerType(b), 'register type1 third time')
        
        self.assertEqual([a.name], Registry.getTypes())
        self.failUnless(Registry._registerType(c), 'register type2')
        self.assertEqual([a.name, c.name], Registry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1

        self.failIf(Registry._clear(), '1st clear')
        self.assertEqual([], Registry.getTypes(), '1st get')
        self.failUnless(Registry._registerType(a), 'register type1')
        self.assertEqual([a.name], Registry.getTypes(), '2nd get')
        self.failIf(Registry._clear(), '2nd clear')
        self.assertEqual([], Registry.getTypes(), '3rd get')


    def test_4_register_get_KindNames(self):
        """Test _registerKind and getKindNames."""
        Registry._clear() # remove previously registered Things

        nt = NoDiagramType
        t1 = DiagramType1
        t2 = DiagramType2
        nk = NoDiagramKind
        k1 = DiagramKind1
        k11= DiagramKind1
        k2 = DiagramKind2
        
        self.assertRaises(RuntimeError, Registry._registerKind, nt, nk)
        self.assertRaises(RuntimeError, Registry._registerKind, t1, nk)
        self.assertRaises(RuntimeError, Registry._registerKind, nt, k1)

        self.assertEqual(None, Registry.getKindNames(t1.name), 'get 0')
        self.assertEqual([],
                         Registry.getAllKindNames(),
                         'getall 0: %s' %(Registry.getAllKindNames()))
        

        self.failUnless(Registry._registerKind(t1, k1), 'register t1,k1')
        self.failIf(Registry._registerKind(t1,k1), 'register t1,k1 second time')
        self.failIf(Registry._registerKind(t1,k11), 'register t1,k1 third time')
        
        self.assertEqual([k1.name], Registry.getKindNames(t1.name), 'get 1')
        self.assertEqual(None, Registry.getKindNames(t2.name), 'get 2')
        self.assertEqual([k1.name], Registry.getAllKindNames(), 'getall 1')
        
        
        self.failUnless(Registry._registerKind(t1,k2), 'register t1,k2')
        self.assertEqual([k1.name, k2.name],
                         Registry.getKindNames(t1.name),
                         'get 3')
        self.assertEqual([k1.name,k2.name],
                         Registry.getAllKindNames(),
                         'getall 2: %s' % Registry.getAllKindNames())

        self.failUnless(Registry._registerType(t2), 'register t2')
        self.failUnless(Registry._registerKind(t2,k1), 'register t2,k1')
        self.failIf(Registry._registerKind(t2,k1), 'register t2,k1 2nd')
        self.assertEqual([k1.name], Registry.getKindNames(t2.name), 'get 4')
        self.assertEqual([k1.name,k2.name],
                         Registry.getAllKindNames(),
                         'getall 3')

    def test_45register(self):
        "Test register(diagramKind)."
        Registry._clear()

        t1 = DiagramType1.name
        t2 = DiagramType2.name
        n  = NoDiagramKind
        d1 = DiagramKind1
        d2 = DiagramKind2
        d3 = DiagramKind3
        d32= DiagramKind3
        d4 = DiagramKind4
                                

        self.assertRaises(RuntimeError, Registry.register, n)
        self.assertRaises(RuntimeError, Registry.register, d2)
        self.failUnless(Registry.register(d1), 'reg d1')
        self.failUnless(Registry.register(d1), 'reg d1 2nd')
        self.assertEqual([], Registry.getAllKindNames(), 'getall 1')

        self.failUnless(Registry.register(d3), 'reg d3')
        self.assertRaises(RuntimeError, Registry.register, d3)
        self.assertRaises(RuntimeError, Registry.register, d32)
        self.assertEqual([d3.name], Registry.getKindNames(t1), 'get t1')
        self.assertNone(Registry.getKindNames(t2), 'get t2')
        
        self.failUnless(Registry.register(d4), 'reg d4')
        self.assertEqual([d3.name, d4.name],
                         Registry.getKindNames(t1),
                         'get t1 2nd')
        self.assertEqual([d4.name],
                         Registry.getKindNames(t2),
                         'get t2 2nd')
        self.assertEqual([d3.name, d4.name],
                         Registry.getAllKindNames(),
                         'getall 2')

        
    def test_5getKind(self):
        "Test getKind(name)."
        Registry._clear() # remove previously registered Things
        
        t1 = DiagramType1
        t2 = DiagramType2
        k3 = DiagramKind3
        k4 = DiagramKind4

        self.assertRaises(RuntimeError, Registry.getKind, k3.name)
        self.assertRaises(RuntimeError, Registry.getKind, k4.name)

        self.failUnless(Registry.register(k3), 'reg k3')
        self.assertEqual(k3, Registry.getKind(k3.name), 'get1 k3')
        self.assertRaises(RuntimeError, Registry.getKind, k4.name)

        self.failUnless(Registry.register(k4), 'reg k4')
        self.assertEqual(k3, Registry.getKind(k3.name), 'get2 k3')
        self.assertEqual(k4, Registry.getKind(k4.name), 'get k4')


    def test_6getDefaultKindName(self):
        "Test getDefaultKindName."
        Registry._clear() # remove previously registered things
        
        k3 = DiagramKind3 # default
        k4 = DiagramKind4
        k5 = DiagramKind5 # second default
        k6 = DiagramKind6
        
        self.failIf(Registry.getDefaultKindName(), 'get 0')
        self.failUnless(Registry.register(k4))
        self.failIf(Registry.getDefaultKindName(), 'get 1')
        self.failUnless(Registry.register(k3))
        self.assertEqual(k3.name,
                         Registry.getDefaultKindName(),
                         'get 2 (%s!=%s)' % (k3.name,
                                             Registry.getDefaultKindName()))
        self.assertRaises(RuntimeError, Registry.register, k3) # double reg
        self.assertRaises(RuntimeError, Registry.register, k5) # double reg 2
        self.assertRaises(RuntimeError, Registry.getKind, k5.name) # get 2nd default
        self.failUnless(Registry.register(k6))
        self.assertEqual(k3.name, Registry.getDefaultKindName(), 'get 3')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(RegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
