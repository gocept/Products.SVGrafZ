# -*- coding: latin-1 -*-
################################################################################
##
## SVGrafZ: BarGraphs
##
## $Id$
################################################################################

from Products.SVGrafZ.interfaces import IDiagramKind, IDefaultDiagramKind
from Products.SVGrafZ.base import DataOnXAxis
from Products.SVGrafZ.dtypes import *
from Products.SVGrafZ import config

class BarDiagram(DataOnXAxis):
    """Abstract superclass for concrete BarDiagram classes."""

    downwardsYAxis = False

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

    def __init__(self, *args, **kw):
        Reverse.__init__(self, *args, **kw)
        self.gridbasex  = 3 # No room left of diagram

    def drawGraph(self):
        "Draw the Bars of the graph."
        distY    = self.distValsY()
        lenDistY = len(distY)
        yBarFull = (self.gridbasey - self.gridboundy) / lenDistY
        yHeight  = 0.7  * yBarFull / self.numgraphs()
        ySpace   = 0.2 * yBarFull / self.numgraphs()
        if self.numgraphs() == 1:
            ySpace = 0
        res      = '<g id="data">\n'

        distY.sort()
        if bool(self.downwardsYAxis):
            distY.reverse()

        for i in range(self.numgraphs()):
            dataset     = dict([[x[1],x[0]] for x in self.data[i]]) # switch x,y
            for j in range(lenDistY):
                try:
                    val = float(dataset[distY[j]])
                    res += '<rect class="dataset%s" x="%s" y="%s" height="%s" width="%s" fill="%s"/>\n'\
                       % (i,
                          self.gridbasex,
                          self.gridbasey-(j*yBarFull)-(i+1)*(yHeight+ySpace),
                          yHeight-ySpace,
                          self.xScale * val,
                          config.SVGrafZ_default_Color)
##                    res += '<line x1="5" x2="600" y1="%s" y2="%s" />'%(self.gridbasey-(j*yBarFull),
##                                                                     self.gridbasey-(j*yBarFull)
##                                                                     )
                except KeyError:
                    pass

##        import pdb
##        pdb.set_trace()

        res += self.yAxis_horizontalLabels(distY,
                                           yBarFull/2,
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



class Reverse(Simple):
    """Simple BarGraph with multiple DataRows,
                       without negative values,
                       x-axis always starting at zero,
                       y-axis sorted from top to bottom."""

    __implements__ = IDiagramKind

    name = "simple bar diagram with downwards-sorted y axis"

    downwardsYAxis = True

    def description():
        """see interfaces.IDiagamKind.description
        """
        return Simple.description() + [
            'Y-axis is sorted from top to bottom.']
    description = staticmethod(description)
