################################################################################
## 
## SVGrafZ: Base
## Version: $Id: base.py,v 1.5 2003/05/23 12:43:18 mac Exp $
##
################################################################################

from math import log10,floor,ceil
from types import *

class BaseGraph:
    """BaseClass for graphs providing base functionallity for all graphs."""

    __computed_results__ = None

    def hasLegend(self):
        "Has the graph a legend?"
        return (type(self.legend) == type([])) and self.legend


    def svgHeader(self):
        res = u"""<?xml version="1.0" encoding="UTF-8" ?>\n"""
        if self.stylesheet:
            res += u"""<?xml-stylesheet href="%s" type="text/css"?>\n""" % (
                self.stylesheet)
        return res + """<svg xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink"
             width="%i"
             height="%i">
             """ % (self.width, self.height)
        

    def svgFooter(self):
        return "</svg>"


    def minX(self):
        return self._computeMinMax('minX')

    def realMinX(self):
        return self._computeMinMax('realMinX')

    def minY(self):
        return self._computeMinMax('minY')

    def realMinY(self):
        return self._computeMinMax('realMinY')
        

    def maxX(self):
        return self._computeMinMax('maxX')

    def realMaxX(self):
        return self._computeMinMax('realMaxX')

    def maxY(self):
        return self._computeMinMax('maxY')

    def realMaxY(self):
        return self._computeMinMax('realMaxY')


    def countDistX(self):
        return self._computeMinMax('countDistX')

    def countDistY(self):
        return self._computeMinMax('countDistY')

    def numgraphs(self):
        return len(self.data)


    def _computeMinMax(self, key):
        if self.__computed_results__:
            return self.__computed_results__[key]

        self._testFormatOfData()
        self.__computed_results__ = {}
        cr = self.__computed_results__
        def compRoundedValMax(val):
            if val == 0:
                return 0
            valBase = 10 ** (int(log10(abs(val))))
            return valBase * ceil((float(val) / valBase)+1)

        def compRoundedValMin(val):
            if val == 0:
                return 0
            valBase = 10 ** (int(log10(abs(val))))
            return valBase * floor((float(val) / valBase)-1)

        def countDistinctValues(list):
            vals = 0
            while (len(list)):
                cval = list.pop()
                vals += 1
                try:
                    while 1:
                        list.pop(list.index(cval))
                except ValueError:
                    pass
            return vals

        allX = []
        allY = []
        stringInX = stringInY = 0
        for dataset in self.data:
            for value in dataset:
                try:
                    valx = float(value[0])
                except ValueError:
                    valx = value[0]
                    stringInX = 1
                try:
                    valy = float(value[1])
                except ValueError:
                    valy = value[1]
                    stringInY = 1

                allX.append(valx)
                allY.append(valy)

        if stringInX:
            cr['realMaxX'] = None
            cr['maxX']     = None
            cr['realMinX'] = None
            cr['minX']     = None
        else:
            cr['realMaxX'] = max(allX)
            cr['maxX']     = compRoundedValMax(cr['realMaxX'])
            cr['realMinX'] = min(allX)
            cr['minX']     = compRoundedValMin(cr['realMinX'])

        if stringInY:
            cr['realMaxY'] = None
            cr['maxY']     = None
            cr['realMinY'] = None
            cr['minY']     = None
        else:
            cr['realMaxY'] = max(allY)
            cr['maxY']     = compRoundedValMax(cr['realMaxY'])
            cr['realMinY'] = min(allY)
            cr['minY']     = compRoundedValMin(cr['realMinY'])

        cr['countDistX'] = countDistinctValues(allX)
        cr['countDistY'] = countDistinctValues(allY)
        
        return cr[key]


    def _testFormatOfData(self):
        if self.data is None:
            raise RuntimeError, 'No Data. (Data is None)'
        if type(self.data) != ListType:
            raise RuntimeError, 'Data is not a list.'
        if len(self.data) == 0:
            raise RuntimeError, 'Data is empty.'
        i = 0
        for dataset in self.data:
            i = i + 1
            if type(dataset) != ListType:
                raise RuntimeError, 'Dataset %i is no List.' % i
            if len(dataset) == 0:
                raise RuntimeError, 'Dataset %i is empty.' % i

            j = 0
            for dataItem in dataset:
                j = j + 1
                if type(dataItem) != ListType:
                    raise RuntimeError, 'DataItem %i in Dataset %i is no List.'\
                          % (i,j)
                if len(dataItem) != 2:
                    raise RuntimeError,\
                          'DataItem %i in Dataset %i: More than 2 dimensions.'\
                          % (j,i)
                k = 0
                for dim in dataItem:
                    k = k + 1
                    if type(dim) not in [IntType,
                                         LongType,
                                         FloatType,
                                         StringType,
                                         UnicodeType,
                                         ]:
                        raise RuntimeError,\
                              'Dimension %i of DataItem %i in Dataset %i: \
                              Not allowed Type of %s.' \
                              % (k,j,i,type(dim))
        return 1        


    def _computeGridLines(self, minVal, maxVal, lines):
        ystep = (maxVal - minVal) / float(abs(lines) + 1)
        return [ minVal + (y * ystep) for y in range(1, abs(lines)+1) ]


    def drawXGrindLines(self):
        """Draw gridlines in parallel to the y-axis."""
        res  = '<g id="xGrid">\n'
        grid = self._computeGridLines(self.minX(), self.maxX(), self.gridlines)
        for xval in grid:
            res +='<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
                self.gridbasex + xval * self.xScale,
                self.gridbasex + xval * self.xScale,
                self.gridbasey,
                self.gridboundy)
            res += '<text x="%s" y="%s" style="text-anchor: middle;">%s</text>'\
                   % (self.gridbasex + xval * self.xScale,
                      self.gridbasey + 15,
                      xval)
            res += '\n'
        return res + '</g>\n'

    def drawXYAxis(self):
        """Draw the x- and y-axis."""
        res  = '<g id="xyaxis" style="stroke:#000000; stroke-opacity:1;">\n'
        res += '<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
            self.gridbasex - 10,
            self.gridboundx,
            self.gridbasey,
            self.gridbasey)
        res += '<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
            self.gridbasex,
            self.gridbasex,
            self.gridbasey + 10,
            self.gridboundy)
        return res + '</g>\n'

    def drawTitle(self):
        res = '<g id="title">\n'
        res += '<text x="%s" y="%s" style="text-anchor: middle;">%s</text>'\
                   % ((self.gridboundx + self.gridbasex) /2,
                      self.gridboundy,
                      self.title)
        return res + '\n</g>\n'

    def drawLegend(self):
        """Draw the Legend."""
        if not self.legend:
            return ''
        res = """<g id="legend">
        <text x="%s" y="%s" style="%s">Legende</text>
        """ % ((self.gridboundx + self.width) / 2,
               self.gridboundy + 10,
               'text-anchor: middle; font-weight: bold;')
        for i in range(len(self.legend)):
            res += """<line class="%s" x1="%s" x2="%s" y1="%s" y2="%s" stroke-width="10" stroke-linecap="round"/>
            """ % ('dataset%s' % (i),
                   self.width - 5,
                   self.width - 15,
                   self.gridboundy + 26 + (15 * i),
                   self.gridboundy + 26 + (15 * i),
                   )
            res += """<text x="%s" y="%s" style="text-anchor:end;">%s</text>"""\
                   % (self.width - 25,
                      self.gridboundy + 30 + (15 * i),
                      self.legend[i],
                      )
        return res+"\n</g>"
