################################################################################
## 
## SVGrafZ: Base
## Version: $Id: base.py,v 1.9 2003/06/03 15:03:13 mac Exp $
##
################################################################################

from math import log10,floor,ceil
from types import *
from config import SVGrafZ_default_Color

class BaseGraph:
    """BaseClass for graphs providing base functionallity for all graphs."""

    __computed_results__ = None
    specialAttribName    = None


    def setSpecialAttrib(self, value):
        """Set the value of the special attribute."""
        self.specialAttrib = value


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


    def distValsX(self):
        return self._computeMinMax('distValsX')

    def distValsY(self):
        return self._computeMinMax('distValsY')

    def numgraphs(self):
        return len(self.data)


    def _compRoundedValMax(self, val):
        """Compute a rounded maximum value."""
        if val == 0:
            return 0
        valBase = 10 ** (int(log10(abs(val))))
        return valBase * ceil((float(val) / valBase)+1)

    def _compRoundedValMin(self, val):
        """Compute a rounded minimum value."""
        if val == 0:
            return 0
        valBase = 10 ** (int(log10(abs(val))))
        return valBase * floor((float(val) / valBase)-1)

    def _getDistinctValues(self, list):
        """Make a list having only distinct values."""
        return dict([(x, 1) for x in list]).keys()


    def _computeMinMax(self, key):
        if self.__computed_results__:
            return self.__computed_results__[key]

        self._testFormatOfData()
        self.__computed_results__ = {}
        cr = self.__computed_results__

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
            cr['realMaxX']  = None
            cr['maxX']      = None
            cr['realMinX']  = None
            cr['minX']      = None
        else:
            cr['realMaxX']  = max(allX)
            cr['maxX']      = self._compRoundedValMax(cr['realMaxX'])
            cr['realMinX']  = min(allX)
            cr['minX']      = self._compRoundedValMin(cr['realMinX'])


        if stringInY:
            cr['realMaxY']  = None
            cr['maxY']      = None
            cr['realMinY']  = None
            cr['minY']      = None
        else:
            cr['realMaxY']  = max(allY)
            cr['maxY']      = self._compRoundedValMax(cr['realMaxY'])
            cr['realMinY']  = min(allY)
            cr['minY']      = self._compRoundedValMin(cr['realMinY'])

        cr['distValsX'] = self._getDistinctValues(allX)
        cr['distValsY'] = self._getDistinctValues(allY)
        return cr[key]

    def _change_computed_result(self, key, value):
        """Set the value of key in __computed_results__ after computation.

        Use with caution!
        """
        self._computeMinMax(key)
        self.__computed_results__[key] = value


    def _testFormatOfData(self):
        if self.data is None:
            raise RuntimeError, 'No Data. (Data is None)'
        if type(self.data) != ListType:
            raise RuntimeError, 'Data is not a list. Maybe wrong converter.'
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
        if not self.gridlines:
            return ''
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
                      self.confLT(xval))
            res += '\n'
        return res + '</g>\n'

    def drawYGrindLines(self):
        """Draw gridlines in parallel to the x-axis."""
        if not self.gridlines:
            return ''
        res  = '<g id="yGrid">\n'
        grid = self._computeGridLines(self.minY(), self.maxY(), self.gridlines)
        for yval in grid:
            res +='<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
                self.gridbasex,
                self.gridboundx,
                self.gridbasey - yval * self.yScale,
                self.gridbasey - yval * self.yScale)
            res += '<text x="3" y="%s" style="text-anchor: start;">%s</text>'\
                   % (self.gridbasey - yval * self.yScale + 5,
                      self.confLT(yval))
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
        if not self.title:
            return ''
        res = '<g id="title">\n'
        res += '<text x="%s" y="%s" style="text-anchor: middle;">%s</text>'\
                   % ((self.gridboundx + self.gridbasex) /2,
                      self.gridboundy + 1,
                      self.confLT(self.title))
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
            res += """<line class="%s" x1="%s" x2="%s" y1="%s" y2="%s" stroke-width="10" stroke-linecap="round" stroke="%s" />
            """ % ('dataset%s' % (i),
                   self.width - 5,
                   self.width - 15,
                   self.gridboundy + 26 + (15 * i),
                   self.gridboundy + 26 + (15 * i),
                   SVGrafZ_default_Color
                   )
            res += """<text x="%s" y="%s" style="text-anchor:end;">%s</text>"""\
                   % (self.width - 25,
                      self.gridboundy + 30 + (15 * i),
                      self.confLT(self.legend[i]),
                      )
        return res+"\n</g>"

    def printError(self):
        """Print the textual description of an error."""
        res = '''
<g id="SVGrafZicon" transform="translate(%s,%s) scale(2)">
  <g id="icondata">
    <rect style="fill: #ef2715;" x="1" y="11.332" height="2.7" width="8.76864"/>
    <rect style="fill: #ef2715;" x="1" y="4.8" height="2.7" width="4.38432"/>
    <rect style="fill: #131ef4;" x="1" y="8.6328" height="2.7" width="11.6915"/>
    <rect style="fill: #131ef4;" x="1" y="2" height="2.7" width="8.76864"/>
  </g>
  <g id="iconxyaxis" style="stroke:#000000; stroke-opacity:1;">
    <line x1="0" x2="15.68" y1="16" y2="16"/>
    <line x1="1" x2="1" y1="17" y2="0.5328"/>
  </g>
</g>''' % (self.width / 2,
           (self.gridbasey - self.gridboundy) / 4)
           
        res += '<text x="%s" y="%s" font-size="12pt" text-anchor="middle" fill="red">%s</text>' % (
            self.width / 2,
            (self.gridbasey - self.gridboundy) / 2,
            'Error: ' + self.errortext)
        return res


    

        
    def confLT(self, text):
        """Convert the littler than symbols ('<') to &lt;."""
        return str(text).replace('<', '&lt;')

    
