################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.1 2003/04/09 12:25:55 mac Exp $
##
################################################################################

from registry import Registry
from types import BarGraphs
from bar import SimpleBarGraph

Registry.registerKind(BarGraphs, SimpleBarGraph)

