################################################################################
## 
## SVGrafZ: SimpleBarGraph
## Version: $Id: bar.py,v 1.7 2003/04/17 13:24:32 mac Exp $
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

    def __init__(self,
                 data=None,
                 width=0,
                 height=0,
                 gridlines=0,
                 legend=None,
                 colnames=None,
                 title=None,
                 stylesheet=None):
        "see IDiagramKind.__init__"
        self.data     = data
        self.width    = width
        self.height   = height
        self.legend   = legend
        self.colnames = colnames
        self.gridlines= gridlines
        self.title    = title
        self.stylesheet=stylesheet

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
        if self.result:
            return self.result
        else:
            self.result  = self.svgHeader()
            try:
                if self.maxX() is None:
                    raise RuntimeError, 'All values on x-axis must be numbers!'
                difX = float(self.maxX() - self.minX())
                if difX:
                    self.xScale = float((self.gridboundx-self.gridbasex)/difX)
                else:
                    self.xScale = 1.0
                    
                self.result += self.drawXGrindLines()
                self.result += self.drawBars()
                self.result += self.drawXYAxis()
                self.result += self.drawLegend()
            except RuntimeError:
                import sys
                ev,en,et = sys.exc_info()
                self.title=str(en)
            
            self.result += self.drawTitle()
            self.result += self.svgFooter()
            return self.result


    def drawBars(self):
        "Draw the Bars of the graph."
        yBarFull = (self.gridbasey - self.gridboundy) / self.countDistY()
        yHeight  = 0.75  * yBarFull / self.numgraphs()
        ySpace   = 0.125 * yBarFull
        res      = '<g id="data">\n'
        pos      = {} # storage for positions of y-values, so same y-values get
        #               same position
        
        for i in range(self.numgraphs()):
            dataset = self.data[i]
            for j in range(len(dataset)):
                item = dataset[j]
                if pos.has_key(item[1]):
                    onPos = pos[item[1]]
                else:
                    onPos = len(pos)
                    pos[item[1]] = onPos
                res += '<rect class="dataset%s" x="%s" y="%s" height="%s" width="%s"/>\n'\
                       % (i,
                          self.gridbasex,
                          self.gridbasey-(onPos*yBarFull)-ySpace-(i+1)*yHeight,
                          yHeight,
                          self.xScale * item[0])

        if self.colnames:
            for i in range(len(self.colnames)):
                colname = self.colnames[i]
                res += '<text x="5" y="%s" style="text-anchor:start;">%s</text>\n'\
                   % (self.gridbasey - i * yBarFull - 3.5 * ySpace,
                      colname)
        else:
            for colname, onPos in pos.items():
                res += '<text x="5" y="%s" style="text-anchor:start;">%s</text>\n'\
                       % (self.gridbasey - onPos * yBarFull - 3.5 * ySpace,
                          colname)

        return res + '</g>\n'
            
                
        
class SimpleBarGraph2(BaseGraph):
    """Simple BarGraph testclass."""

    __implements__ = IDiagramKind

    name = 'Zweifaches Balkendiagramm'

    def __init__(self,
                 data=None,
                 width=0,
                 height=0,
                 gridlines=0,
                 legend=None,
                 colnames=None,
                 title=None,
                 stylesheet=None):
        "see IDiagramKind.__init__"
        self.data     = data
        self.width    = width
        self.height   = height
        self.legend   = legend
        self.colnames = colnames
        self.gridlines= gridlines
        self.title    = title
        self.stylesheet=stylesheet


    def compute(self):
        """Compute the Diagram."""
        return self.svgHeader() + \
               '<text x="1" y="30">leer</text>' + \
               self.svgFooter()

