# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: BarGraphs
##
## $Id: bar.py,v 1.22 2005/02/16 09:06:52 mac Exp $
################################################################################

from Products.SVGrafZ.interfaces import IDiagramKind, IDefaultDiagramKind
from Products.SVGrafZ.base import DataOnXAxis
from Products.SVGrafZ.dtypes import *
from Products.SVGrafZ import config

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

