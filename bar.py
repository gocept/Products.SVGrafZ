################################################################################
## 
## SVGrafZ: SimpleBarGraph
## Version: $Id: bar.py,v 1.2 2003/04/09 13:28:04 mac Exp $
##
################################################################################

from interfaces import IDiagramKind

class SimpleBarGraph:
    """Simple BarGraph with multiple DataRows possible."""

    __implements__ = IDiagramKind

    name = 'Einfaches Balkendiagramm'

