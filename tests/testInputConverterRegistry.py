################################################################################
## 
## SVGrafZ: Test of InputConverterRegistry
## $Id: testInputConverterRegistry.py,v 1.1 2003/05/28 07:06:00 mac Exp $
##
################################################################################

import config
import unittest
from inputconverterreg import InputConverterRegistry
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




class InputConverterRegistryTests(unittest.TestCase):
    """Tests for the InputConverterRegistry.
    """

    def test_1singleton(self):
        """Test if InputConverterRegistry is a singleton."""
        from inputconverterreg import InputConverterRegistry
        a = InputConverterRegistry
        b = InputConverterRegistry

        self.assertEqual(str(a.__class__),
                         'inputconverterreg.InputConverterRegistry',
                         'classtest')
        self.assertRaises(AttributeError,
                          InputConverterRegistry) # failing of instanciation
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
        
        self.assertRaises(RuntimeError, InputConverterRegistry._registerType, n)
        self.failUnless(InputConverterRegistry._registerType(a),
                        'register type1')
        self.failIf(InputConverterRegistry._registerType(a),
                    'register type1 second time')
        self.failIf(InputConverterRegistry._registerType(b),
                    'register type1 third time')
        
        self.assertEqual(['Type1'], InputConverterRegistry.getTypes())
        self.failUnless(InputConverterRegistry._registerType(c),
                        'register type2')
        self.assertEqual(['Type1', 'Type2'], InputConverterRegistry.getTypes())
        
    def test_3_clear(self):
        """Test of _clear()."""
        a = DiagramType1

        self.failIf(InputConverterRegistry._clear(), '1st clear')
        self.failIf(InputConverterRegistry.getTypes(), '1st get')
        self.failUnless(InputConverterRegistry._registerType(a),
                        'register type1')
        self.failUnless(InputConverterRegistry.getTypes(), '2nd get')
        self.failIf(InputConverterRegistry._clear(), '2nd clear')
        self.failIf(InputConverterRegistry.getTypes(), '3rd get')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InputConverterRegistryTests,
                                     sortUsing  = cmp))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
