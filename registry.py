################################################################################
## 
## SVGrafZ_DiagramRegistry
##
## Version: $Id: registry.py,v 1.7 2003/06/13 10:23:57 mac Exp $
################################################################################

from interfaces import IDiagramType, IDiagramKind, IDefaultDiagramKind

class Registry:
    """Registry for DiagramTypes and -Kinds.
    """

    ## public methods:

    def register(self, diagramKind):
        """Let a diagramKind register itself.

        diagramKind ... class implementing IDiagramKind
        returns True
        exception RuntimeError if not implementing necessary Interfaces.
        """
        if not IDiagramKind.isImplementedByInstancesOf(diagramKind):
            raise RuntimeError, 'Not implementing IDiagramKind.'


        capabilities = diagramKind.registration()

        if capabilities: # only if diagramKind has diagramTypes
            if IDefaultDiagramKind.isImplementedByInstancesOf(diagramKind):
                if self._defaultDiagramKindName is None:
                    self._defaultDiagramKindName = diagramKind.name
                else:
                    raise RuntimeError,  'DoubleRegistration of Default %s' % (
                    diagramKind.name)

            if self._diagramKinds.get(diagramKind.name):
                raise RuntimeError, 'DoubleRegistration of %s' % (
                    diagramKind.name)
            
            self._diagramKinds[diagramKind.name] = diagramKind

            for diagramType in capabilities:
                self._registerKind(diagramType, diagramKind)
        return True


    def getKindNames(self, typeName):
        """Get the DiagramKinds registered for a DiagrammType.

        typeName ... Name of the DiagramType

        returns dictionary kindName:kindObj
                None when typeName is not a registered Type
        """
        return self._diagramTypes.get(typeName, None)


    def getKind(self, name):
        """Get the ClassObject of a DiagramKind.

        name ... Name of the DiagramKind
        exception RuntimeError, if name not registered
        """

        if name not in self._diagramKinds:
            raise RuntimeError, 'DiagramKind %s does not exist.' % (name)

        return self._diagramKinds[name]

    def getAllKindNames(self):
        """Get all Names of DiagramKinds.

        returns unique list of strings of DiagramKind-Names ordered alphabetically
                emptyList, when no kinds registered 
        """
        res = []

        for typ in self._diagramTypes.values():
            for kind in typ:
                if kind not in res:
                    res.append(kind)
        res.sort()
        return res

    def getDefaultKindName(self):
        """Get the Name of the default DiagramKind.

        The default one is the first one which got registered.
        None is returned when no DiagramKind was registered so far."""

        return self._defaultDiagramKindName

    def getTypes(self):
        """Get the registered DiagramTypes."""
        return self._diagramTypes.keys()


    ## private methods:
    
    def __init__(self):
        self._diagramTypes = {}
        self._diagramKinds = {}
        self._defaultDiagramKindName = None

    _clear = __init__

    def _registerType(self, type):
        """Register a DiagrammType.

        type ... class implementing IDiagramType

        returns 1 on success
                0 type already in registry
        exception RuntimeError, if type not implementing Interface
        """
        if not IDiagramType.isImplementedByInstancesOf(type):
            raise RuntimeError, 'Not implementing IDiagramType.'
                     
        if type.name in self._diagramTypes.keys():
            return 0
        
        self._diagramTypes[type.name] = []
        return 1


    def _registerKind(self, type, kind):
        """Register a DiagramKind for a DiagramType.

        If DiagramType is not yet registered, it gets registered within here.

        type ... class implementing IDiagramType
        kind ... class implementing IDiagramKind

        returns 1 on success
                0 if kind already in registry
        exception RuntimeError, if not implementing Interface
        """

        if not IDiagramKind.isImplementedByInstancesOf(kind):
            raise RuntimeError, 'Not implementing IDiagramKind.'

        self._registerType(type)
        
        if kind.name in self._diagramTypes[type.name]:
            return 0
        
        self._diagramTypes[type.name].append(kind.name)
        return 1

Registry = Registry() # make it Singleton-like
