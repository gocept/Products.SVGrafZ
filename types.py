################################################################################
## 
## SVGrafZ: BarGraphs
## Version: $Id: types.py,v 1.2 2003/04/09 13:28:04 mac Exp $
##
################################################################################

from interfaces import IDiagramType

class BarGraphs:
    """DiagramType of bar graphs."""

    __implements__ = IDiagramType

    name = 'Balkendiagramme'



class RowGraphs:
    """DiagramType of row graphs."""

    __implements__ = IDiagramType

    name = 'Säulendiagramme'


