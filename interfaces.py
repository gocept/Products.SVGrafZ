################################################################################
## 
## SVGrafZ: Interfaces
## Version: $Id: interfaces.py,v 1.1 2003/04/09 12:25:55 mac Exp $
##
################################################################################

from Interface import Interface

class IDiagramType(Interface):
    """Interface for DiagramTypes."""

    def name():
        """Get the Name of the DiagramType."""


class IDiagramKind(Interface):
    """Interface for DiagramKinds."""

    def name():
        """Get the Name of the DiagramKind."""
