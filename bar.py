################################################################################
## 
## SVGrafZ: SimpleBarGraph
## Version: $Id: bar.py,v 1.3 2003/04/10 13:58:50 mac Exp $
##
################################################################################

from interfaces import IDiagramKind
from base import BaseGraph

class SimpleBarGraph(BaseGraph):
    """Simple BarGraph with multiple DataRows,
                       without negative values,
                       y-axix starting always at zero."""

    __implements__ = IDiagramKind

    name = 'Einfaches Balkendiagramm'

    def __init__(self, data, width=600, height=300, gridlines=10, legend=None, colnames=None):
        "see IDiagramKind.__init__"
        self.data     = data
        self.width    = width
        self.height   = height
        self.legend   = legend
        self.colnames = colnames
        self.gridlines= gridlines

        self.result   = ''

##      Achtung: die Koordinaten 0,0 sind im SVG links oben!
##        gridbasey   unteres Ende in y-Richtung
##        gridboundy  oberes  Ende in y-Richtung
##        gridbasey groesser gridboundy!
##        gridbasex   unteres (linkes) Ende in x-Richtung
##        gridboundx  oberes (rechtes) Ende in x-Richtung
##        gridbasex kleiner gridboundx!

        self.gridbasey  = self.height * 0.9333
        self.gridboundy = self.height * 0.0333
        self.gridbasex  = self.width  * 0.0666
        if self.hasLegend():
            self.gridboundx = self.width * 0.8
        else:
            self.gridboundx = self.width * 0.98
        
        
    def compute(self):
        """Compute the Diagram."""
        self.result = self.svgHeader()
        self.result = self.result + svgRaster()

        
        
