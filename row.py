################################################################################
## 
## SVGrafZ: RowGraphs
##
## $Id: row.py,v 1.4 2003/10/07 08:55:18 mac Exp $
################################################################################

from interfaces import IDiagramKind
from base import DataOnYAxis
from dtypes import *
from config import SVGrafZ_default_Color

class RowDiagram(DataOnYAxis):
    """Abstract superclass for concrete RowDiagram classes."""

    def registration():
        """See IDiagramKind.registration()."""
        return [RowGraphs]
    registration = staticmethod(registration)

    def description():
        """see interfaces.IDiagamKind.description
        """
        return DataOnYAxis.description() + [
            'Continuous data displayed as colored columns.',]
    description = staticmethod(description)    


class Simple(RowDiagram):
    """Simple RowGraph with multiple DataRows,
                       without negative values,
                       y-axis always starting at zero,
                       labels on x-axis written vertically,
    """

    __implements__ = IDiagramKind

    name = 'simple column diagram'


    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.computeYScale,
                self.drawYGridLines,] + \
                BaseGraph.getDrawingActions(self)

    def description():
        """see interfaces.IDiagamKind.description
        """
        return RowDiagram.description() + [
            "Multiple Datasets possible.",
            "Y-axis is always starting at zero, so no negative values are \
            possible.",
            "The labels on the x-axis are written vertically.",
            ]

    description = staticmethod(description)

    def drawGraph(self):
        "Draw the Bars of the graph."
        distX  = self.distValsX()
        lenDistX = len(distX)
        xBarFull = (self.gridboundx - self.gridbasex) / lenDistX
        xWidth   = 0.75  * xBarFull / self.numgraphs()
        xSpace   = 0.125 * xBarFull
        res      = '<g id="data">\n'

        distX.sort()
        for i in range(self.numgraphs()):
            dataset = dict(self.data[i])
            for j in range(lenDistX):
                try:
                    val = float(dataset[distX[j]])
                    res += '<rect class="dataset%s" x="%s" y="%s" height="%s" width="%s" fill="%s"/>\n'\
                       % (i,
                          self.gridbasex + j * xBarFull + xSpace + i * xWidth,
                          self.gridbasey - val * self.yScale,
                          val * self.yScale,
                          xWidth,
                          SVGrafZ_default_Color)
                except KeyError:
                    pass

        res += self.xAxis_verticalLabels(distX,
                                         self.gridbasex + xBarFull / 2,
                                         xBarFull)

        return res + '</g>\n'

class FillingGaps(Simple):
    """ColumnGraph like Simple but with integer values on x-axis,
                                        filling gaps im x-axis (making data coninoous)."""

    __implements__ = IDiagramKind

    name = 'column diagram with int(x)'
    
    def description():
        """see interfaces.IDiagamKind.description
        """
        return Simple.description() + [
            'Values on x-axis are must be integer.',
            'Missing values on x-Axis are added as zero-values (making data coninoous)'
            'Values on y-axis are shown as integers.'
            ]
    description = staticmethod(description)


    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.makeXValsContinoous,
                self.computeYScale,
                self.drawYGridLinesInt,] + \
                RowDiagram.getDrawingActions(self)

    def makeXValsContinoous(self):
        "Fill gaps in x-Values so that they are continoous."
        distX = range(self.realMinX(), self.realMaxX())
        self._change_computed_result('distValsX', distX)
        return ''


    def specialAttribHook(self):
        """Handling of the specialAttrib.

        Test datatype of specialAttrib & change data influenced by
          specialAttrib.

        Return: void
        On error: raise RuntimeError
        """
        self._change_computed_result('realMinY', 0.0)
        self._change_computed_result('minY',
                                     self._compRoundedValMax(0.0))
