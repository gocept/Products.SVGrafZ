################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.5 2003/05/30 08:19:04 mac Exp $
##
################################################################################

from registry import Registry
from icreg import ICRegistry
from dtypes import BarGraphs, RowGraphs
from bar import SimpleBarGraph,SimpleBarGraph2
from svgrafz import SVGrafZProduct
from ic import NoneConverter, RowGraph_ZSQLMethod

from svgrafz import SVGrafZProduct, manage_addDiagramForm, \
     manage_addDiagramFunction, manage_defaultPossible

def initialize(registrar):
    # register diagramkinds
    Registry.register(SimpleBarGraph)
    Registry.register(SimpleBarGraph2)

    # register InputConverters
    ICRegistry.register(NoneConverter)
    ICRegistry.register(RowGraph_ZSQLMethod)
    
    registrar.registerClass(
        SVGrafZProduct, 
        constructors = (manage_addDiagramForm,
                        manage_addDiagramFunction,
                        manage_defaultPossible,
                        ),
        icon = 'www/icon.gif'
        )
    registrar.registerHelp()
