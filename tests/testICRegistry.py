################################################################################
## 
## SVGrafZ: Test of ICRegistry
## $Id: testICRegistry.py,v 1.1 2003/05/28 07:15:01 mac Exp $
##
################################################################################

import config
import unittest
from icreg import ICRegistry
from interfaces import IDiagramType, IInputConverter, IDataSource

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
    def registration():
        return {}

class Converter2:
    __implements__ = IInputConverter
    name = 'Converter2'
    def registration():
        return {NoDiagramType: [DataSource1]}

class Converter3:
    __implements__ = IInputConverter
    name = 'Converter3'
    def registration():
        return {DiagramType1: [NoDataSource]}

class Converter4:
    __implements__ = IInputConverter
    name = 'Converter4'
    def registration():
        return {DiagramType1: [DataSource1]}




class ICRegistryTests(unittest.TestCase):
    """Tests for the ICRegistry.
    """

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
        """Test _registerType(type) and getType()."""

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
        
        self.assertEqual(['Type1'], ICRegistry.getTypes())
        self.failUnless(ICRegistry._registerType(c),
                        'register type2')
        self.assertEqual(['Type1', 'Type2'], ICRegistry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1

        self.failIf(ICRegistry._clear(), '1st clear')
        self.failIf(ICRegistry.getTypes(), '1st get')
        self.failUnless(ICRegistry._registerType(a),
                        'register type1')
        self.failUnless(ICRegistry.getTypes(), '2nd get')
        self.failIf(ICRegistry._clear(), '2nd clear')
        self.failIf(ICRegistry.getTypes(), '3rd get')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ICRegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
