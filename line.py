################################################################################
## 
## SVGrafZ: LineGraphs
##
## $Id: line.py,v 1.1 2003/06/03 12:41:32 mac Exp $
################################################################################

from interfaces import IDiagramKind
from base import BaseGraph
from dtypes import *
from config import SVGrafZ_default_Color

class SimpleLineGraph(BaseGraph):
    """Simple LineGraph with multiple DataRows,
                        without negative values,
                        y-axis always starting at zero,
                        no double values on x-axis allowed. (if so, random value
                          gets choosen).
                        missing x-values are left out.
                        values on x-axis are taken as discrete.
    """

    __implements__ = IDiagramKind

    name = 'Einfaches Liniendiagramm'

    def registration():
        """See IDiagramKind.registration()."""
        return [LineGraphs]
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
        
        self.result = self.svgHeader()
        if self.errortext:
            self.result += self.printError()
        else:
            try:
                if self.maxY() is None:
                    raise RuntimeError, 'All values on y-axis must be numbers!'
                difY = float(self.maxY() - self.minY())
                if difY:
                    self.yScale = float((self.gridbasey-self.gridboundy) / difY)
                else:
                    self.yScale = 1.0
                    
                self.result += self.drawYGrindLines()
                self.result += self.drawLines()
                self.result += self.drawXYAxis()
                self.result += self.drawLegend()
                self.result += self.drawTitle()
            except RuntimeError:
                import sys
                self.errortext = str(sys.exc_info()[1])
                self.result = self.svgHeader() + self.printError()

        self.result += self.svgFooter()
        return self.result


    def drawLines(self):
        "Draw the Lines of the graph."
        distX  = self.distValsX()
        lenDistX = len(distX)
        xWidth = float(self.gridboundx - self.gridbasex) / (lenDistX + 1)
        base   = self.gridbasex + xWidth
        res    = '<g id="data">\n'
        start  = 1
        
        distX.sort()
        for i in range(self.numgraphs()):
            dataset = dict(self.data[i])
            for j in range(lenDistX):
                try:
                    val = float(dataset[distX[j]])
                except KeyError:
                    if not start:
                        res +='"/>\n"'
                        start = 1
                if start:
                    res += '<path class="dataset%s" stroke-width="2" fill="none" stroke="%s" d="M' % (i, SVGrafZ_default_Color)
                else:
                    res += 'L'
                res += "%s,%s " % (base + j * xWidth,
                                   self.gridbasey - (val * self.yScale))
                start = 0
            res += '"/>\n'
            start = 1

        if self.colnames:
            colnamesCount = len(self.colnames)
            colnames      = self.colnames
        else:
            colnamesCount = lenDistX
            colnames      = distX

        
        for i in range(colnamesCount):
            colname = colnames[i]
            res +='''<defs>
            <path d="M %s %s V 15" id="colname%s"/>
            </defs>\n''' % (base + i * xWidth + 2,
                            self.height - 2,
                            i)
            res+='''<text>
            <textPath xlink:href="#colname%s">%s</textPath>
            </text>''' % (i, self.confLT(colname))

        return res + '</g>\n'
