################################################################################
## 
## SVGrafZ: SimpleBarGraph
## Version: $Id: bar.py,v 1.1 2003/04/09 12:25:55 mac Exp $
##
################################################################################

from interfaces import IDiagramKind

class SimpleBarGraph:
    """Simple BarGraph with multiple DataRows possible."""

    __implements__ = IDiagramKind

    def name(self):
        ""+IDiagramKind.name.__doc__
        return 'Einfaches Balkendiagramm'

SimpleBarGraph = SimpleBarGraph() # make it singleton-like
