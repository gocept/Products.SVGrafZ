################################################################################
## 
## SVGrafZ: BarGraphs
##
## $Id: bar.py,v 1.13 2003/06/04 10:20:55 mac Exp $
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
                self.result += self.drawGraph()
                self.result += self.drawXYAxis()
                self.result += self.drawLegend()
                self.result += self.drawTitle()
            except RuntimeError:
                import sys
                self.errortext = str(sys.exc_info()[1])
                self.result = self.svgHeader() + self.printError()

            self.result += self.svgFooter()
        return self.result


    def drawGraph(self):
        "Draw the Bars of the graph."
        distY    = self.distValsY()
        lenDistY = len(distY)
        yBarFull = (self.gridbasey - self.gridboundy) / lenDistY
        yHeight  = 0.75  * yBarFull / self.numgraphs()
        ySpace   = 0.125 * yBarFull
        res      = '<g id="data">\n'

        distY.sort()
        for i in range(self.numgraphs()):
            dataset     = dict([[x[1],x[0]] for x in self.data[i]]) # switch x,y
            for j in range(lenDistY):
                try:
                    val = float(dataset[distY[j]])
                    res += '<rect class="dataset%s" x="%s" y="%s" height="%s" width="%s" fill="%s"/>\n'\
                       % (i,
                          self.gridbasex,
                          self.gridbasey-(j*yBarFull)-ySpace-(i+1)*yHeight,
                          yHeight,
                          self.xScale * val,
                          SVGrafZ_default_Color)
                except KeyError:
                    pass
                   

        res += self.yAxis_horizontalLabels(distY, 
                                           self.gridboundy+yBarFull/2-ySpace,
                                           yBarFull)
        return res + '</g>\n'

