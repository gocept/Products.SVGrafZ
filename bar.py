################################################################################
## 
## SVGrafZ: BarGraphs
##
## $Id: bar.py,v 1.19 2003/10/07 08:55:18 mac Exp $
################################################################################

from interfaces import IDiagramKind, IDefaultDiagramKind
from base import DataOnXAxis
from dtypes import *
from config import SVGrafZ_default_Color

class BarDiagram(DataOnXAxis):
    """Abstract superclass for concrete BarDiagram classes."""

    def registration():
        """See IDiagramKind.registration()."""
        return [BarGraphs]
    registration = staticmethod(registration)

    def description():
        "See interfaces.IDiagamKind.description."
        return DataOnXAxis.description() + [
            'Continuous data is shown as horizontal bars of different colors.']
    description = staticmethod(description)


class Simple(BarDiagram):
    """Simple BarGraph with multiple DataRows,
                       without negative values,
                       x-axis always starting at zero."""

    __implements__ = IDefaultDiagramKind

    name = 'simple bar diagram'

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


    def description():
        """see interfaces.IDiagamKind.description
        """
        return BarDiagram.description() + [
            'You can have multiple Datasets.',
            'X-axis is always starting at zero, so you cannot have negative continuous values.',]
    description = staticmethod(description)


    def specialAttribHook(self):
        """Handling of the specialAttrib.

        Test datatype of specialAttrib & change data influenced by
          specialAttrib.

        Return: void
        On error: raise RuntimeError
        """
        self._change_computed_result('realMinX', 0.0)
        self._change_computed_result('minX',
                                     self._compRoundedValMax(0.0))

    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.computeXScale,
                self.drawXGridLines] + \
                BarDiagram.getDrawingActions(self)


class IntX(Simple):
    """BarGraph like Simple but with x-axis values rounded to int."""

    __implements__ = IDiagramKind

    name = 'bar diagram with int(x)'
    
    def description():
        """see interfaces.IDiagamKind.description
        """
        return Simple.description() + [
            'Values on x-axis are shown as integers.'
            ]
    description = staticmethod(description)
    
    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.computeXScale,
                self.drawXGridLinesInt] + \
                BarDiagram.getDrawingActions(self)

