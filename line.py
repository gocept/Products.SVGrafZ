################################################################################
## 
## SVGrafZ: LineGraphs
##
## $Id: line.py,v 1.3 2003/06/04 08:56:17 mac Exp $
################################################################################

from interfaces import IDiagramKind
from base import DataOnYAxis
from dtypes import *
from config import SVGrafZ_default_Color

class LineDiagram(DataOnYAxis):
    """Abstract superclass for concrete LineDiagram classes."""

    def registration():
        """See IDiagramKind.registration()."""
        return [LineGraphs]
    registration = staticmethod(registration)
    

class Simple(LineDiagram):
    """Simple LineGraph with multiple DataRows,
                        without negative values,
                        y-axis always starting at zero,
                        no double values on x-axis allowed. (if so, random value
                          gets choosen).
                        missing x-values are left out.
                        values on x-axis are taken as discrete.
    """

    __implements__ = IDiagramKind
    name = 'simple line diagram'


    def drawGraph(self):
        "Draw the Lines of the graph and name the columns."
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

        res += self.xAxis_verticalLabels(distX, base, xWidth)

        return res + '</g>\n'



class Mirrored(LineDiagram):
    """LineGraph with multiple DataRows,
                      without negative values, smallest y-value is always 0,
                      y-axis is mirrored, so the biggest values are on bottom,
                      no double values on x-axis allowed. (if so, random value
                          gets choosen),
                      missing x-values are left out,
                      values on x-axis are taken as discrete,
                      specialAttribute for defining minimun units on y-axis,
    """

    __implements__ = IDiagramKind
    name              = 'mirrored line diagram'
    specialAttribName = 'minimum of shown units on y-axis'

    def specialAttribHook(self):
        "Do the checking of specialAttrib things."
        if self.specialAttrib is None:
            return
        try:
            self.specialAttrib = float(self.specialAttrib)
            self._change_computed_result('realMaxY',
                                         max(self.realMaxY(),
                                             self.specialAttrib))
            self._change_computed_result('maxY',
                                         max(self.maxY(),
                                             self._compRoundedValMax(
                self.specialAttrib)))
            
            
        except (ValueError, TypeError):
            self.errortext = "'%s' must be a number." % self.specialAttribName
            
    def drawGraph(self):
        "Draw the Lines of the graph and name the columns."
        distX    = self.distValsX()
        lenDistX = len(distX)
        xWidth   = float(self.gridboundx - self.gridbasex) / (lenDistX + 1)
        base     = self.gridbasex + xWidth
        res      = '<g id="data">\n'
        start    = 1
        
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
                                   self.gridboundy + (val * self.yScale))
                start = 0
            res += '"/>\n'
            start = 1

        res += self.xAxis_verticalLabels(distX, base, xWidth)
        
        return res + '</g>\n'


    def drawYGrindLines(self):
        """Draw gridlines in parallel to the x-axis."""
        if not self.gridlines:
            return ''
        res  = '<g id="yGrid">\n'
        grid = self._computeGridLines(self.minY(), self.maxY(), self.gridlines)
        for yval in grid:
            y = self.gridboundy + yval * self.yScale
            res +='<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
                self.gridbasex,
                self.gridboundx,
                y,
                y)
            res += '<text x="3" y="%s" style="text-anchor: start;">%s</text>'\
                   % (self.gridboundy + yval * self.yScale + 5,
                      self.confLT(yval))
            res += '\n'
        return res + '</g>\n'
