################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.4 2003/04/17 14:15:43 mac Exp $
##
################################################################################

from registry import Registry
from dtypes import BarGraphs, RowGraphs
from bar import SimpleBarGraph,SimpleBarGraph2
from svgrafz import SVGrafZProduct


from svgrafz import SVGrafZProduct, manage_addDiagramForm, \
     manage_addDiagramFunction, manage_defaultPossible

def initialize(registrar):
    # register diagramkinds
    Registry.registerKind(BarGraphs, SimpleBarGraph)
    Registry.registerKind(BarGraphs, SimpleBarGraph2)
    Registry.registerKind(RowGraphs, SimpleBarGraph2)
    
    registrar.registerClass(
        SVGrafZProduct, 
        constructors = (manage_addDiagramForm,
                        manage_addDiagramFunction,
                        manage_defaultPossible,
                        ),
        icon = 'www/icon.gif'
        )
    registrar.registerHelp()
