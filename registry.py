################################################################################
## 
## SVGrafZ_Registry
## Version: $Id: registry.py,v 1.3 2003/04/11 14:06:54 mac Exp $
##
################################################################################

from interfaces import IDiagramType, IDiagramKind

class Registry:
    """Registry for DiagramTypes and -Kinds.
    """

    def __init__(self):
        self._diagrams = {}

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
                     
        if type.name in self._diagrams.keys():
            return 0
        
        self._diagrams[type.name] = {}
        return 1

    def getTypes(self):
        """Get the registered DiagramTypes."""
        return self._diagrams.keys()


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

        if type.name not in self._diagrams.keys():
            self.registerType(type)

        if kind.name in self._diagrams[type.name].keys():
            return 0
        
        self._diagrams[type.name][kind.name] = kind
        return 1


    def getKinds(self, typeName):
        """Get the DiagramKinds registered for a DiagrammType.

        typeName ... Name of the DiagramType

        returns dictionary kindName:kindObj
                None when typeName is not a registered Type
        """
        return self._diagrams.get(typeName, None)


    def getAllKindNames(self):
        """Get all Names of DiagramKinds.

        returns unique list of strings of DiagramKind-Names ordered alphabetically
                emptyList, when no kinds registered 
        """
        res = []

        for typ in self._diagrams.values():
            for kind in typ.keys():
                if kind not in res:
                    res.append(kind)
        res.sort()
        return res


Registry = Registry() # make it Singleton-like
