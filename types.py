################################################################################
## 
## SVGrafZ: BarGraphs
## Version: $Id: types.py,v 1.1 2003/04/09 12:25:55 mac Exp $
##
################################################################################

from interfaces import IDiagramType

class BarGraphs:
    """DiagramType of bar graphs."""

    __implements__ = IDiagramType

    def name(self):
        ""+IDiagramType.name.__doc__
        return 'Balkendiagramme'

BarGraphs = BarGraphs() # make it singleton like

class RowGraphs:
    """DiagramType of row graphs."""

    __implements__ = IDiagramType

    def name(self):
        ""+IDiagramType.name.__doc__
        return 'Säulendiagramme'


RowGraphs = RowGraphs() # make it singleton like
