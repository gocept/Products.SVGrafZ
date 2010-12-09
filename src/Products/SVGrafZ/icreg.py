# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: Registry of InputConverters
##
## $Id$
################################################################################

from Products.SVGrafZ.interfaces import \
     IDiagramType, IInputConverter, IDefaultInputConverter, IDataSource

class ICRegistry:
    """Registry for InputConverters.
    """

    ### public methods:

    def register(self, converter):
        """Register a converter.

        converter ... class implementing IInputConverter
        return True
        exception RuntimeError, if Interfaces not implemented
        """

        if not IInputConverter.isImplementedByInstancesOf(converter):
            raise RuntimeError, 'SVGrafZ-Error: InputConverter "%s" is not implementing IInputConverter.' % repr(converter)

        converterInstance = converter()
        capabilities = converterInstance.registration()

        if capabilities: # only if converter is able to do something
            if IDefaultInputConverter.isImplementedBy(converterInstance):
                if not self._defaultConverterName is None:
                    raise RuntimeError, \
                          'SVGrafZ-Error: DoubleRegistration of DefaultInputConverter "%s"' % converter.name
                else:
                    self._defaultConverterName = converter.name

            if self._inputConverters.get(converter.name):
                raise RuntimeError, 'SVGrafZ-Error: DoubleRegistration of InputConverter "%s"' % converter.name
            
            self._inputConverters[converter.name] = converterInstance

            for diagramType in capabilities.keys():
                for dataSource in capabilities[diagramType]:
                    self._registerConverter(diagramType, dataSource, converter)

        return True

         
    def getConverter(self, converterName):
        """Get the instance of a converter.

        converterName ... string: converter.name
        return instance of a class implementing IInputConverter and having
                  class.name = converter.name
               or None if converter not registered
        """
        return self._inputConverters.get(converterName)



    def getDefaultConverterName(self):
        """Get the Name of the default Converter.

        The default one is the first one which got registered.
        It should be a so called NoneConverter which does no conversion.
        
        None is returned when no Converter was registered so far.
        """
        return self._defaultConverterName
    

    def getConverters(self, diagramTypeName, dataSourceName):
        """Get the names of registered converters for given diagramType&source.

        diagramTypeName ... string: diagramType.name
        dataSourceName  ... string: dataSource.name

        return list of registered ConverterNames
               emptyList, if none registered or diagramType or dataSource not
                 registered.
        """
        return self._diagramTypes.get(diagramTypeName,{}).get(dataSourceName,[])


    def getSources(self, diagramTypeName):
        """Get the Names of the registered DataSources for a diagramType.

        diagramTypeName ... string: diagramType.name

        returns list of registered DataSourceNames
                emptyList, if none registered or diagramType not registered.
        """
        return self._diagramTypes.get(diagramTypeName, {}).keys()


    def getTypes(self):
        """Get the registered DiagramTypeNames."""
        return self._diagramTypes.keys()



    ### private methods:
                
    def __init__(self):
        self._diagramTypes = {}    # name: {source1name: [converternames...]...}
        self._inputConverters = {} # name: instance
        self._defaultConverterName = None # string

    _clear = __init__

    def _registerType(self, type):
        """Register a DiagrammType.

        type ... class implementing IDiagramType

        returns 1 on success
                0 type already in registry
        exception RuntimeError, if type not implementing Interface
        """
        if not IDiagramType.isImplementedByInstancesOf(type):
            raise RuntimeError, 'SVGrafZ-Error: DiagramType "%s" is not implementing IDiagramType.' % repr(type)
                     
        if type.name in self._diagramTypes.keys():
            return 0
        
        self._diagramTypes[type.name] = {}
        return 1


    def _registerSource(self, diagramType, dataSource):
        """Register a dataSource for a diagramType.

        If DiagramType is not yet registered, it gets registered within here.

        diagramType ... class implementing IDiagramType
        dataSource  ... class implementing IDataSource

        returns 1 on success
                0 if dataSource already registered for diagramType
        exception RuntimeError, if Interfaces not implemented
        """
        if not IDataSource.isImplementedByInstancesOf(dataSource):
            raise RuntimeError, 'SVGrafZ-Error: DataSource "%s" is not implementing IDataSource.' % repr(dataSource)

        self._registerType(diagramType)
                             
        if dataSource.name in self._diagramTypes[diagramType.name].keys():
            return 0
        
        self._diagramTypes[diagramType.name][dataSource.name] = []
        return 1



    def _registerConverter(self, diagramType, dataSource, converter):
        """Register a converter to a diagramType and a dataSource.

        diagramType ... class implementing IDiagramType
        dataSource  ... class implementing IDataSource
        converter   ... instance of a class implementing IInputConverter

        returns 1 on success
                0 if converter already registered for diagramType and dataSource
        exception RuntimeError, if Interfaces not implemented
        """
        if not IInputConverter.isImplementedByInstancesOf(converter):
            raise RuntimeError, 'SVGrafZ-Error: InputConverter "%s" is not implementing IInputConverter.' % repr(converter)

        self._registerSource(diagramType, dataSource)
                     
        if converter.name in \
               self._diagramTypes[diagramType.name][dataSource.name]:
            return 0
        
        self._diagramTypes[diagramType.name][dataSource.name].append(
            converter.name)
        return 1


ICRegistry = ICRegistry() # make it Singleton-like
