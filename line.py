# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: LineGraphs
##
## $Id: line.py,v 1.14 2003/10/27 10:14:06 mac Exp $
################################################################################

from interfaces import IDiagramKind
from base import DataOnYAxis
from dtypes import *
from config import SVGrafZ_default_Color

class LineDiagram(DataOnYAxis):
    """Abstract superclass for concrete LineDiagram classes."""

    pointsAsCrosses = 0
    mirrored = 0
    labels = 'vertical'

    def registration():
        """See IDiagramKind.registration()."""
        return [LineGraphs]
    registration = staticmethod(registration)

    def description():
        """see interfaces.IDiagamKind.description
        """
        return DataOnYAxis.description() + [
            'Continuous data displayed as colored lines.',
            "Multiple Datasets possible.",
            "No double values on x-axis inside one dataset allowed. (random \
            value gets choosen in this case).",
            ]
    description = staticmethod(description)


    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.computeYScale,
                self.drawYGridLines,] + \
                DataOnYAxis.getDrawingActions(self)


    def _drawCross(self, x, y, i, color):
        """Draw a cross instead of a point.

           x,y ... absolute position of point
           i ... dataset-number
           color ... color of the cross
        """
        return '''
        <line class="dataset%s" x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" />
        <line class="dataset%s" x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" />
        ''' % (i, x-3, y-3, x+3, y+3, color,
               i, x+3, y-3, x-3, y+3, color,
               )

    def drawGraph(self):
        """Draw the Lines of the graph and name the columns."""
        
        distX    = self.distValsX()
        lenDistX = len(distX)
        xWidth   = float(self.gridboundx - self.gridbasex) / lenDistX
        base     = self.gridbasex + xWidth / 2
        res      = '<g id="data">\n'
        
        distX.sort()
        for i in range(self.numgraphs()):
            dataset = dict(self.data[i])
            points  = []
            for j in range(lenDistX):
                if len(dataset) == 0:
                    break
                try:
                    val = float(dataset[distX[j]])
                    x   = base + j * xWidth
                    if self.mirrored:
                        y = self.gridboundy + (val * self.yScale)
                    else:
                        y = self.gridbasey - (val * self.yScale)
                    points.append([x,y])
                    if self.pointsAsCrosses:
                        res += self._drawCross(x,y,i,SVGrafZ_default_Color)
                except KeyError:
                    pass

            if len(points) > 1:
                start = 1
                for point in points:
                    if start:
                        res += '<path class="dataset%s" stroke-width="2" fill="none" stroke="%s" d="M%s,%s' % (
                            i,
                            SVGrafZ_default_Color,
                            point[0],
                            point[1])
                        start = 0
                    else:
                        res += ' L%s,%s' % (point[0], point[1])
                res += '"/>\n'

        if self.labels == 'vertical':
            res += self.xAxis_verticalLabels(distX, base, xWidth)
        else: # 'diagonal'
            res += self.xAxis_diagonalLabels(distX, base, xWidth, 'lines')
        return res + '</g>\n'


class Simple(LineDiagram):
    """Simple LineGraph with multiple DataRows,
                        without negative values,
                        y-axis always starting at zero,
                        no double values on x-axis allowed. (if so, random value
                          gets choosen).
                        missing x-values are left out.
                        values on x-axis are taken as discrete.
    """
    __implements__  = IDiagramKind
    name            = 'simple line diagram'
    pointsAsCrosses = 0
    mirrored        = 0
    labels          = 'vertical'

    def description():
        """see interfaces.IDiagamKind.description
        """
        return LineDiagram.description() + [
            "The labels on the x-axis written vertically.",
            ]
    description = staticmethod(description)


class PointsAsCrosses(LineDiagram):
    "Abstract Diagramm with a drawing helper method to draw points as little crosses."

    pointsAsCrosses = 1
    mirrored = 0
    labels = 'vertical'
    
    def description():
        """see interfaces.IDiagamKind.description
        """
        return LineDiagram.description() + [
            "Points are drawn as little x on diagram.",]
    description = staticmethod(description)


class Mirrored(PointsAsCrosses):
    """LineGraph with multiple DataRows,
                      without negative values, smallest y-value is always 0,
                      y-axis is mirrored, so the biggest values are on bottom,
                      no double values on x-axis allowed. (if so, random value
                          gets choosen),
                      values on x-axis are taken as discrete,
                      specialAttribute for defining minimun units on y-axis,
                      points are drawn as little x on diagram
                      labels on x-axis diagonally written
    """

    __implements__ = IDiagramKind
    name              = 'mirrored line diagram'
    specialAttribName = 'minimum of shown units on y-axis'
    pointsAsCrosses   = 1
    mirrored          = 1
    labels            = 'diagonal'

    def description():
        """see interfaces.IDiagamKind.description
        """
        return PointsAsCrosses.description() + [
            "Y-axis is mirrored, so the biggest values are at bottom.",
            "Y-axis is always starting at zero, so no negative values are \
            possible.",
            "The labels on the x-axis written diagonally.",
            ]
    description = staticmethod(description)

    def specialAttribHook(self):
        "Do the checking of specialAttrib things."
        self._change_computed_result('realMinY', 0.0)
        self._change_computed_result('minY', self._compRoundedValMin(0.0))
        
        self.gridbasey  = self.height * 0.88 # more room for labels on y-axis

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
            raise RuntimeError, "'%s' must be a number." % (self.specialAttribName)

            
    def drawYGridLines(self):
        """Draw gridlines in parallel to the x-axis.

        Overwriting existing method because of mirrored y-axis.
        """
        if not self.gridlines:
            return ''
        if self.intcaption:
            rtype = int
        else:
            rtype = float
        grid = self._computeGridLines(self.minY(),
                                      self.maxY(),
                                      self.gridlines,
                                      rtype)
        res  = '<g id="yGrid">\n'
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




class SimpleCrossed(PointsAsCrosses):
    """LineGraph with multiple DataRows,
                      without negative values, smallest y-value is always 0,
                      no double values on x-axis allowed. (if so, random value
                          gets choosen),
                      missing x-values are left out,
                      values on x-axis are taken as discrete,
                      points are drawn as little x on diagram
                      labels on x-axis diagonally written
    """

    __implements__  = IDiagramKind
    name            = 'line diagram with crosses as points'
    pointsAsCrosses = 1
    mirrored        = 0
    labels          = 'vertical'

    def description():
        """see interfaces.IDiagamKind.description
        """
        return LineDiagram.description() + [
            "Y-axis is always starting at zero, so no negative values are \
            possible.",
            "The labels on the x-axis written vertically.",
            ]
    description = staticmethod(description)

    def specialAttribHook(self):
        "Do the checking of specialAttrib things."
        self._change_computed_result('realMinY', 0.0) # min of y is zero
        self._change_computed_result('minY', self._compRoundedValMin(0.0))
