################################################################################
## 
## SVGrafZ: Test of ICRegistry
## $Id: testICRegistry.py,v 1.3 2003/06/13 08:43:23 mac Exp $
##
################################################################################

import config
import unittest
from icreg import ICRegistry
from interfaces import IDiagramType, IInputConverter, IDefaultInputConverter,\
     IDataSource

def pdb():
    import pdb
    pdb.set_trace()

class NoDiagramType: pass
class DiagramType1:
    __implements__ = IDiagramType
    name = 'Type1'
    
class DiagramType2:
    __implements__ = IDiagramType
    name = 'Type2'

class NoDataSource: pass
class DataSource1:
    __implements__ = IDataSource
    name = 'Source1'
    
class DataSource2:
    __implements__ = IDataSource
    name = 'Source2'

class NoConverter: pass
class Converter1:
    __implements__ = IInputConverter
    name = 'Converter1'
    def registration(self):
        return {}

class Converter2:
    __implements__ = IInputConverter
    name = 'Converter2'
    def registration(self):
        return {NoDiagramType: [DataSource1]}

class Converter3:
    __implements__ = IInputConverter
    name = 'Converter3'
    def registration(self):
        return {DiagramType1: [NoDataSource]}

class Converter4:
    __implements__ = IDefaultInputConverter
    name = 'Converter4'
    def registration(self):
        return {DiagramType1: [DataSource1]}

class Converter5:
    __implements__ = IInputConverter
    name = 'Converter5'
    def registration(self):
        return {DiagramType1: [DataSource1, DataSource2],
                DiagramType2: [DataSource2]}

class Converter6:
    __implements__ = IDefaultInputConverter
    name = 'Converter6'
    def registration(self):
        return {DiagramType1: [DataSource2]}

class Converter7:
    __implements__ = IInputConverter
    name = 'Converter7'
    def registration(self):
        return {DiagramType2: [DataSource2]}



