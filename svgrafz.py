################################################################################
## 
## SVGrafZ
## Version: $Id: svgrafz.py,v 1.2 2003/04/11 14:06:54 mac Exp $
##
################################################################################


from OFS.SimpleItem import SimpleItem
from registry import Registry

def getDiagramKinds():
    """Get the names of the DiagramKinds."""
    return Registry.getAllKindNames()

class SVGrafZProduct(SimpleItem):
    """ProductClass of SVGrafZ."""

    meta_type = 'SVGrafZ'

    _properties=({'id':'title',       'type': 'string', 'mode': 'w'},
                 {'id':'dataSource',  'type': 'string', 'mode': 'w'},
                 {'id':'diagramKind', 'type': 'selection', 'mode': 'w', 'select_variable' : 'getDiagramKinds'}
                 
                 )

    
    def __init__(self, id, title):
        self.id    = id
        self.title = title
