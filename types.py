################################################################################
## 
## SVGrafZ: BarGraphs
## Version: $Id: types.py,v 1.3 2003/04/10 13:58:50 mac Exp $
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