class ICRegistryTests(unittest.TestCase):
    """Tests for the ICRegistry.
    """

    def assertNone(self, expr, msg=None):
        """Fail the test unless the expression is None."""
        if expr is not None: raise self.failureException, msg

    def test_1singleton(self):
        """Test if ICRegistry is a singleton."""
        from icreg import ICRegistry
        a = ICRegistry
        b = ICRegistry

        self.assertEqual(str(a.__class__),
                         'icreg.ICRegistry',
                         'classtest')
        self.assertRaises(AttributeError,
                          ICRegistry) # failing of instanciation
        self.assertEqual(a, b, 'a==b')
        a.testAttributeWhichRegistryNeverHas = 'test'
        self.assertEqual(a.testAttributeWhichRegistryNeverHas,
                         b.testAttributeWhichRegistryNeverHas,
                         'a.attrib==b.attrib')

    def test_2register_get_Type(self):
        """Test _registerType(type) and getTypes()."""

        n = NoDiagramType
        a = DiagramType1
        b = DiagramType1
        c = DiagramType2
        
        self.assertRaises(RuntimeError, ICRegistry._registerType, n)
        self.failUnless(ICRegistry._registerType(a),
                        'register type1')
        self.failIf(ICRegistry._registerType(a),
                    'register type1 second time')
        self.failIf(ICRegistry._registerType(b),
                    'register type1 third time')
        
        self.assertEqual([a.name], ICRegistry.getTypes())
        self.failUnless(ICRegistry._registerType(c),
                        'register type2')
        self.assertEqual([a.name, c.name], ICRegistry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1

        self.failIf(ICRegistry._clear(), '1st clear')
        self.assertEqual([], ICRegistry.getTypes(), '1st get')
        self.failUnless(ICRegistry._registerType(a), 'register type1')
        self.assertEqual([a.name], ICRegistry.getTypes(), '2nd get')
        self.failIf(ICRegistry._clear(), '2nd clear')
        self.assertEqual([], ICRegistry.getTypes(), '3rd get')

    def test_4_registerSource(self):
        """Test of _registerSource(...) and getSource(...)"""
        d = DiagramType1
        e = DiagramType2
        n = NoDataSource
        a = DataSource1
        b = DataSource1
        c = DataSource2
        
        ICRegistry._clear()

        self.assertEqual([], ICRegistry.getSources(d.name),
                         'get from empty Registry')
        self.failUnless(ICRegistry._registerType(d))
        self.assertEqual([], ICRegistry.getSources(d.name),
                         'get from empty Type')
        self.assertEqual([], ICRegistry.getSources(e.name),
                         'get from not registered Type')
        self.assertRaises(RuntimeError, ICRegistry._registerSource, d, n)
        self.failUnless(ICRegistry._registerSource(d, a), 'reg one')
        self.failIf(ICRegistry._registerSource(d, a), 'reg one 2nd time')
        self.failIf(ICRegistry._registerSource(d, b), 'reg one 3rd time')
        self.assertEqual([a.name], ICRegistry.getSources(d.name), 'get one')
        self.assertEqual([a.name], ICRegistry.getSources(d.name), 'get one2')
        self.assertEqual([],
                         ICRegistry.getSources(e.name),
                         'get not registered Type 2')
        self.failUnless(ICRegistry._registerSource(e, a), 'reg two two')
        self.failIf(ICRegistry._registerSource(e, a), 'reg two two 2nd')
        self.failIf(ICRegistry._registerSource(e, b), 'reg two two 3rd')
        self.assertEqual([a.name], ICRegistry.getSources(e.name), 'get two')
        self.assertEqual([a.name], ICRegistry.getSources(e.name), 'get two2')
        self.assertEqual([a.name], ICRegistry.getSources(d.name), 'get one3')
        self.failUnless(ICRegistry._registerSource(d, c), 'reg tri')
        self.failIf(ICRegistry._registerSource(d, c), 'reg tri 2nd')
        res1 = ICRegistry.getSources(d.name)
        res1.sort()
        self.assertEqual([a.name, c.name], res1, 'get tri %s' % res1)
        res2 = ICRegistry.getSources(d.name)
        res2.sort()
        self.assertEqual([a.name, c.name], res2, 'get tri2')
        self.assertEqual([a.name], ICRegistry.getSources(e.name), 'get two3')


    def test_5_registerConverter(self):
        """Test _registerConverter(...) and getConverters(...)."""
        d1 = DiagramType1
        d2 = DiagramType2
        s1 = DataSource1
        s2 = DataSource2
        n  = NoConverter
        a  = Converter1
        b  = Converter1
        c  = Converter2

        ICRegistry._clear()
        self.assertEqual([],
                         ICRegistry.getConverters(d1.name, s1.name),
                         'get empty reg')
        self.failUnless(ICRegistry._registerType(d1))
        self.assertEqual([],
                         ICRegistry.getConverters(d1.name, s1.name),
                         'get empty type')
        self.failUnless(ICRegistry._registerSource(d1,s1))
        self.assertEqual([],
                         ICRegistry.getConverters(d1.name, s1.name),
                         'get empty src')
        self.assertRaises(RuntimeError, ICRegistry._registerConverter, d2,s1,n)
        self.failUnless(ICRegistry._registerConverter(d2,s1,a), 'reg 21a')
        self.failIf(ICRegistry._registerConverter(d2,s1,a), 'reg 21a 2nd')
        self.failIf(ICRegistry._registerConverter(d2,s1,b), 'reg 21a 3rd')
        self.assertEqual([],
                         ICRegistry.getConverters(d1.name,s1.name),
                         'get empty src2')
        self.assertEqual([a.name],
                         ICRegistry.getConverters(d2.name,s1.name),
                         'get 21')
        self.assertEqual([a.name],
                         ICRegistry.getConverters(d2.name,s1.name),
                         'get 21 2nd')
        self.failUnless(ICRegistry._registerConverter(d2,s2,a), 'reg 22a')
        self.failIf(ICRegistry._registerConverter(d2,s2,a), 'reg 22a 2nd')
        self.failUnless(ICRegistry._registerConverter(d1,s2,a), 'reg 12a')
        self.assertEqual([a.name],
                         ICRegistry.getConverters(d2.name,s1.name),
                         'get 21 3rd')
        self.failUnless(ICRegistry._registerConverter(d2,s1,c), 'reg 21c')
        self.assertEqual([a.name, c.name],
                         ICRegistry.getConverters(d2.name,s1.name),
                         'get 21 4th')
        self.assertEqual([a.name],
                         ICRegistry.getConverters(d1.name,s2.name),
                         'get 12')
        self.assertEqual([],
                         ICRegistry.getConverters(d1.name,s1.name),
                         'get 11')


    def test_6register(self):
        """Test register(converter)."""
        d1 = DiagramType1.name
        d2 = DiagramType2.name
        s1 = DataSource1.name
        s2 = DataSource2.name
        n  = NoConverter
        c1 = Converter1
        c2 = Converter2
        c3 = Converter3
        c4 = Converter4
        c42= Converter4
        c5 = Converter5
            
        ICRegistry._clear()
        self.assertRaises(RuntimeError, ICRegistry.register, n)
        self.failUnless(ICRegistry.register(c1), 'reg c1')
        self.assertEqual([], ICRegistry.getTypes(), 'get c1')
        self.assertRaises(RuntimeError, ICRegistry.register, c2)
        self.assertRaises(RuntimeError, ICRegistry.register, c3)
        self.failUnless(ICRegistry.register(c4), 'reg c4')
        self.assertEqual([d1], ICRegistry.getTypes(), 'get c4 typ')
        self.assertEqual([s1], ICRegistry.getSources(d1), 'get c4 src')
        self.assertEqual([c4.name],
                         ICRegistry.getConverters(d1,s1),
                         'get c4 conv')
        self.assertRaises(RuntimeError, ICRegistry.register, c4)
        self.assertRaises(RuntimeError, ICRegistry.register, c42)
        self.assertEqual([d1], ICRegistry.getTypes(), 'get c4 typ 3rd')
        self.assertEqual([s1], ICRegistry.getSources(d1), 'get c4 src 3rd')
        self.assertEqual([c4.name],
                         ICRegistry.getConverters(d1,s1),
                         'get c4 conv 3rd')
        self.failUnless(ICRegistry.register(c5), 'reg c5')
        self.assertEqual([d1,d2], ICRegistry.getTypes(), 'get c5 typ')
        res = ICRegistry.getSources(d1)
        res.sort()
        self.assertEqual([s1,s2], res, 'get c5 d1 src')
        self.assertEqual([s2], ICRegistry.getSources(d2), 'get c5 d2 src')
        self.assertEqual([c4.name, c5.name],
                         ICRegistry.getConverters(d1,s1),
                         'get c5 d1s1 conv')
        self.assertEqual([c5.name],
                         ICRegistry.getConverters(d1,s2),
                         'get c5 d1s2 conv')

    def test_7getConverter(self):
        """Test getConverter(converterName)."""
        c1 = Converter1
        c4 = Converter4

        ICRegistry._clear()
        self.assertNone(ICRegistry.getConverter(c1.name), 'get c1 1st')
        self.assertNone(ICRegistry.getConverter(c4.name), 'get c4 1st')
        self.failUnless(ICRegistry.register(c1))
        self.assertNone(ICRegistry.getConverter(c1.name), 'get c1 2nd')
        self.assertNone(ICRegistry.getConverter(c4.name), 'get c4 2nd')
        self.failUnless(ICRegistry.register(c4))
        self.assertNone(ICRegistry.getConverter(c1.name), 'get c1 3rd')
        self.assertEqual(c4().__class__,
                         ICRegistry.getConverter(c4.name).__class__,
                         'get c4 3rd (%s != %s)' %(c4().__class__,
                                                   ICRegistry.getConverter(
            c4.name).__class__
                                                   ))
        

    def test_8getDefaultConverterName(self):
        """Test getDefaultConverterName()."""

        c1 = Converter1 # empty converter
        c4 = Converter4 # default converter
        c5 = Converter5
        c6 = Converter6 # second default
        c7 = Converter7
        

        ICRegistry._clear()

        self.assertNone(ICRegistry.getDefaultConverterName(), 'empty reg')
        self.failUnless(ICRegistry.register(c1))
        self.assertNone(ICRegistry.getDefaultConverterName(), 'empty reg 2nd')
        self.failUnless(ICRegistry.register(c5))
        self.assertNone(ICRegistry.getDefaultConverterName(), 'no default')
        self.failUnless(ICRegistry.register(c4))
        self.assertEqual(c4.name,
                         ICRegistry.getDefaultConverterName(),
                         'default')
        self.assertRaises(RuntimeError, ICRegistry.register, c6) #second default
        self.assertNone(ICRegistry.getConverter(c6.name), 'get 2nd default')
        self.assertEqual(c4.name,
                         ICRegistry.getDefaultConverterName(),
                         'default 2')
        self.failUnless(ICRegistry.register(c7))
        self.assertEqual(c4.name,
                         ICRegistry.getDefaultConverterName(),
                         'default 3')

        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ICRegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
