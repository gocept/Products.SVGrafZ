################################################################################
## 
## SVGrafZ: BarGraphs
## Version: $Id: dtypes.py,v 1.1 2003/04/15 08:58:26 mac Exp $
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


