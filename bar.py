################################################################################
## 
## SVGrafZ: BarGraphs
##
## $Id: bar.py,v 1.12 2003/06/04 08:56:17 mac Exp $
################################################################################

from interfaces import IDiagramKind
from base import BaseGraph
from dtypes import *
from config import SVGrafZ_default_Color


class SimpleBarGraph(BaseGraph):
    """Simple BarGraph with multiple DataRows,
                       without negative values,
                       x-axis always starting at zero."""

    __implements__ = IDiagramKind

    name = 'simple bar diagram'

    def registration():
        """See IDiagramKind.registration()."""
        return [BarGraphs]
    registration = staticmethod(registration)

    def __init__(self,
                 data=None,
                 width=0,
                 height=0,
                 gridlines=0,
                 legend=None,
                 colnames=None,
                 title=None,
                 stylesheet=None,
                 errortext=None):
        "See IDiagramKind.__init__"
        self.data       = data
        self.width      = width
        self.height     = height
        self.legend     = legend
        self.colnames   = colnames
        self.gridlines  = gridlines
        self.title      = title
        self.stylesheet = stylesheet
        self.errortext  = errortext
        
        self.result     = ''

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
        self.result  = self.svgHeader()
        if self.errortext:
            self.result += self.printError()
        else:
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
                self.result += self.drawTitle()
            except RuntimeError:
                import sys
                self.errortext = str(sys.exc_info()[1])
                self.result = self.svgHeader() + self.printError()

            self.result += self.svgFooter()
        return self.result


    def drawBars(self):
        "Draw the Bars of the graph."
        yBarFull = (self.gridbasey - self.gridboundy) / len(self.distValsY())
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
                res += '<rect class="dataset%s" x="%s" y="%s" height="%s" width="%s" fill="%s"/>\n'\
                       % (i,
                          self.gridbasex,
                          self.gridbasey-(onPos*yBarFull)-ySpace-(i+1)*yHeight,
                          yHeight,
                          self.xScale * item[0],
                          SVGrafZ_default_Color)

        if self.colnames:
            for i in range(len(self.colnames)):
                colname = self.colnames[i]
                res += '<text x="5" y="%s" style="text-anchor:start;">%s</text>\n'\
                   % (self.gridbasey - i * yBarFull - 3.5 * ySpace,
                      self.confLT(colname))
        else:
            for colname, onPos in pos.items():
                res += '<text x="5" y="%s" style="text-anchor:start;">%s</text>\n'\
                       % (self.gridbasey - onPos * yBarFull - 3.5 * ySpace,
                          self.confLT(colname))

        return res + '</g>\n'

