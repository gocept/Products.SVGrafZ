################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.2 2003/04/14 14:14:02 mac Exp $
##
################################################################################

from registry import Registry
from types import BarGraphs
from bar import SimpleBarGraph
from svgrafz import SVGrafZProduct


from svgrafz import SVGrafZProduct, addForm, addFunction

def initialize(registrar):
    # register diagramkinds
    Registry.registerKind(BarGraphs, SimpleBarGraph)
    
    registrar.registerClass(
        SVGrafZProduct, 
        constructors = (addForm, addFunction),
        icon = 'www/icon.gif'
        )
