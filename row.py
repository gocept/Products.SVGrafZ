################################################################################
## 
## SVGrafZ: RowGraphs
##
## $Id: row.py,v 1.1 2003/06/04 08:56:17 mac Exp $
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


class Simple(RowDiagram):
    """Simple RowGraph with multiple DataRows,
                       without negative values,
                       y-axis always starting at zero,
                       labels on x-axis written vertically,
    """

    __implements__ = IDiagramKind

    name = 'simple column diagram'


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
