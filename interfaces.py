################################################################################
## 
## SVGrafZ: Interfaces
## Version: $Id: interfaces.py,v 1.2 2003/04/09 13:28:04 mac Exp $
##
################################################################################

from Interface import Interface,Attribute

class IDiagramType(Interface):
    """Interface for DiagramTypes."""

    name = Attribute("Get the Name of the DiagramType.")
        



class IDiagramKind(Interface):
    """Interface for DiagramKinds."""

    name = Attribute ("Get the Name of the DiagramKind.")



class IDiagramKindDefault(IDiagramKind):
    """MarkerInterface for DefaultDiagramKinds."""


    
