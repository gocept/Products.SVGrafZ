################################################################################
## 
## SVGrafZ_Registry
## Version: $Id: registry.py,v 1.4 2003/04/16 14:14:38 mac Exp $
##
################################################################################

from interfaces import IDiagramType, IDiagramKind

class Registry:
    """Registry for DiagramTypes and -Kinds.
    """

    def __init__(self):
        self._diagramTypes = {}
        self._diagramKinds = {}
        self._defaultDiagramKindName = None

    _clear = __init__

    def registerType(self, type):
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

    def getTypes(self):
        """Get the registered DiagramTypes."""
        return self._diagramTypes.keys()


    def registerKind(self, type, kind):
        """Register a DiagramKind for a DiagramType.

        If DiagramType is not yet registered, it gets registered within here.

        type ... class implementing IDiagramType
        kind ... class implementing IDiagramKind

        returns 1 on success
                0 if kind already in registry
        exception RuntimeError, if not implementing Interface
        """

        if not IDiagramType.isImplementedByInstancesOf(type):
            raise RuntimeError, 'Not implementing IDiagramType.'
        if not IDiagramKind.isImplementedByInstancesOf(kind):
            raise RuntimeError, 'Not implementing IDiagramKind.'

        if type.name not in self._diagramTypes.keys():
            self.registerType(type)

        if kind.name in self._diagramTypes[type.name]:
            return 0
        
        self._diagramTypes[type.name].append(kind.name)
        self._diagramKinds[kind.name] = kind
        if self._defaultDiagramKindName is None:
            self._defaultDiagramKindName = kind.name
        return 1


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
        
        

Registry = Registry() # make it Singleton-like
