################################################################################
## 
## SVGrafZ
## Version: $Id: svgrafz.py,v 1.3 2003/04/14 14:14:02 mac Exp $
##
################################################################################


from OFS.SimpleItem import SimpleItem
from registry import Registry
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

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

    security=ClassSecurityInfo()


    def __init__(self, id, title, graph):
        self.id    = id
        self.title = title
        self.namegraph = graph


    security.declarePublic('html')
    def html(self):
        print '<object type="image/svg+xml" width="600" height="300" data="self">Ihr Browser unterstützt keine SVG-Grafiken. Schade.</object>'

        

InitializeClass(SVGrafZProduct)


def addForm(dispatcher):
    """Returns an HTML form."""
    
    return """<html>
    <head><title>Add SVGrafZ</title></head>
    <body>   
    <form action="addFunction">
    id: <input type="text" name="id"/><br/>
    title: <input type="text" name="title"/><br/>
    diagramKind:<select height="1" name="graph">
    <option>SimpleBarGraph</option>
    </select>
    <br/>
    <input type="submit"/>
    </form>
    </body>
    </html>"""


def addFunction(dispatcher, id, title, graph):
    """Create a new graph and add it to myself."""
    g = SVGrafZProduct(id, title, graph)
    dispatcher.Destination()._setObject(id, g)
