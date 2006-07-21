# -*- coding: latin-1 -*-
################################################################################
## 
## SVGrafZ: Base
## Version: $Id$
##
################################################################################

# python imports
from math import log10, floor, ceil
from types import *
from string import split

# sibling imports
from Products.SVGrafZ import config

# set this var to 1 to use the dom generation (not complete yet)
usedom = 0
if usedom:
    from xml.dom.minidom import Document


class BaseGraph:
    """Abstract base class for all diagramKinds providing base functionallity.
    """

    __computed_results__ = None
    specialAttribName    = None


    def __init__(self,
                 data        = None,
                 legend      = None,
                 colnames    = None,
                 title       = None,
                 stylesheet  = None,
                 errortext   = None,
                 otherParams = {}):
        "See IDiagramKind.__init__"
        self.data       = data
        self.width      = otherParams.get('width', 0)
        self.height     = otherParams.get('height', 0)
        self.legend     = legend
        self.colnames   = colnames
        self.gridlines  = otherParams.get('gridlines')
        self.fillgaps   = otherParams.get('fillgaps')
        self.intcaption = otherParams.get('intcaption')
        self.title      = title
        self.stylesheet = stylesheet
        self.errortext  = errortext
        self.result     = ''

##      Achtung: die Koordinaten 0,0 sind im SVG links oben!
##        gridbasey   unteres Ende in y-Richtung
##        gridboundy  oberes  Ende in y-Richtung
##        gridbasey groesser gridboundy!
##        gridbasex   unteres (linkes) Ende in x-Richtung
##        gridboundx  oberes (rechtes) Ende in x-Richtung
##        gridbasex kleiner gridboundx!

        self.gridbasey  = self.height - 20
        self.gridboundy = 20
        self.gridbasex  = 40
        if self.hasLegend():
            self.gridboundx = self.width - 120
        else:
            self.gridboundx = self.width - 12


    def setSpecialAttrib(self, value):
        """Set the value of the special attribute."""
        self.specialAttrib = value


    def hasLegend(self):
        "Has the graph a legend?"
        return (type(self.legend) in (type([]), type({}))) and self.legend

    def getDom(self):
        self.xmldoc = Document()
        # XXX minidom kann keine customisierte xml-processing instruction
        # XXX also mit umlauten testen, ob 'encoding="UTF-8"' nötig
##        xml = self.xmldoc.createProcessingInstruction(
##            'xml',
##            'version="1.0" encoding="UTF-8"')
##        self.xmldoc.appendChild(xml)
        if self.stylesheet:
            style = self.xmldoc.createProcessingInstruction(
                'xml-stylesheet',
                'href="%s" type="text/css"' % self.stylesheet)
            self.xmldoc.appendChild(style)
        svg = self.xmldoc.appendChild(self.xmldoc.createElement("svg"))
        svg.setAttribute('xmlns', "http://www.w3.org/2000/svg")
        svg.setAttribute('xmlns:xlink', "http://www.w3.org/1999/xlink")
        svg.setAttribute('width', str(self.width))
        svg.setAttribute('height', str(self.height))


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

    def allX(self):
        return self._computeMinMax('allX')

    def allY(self):
        return self._computeMinMax('allY')


    def numgraphs(self):
        return len(self.data)


    def _compRoundedValMax(self, val):
        """Compute a rounded maximum value."""
        if val == 0:
            return 0
        valBase = 10 ** (int(log10(abs(val))))
        return valBase * ceil((float(val + valBase / 10.0) / valBase))

    def _compRoundedValMin(self, val):
        """Compute a rounded minimum value."""
        if val == 0:
            return 0
        valBase = 10 ** (int(log10(abs(val))))
        return valBase * floor((float(val) / valBase)-1)

    def _getDistinctValues(self, list):
        """Make a list having only distinct values."""
        if not len(list):
            return []
        if type(list[0]) == type(self): # objects in list
            tmp = list[:]
            res = []
            while (tmp):
                if not tmp[0] in tmp[1:]:
                    res.append(tmp[0])
                del tmp[0]
            return res
        else:
            return dict([(x, 1) for x in list]).keys()


    def _computeMinMax(self, key):
        if self.__computed_results__:
            return self.__computed_results__[key]

        self._testFormatOfData()
        self.__computed_results__ = {}
        cr = self.__computed_results__

        allX = []
        allY = []
        allXfloat = []
        allYfloat = []
        stringInX = stringInY = False
        for dataset in self.data:
            for value in dataset:
                allX.append(value[0])
                if not stringInX:
                    try:
                        allXfloat.append(float(value[0]))
                    except ValueError:
                        stringInX = True

                allY.append(value[1])
                if not stringInY:
                    try:
                        allYfloat.append(float(value[1]))
                    except ValueError:
                        stringInY = True

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
            if self.fillgaps:
                cr['distValsX'] = range(cr['realMinX'], cr['realMaxX'] + 1)
            allX = allXfloat

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
            if self.fillgaps:
                cr['distValsY'] = range(cr['realMinY'], cr['realMaxY'] + 1)
            allY = allYfloat

        cr['allX'] = allX
        cr['allY'] = allY
        if cr.get('distValsX') is None:
            cr['distValsX'] = self._getDistinctValues(allX)
        if cr.get('distValsY') is None:
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
            raise RuntimeError, config.SVGrafZ_empty_dataset
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
                                         InstanceType,
                                         ]:
                        raise RuntimeError,\
                              'Dimension %i of DataItem %i in Dataset %i: \
                              Not allowed Type of %s.' \
                              % (k,j,i,type(dim))
        return 1        


    def _computeGridLines(self, minVal, maxVal, lines, rtype):
        """Compute the variable values for the gridlines.

        minVal ... first grid value
        maxVal ... last grid value
        lines  ... number of lines in grid
        rtype  ... <type 'int'> or <type 'float'> for type of the result values
        """
        if (rtype == int) and ((maxVal - minVal) < lines):
            lines = maxVal - minVal
        ystep = (maxVal - minVal) / rtype(abs(lines) + 1)
        return [rtype(minVal + (y * ystep)) for y in range(1, abs(lines) + 1)]
    

    def drawXGridLines(self):
        """Draw gridlines in parallel to the y-axis."""
        if not self.gridlines:
            return ''
        if self.intcaption:
            rtype = int
        else:
            rtype = float
            
        grid = self._computeGridLines(self.minX(),
                                      self.maxX(),
                                      self.gridlines,
                                      rtype)
        res  = '<g id="xGrid">\n'
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


    def drawYGridLines(self):
        """Draw gridlines in parallel to the x-axis."""
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

    def drawYGridLinesDiscrete(self):
        """Draw gridlines in parallel to the x-axis label it with the discrete values."""
        if not self.gridlines:
            return ''
        if self.intcaption:
            rtype = int
        else:
            rtype = float

        distY = self.distValsY()
        distY.sort()
        grid = self._computeGridLines(self.minY(),
                                      self.maxY(),
                                      self.gridlines,
                                      rtype)
        res  = '<g id="yGrid">\n'
        for yval in grid:
            if yval == 0:
                text = ''
            else:
                text = distY[yval - 1]
            res +='<line x1="%s" x2="%s" y1="%s" y2="%s"/>\n' % (
                self.gridbasex,
                self.gridboundx,
                self.gridbasey - yval * self.yScale,
                self.gridbasey - yval * self.yScale)
            res += '<text x="3" y="%s" style="text-anchor: start;">%s</text>'\
                   % (self.gridbasey - yval * self.yScale + 5,
                      self.confLT(text))
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
                   % (self.width / 2,
                      self.gridboundy - 4,
                      self.confLT(self.title))
        return res + '\n</g>\n'

    def drawLegend(self):
        """Draw the Legend."""
        if not self.legend:
            return ''
        res = """<g id="legend">
        <text x="%s" y="%s" style="%s">%s</text>
        """ % ((self.gridboundx + self.width) / 2,
               self.gridboundy + 10,
               'text-anchor: middle; font-weight: bold;',
               config.SVGrafZ_legend_name)
        for i in range(len(self.legend)):
            res += """<line class="%s" x1="%s" x2="%s" y1="%s" y2="%s" stroke-width="10" stroke-linecap="round" stroke="%s" />
            """ % ('dataset%s' % (i),
                   self.width - 5,
                   self.width - 15,
                   self.gridboundy + 26 + (15 * i),
                   self.gridboundy + 26 + (15 * i),
                   config.SVGrafZ_default_Color
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

        step = 0
        print `self.errortext`
        err_txt = u"%s: %s" % (config.SVGrafZ_error_name, self.errortext)
        for errortext in split(self.confLT(err_txt), '\n'):
            res += '<text x="%s" y="%s" font-size="12pt" text-anchor="middle" fill="red">%s</text>' % (
                self.width / 2,
                (self.gridbasey - self.gridboundy) / 2 + step,
                errortext)
            step += 20
        return res

    def xAxis_verticalLabels(self, labels, firstWidth, xWidth):
        """Print the labels on x-axis vertically.

        labels     ... list of strings with labelnames, if self.colnames
                         exists, then it is taken instead
        firstWidth ... float points from self.gridbasex to first label
        xWidth     ... float points between labels
        """
        if self.colnames: # use colnames, if given
            labels = self.colnames
        res = ''
        for i in range(len(labels)):
            label = labels[i]
            res +='''<defs>
            <path d="M %s %s V 15" id="xAxisLabel%s"/>
            </defs>\n
            <text>
            <textPath xlink:href="#xAxisLabel%s">%s</textPath>
            </text>\n''' % (firstWidth + i * xWidth + 2,
                            self.height - 2,
                            i,
                            i,
                            self.confLT(str(label)))
        return res

    def xAxis_diagonalLabels(self, labels, firstWidth, xWidth, withLines=0):
        """Print labels on x-axis diagonally from bottom-left to upper-right.

        labels     ... list of strings with labelnames, if self.colnames
                         exists, then it is taken instead
        firstWidth ... float points from self.gridbasex to first label
        xWidth     ... float points between labels
        withLines  ... if withLines: draw lines in parallel to y-axis
        """
        if self.colnames: # use colnames, if given
            labels = self.colnames
        res = ''
        diff = self.height - self.gridbasey
        for i in range(len(labels)):
            label = labels[i]
            res += '''<defs>
            <path d="M %s %s l 600 600" id="xAxisLabel%s"/>
            </defs>\n
            <text style="text-anchor: start;">
            <textPath xlink:href="#xAxisLabel%s">%s</textPath>
            </text>\n''' % (firstWidth + i * xWidth - 7,
                            self.gridbasey + 7,
                            i,
                            i,
                            self.confLT(str(label)))
##            res += '<line x1="%s" x2="%s" y1="%s" y2="%s" />\n' % (
##                firstWidth + i * xWidth - 7,
##                firstWidth + i * xWidth + 600 -7 ,
##                self.gridbasey + 7,
##                self.gridbasey + 607,
##                )
            if withLines:
                res += '<line x1="%s" x2="%s" y1="%s" y2="%s" />\n' % (
                    firstWidth + i * xWidth,
                    firstWidth + i * xWidth,
                    self.gridbasey,
                    self.gridboundy,)
        return res

    def yAxis_horizontalLabels(self, labels, firstHeight, yHeight):
        """Print horizontal Labels on yAxis.

        labels      ... list: of strings with labelnames, if self.colnames
                         exists, then it is taken instead
        firstHeight ... float: points from self.gridbasey to first label
        yHeight     ... float: points between labels
        """
        res = ''
        if self.colnames: # use colnames, if given
            labels = self.colnames
        for i in range(len(labels)):
            label = labels[i]
            res += '''<text x="5" y="%s" style="text-anchor:start;">
                        <tspan baseline-shift="sub">%s</tspan>
                       </text>\n''' % (
                self.gridbasey - i * yHeight - firstHeight,
                self.confLT(label))
        return res
        

    def compute(self):
        """Compute the Diagram."""
        if self.result:
            return self.result

        if usedom:
            self.getDom()
            return self.xmldoc.toxml()
        # else: not usedom
        self.result = self.svgHeader()
        if self.errortext:
            self.result += self.printError()
        else:
            try:
                for action in self.getDrawingActions():
                    self.result += action()
            except RuntimeError:
                import sys
                self.errortext = sys.exc_info()[1].args[0]
                self.result = self.svgHeader() + self.printError()

        self.result += self.svgFooter()
        return self.result


    def computeYScale(self):
        """Compute scaling factor for y-direction."""
        if self.maxY() is None:
            raise RuntimeError, 'All values on y-axis must be numbers!'
        self.specialAttribHook()

        difY = float(self.maxY() - self.minY())
        if difY:
            self.yScale = float((self.gridbasey-self.gridboundy) / difY)
        else:
            self.yScale = 1.0
        return ''


    def computeXScale(self):
        """Compute scaling factor for x-direction."""
        if self.maxX() is None:
            raise RuntimeError, 'All values on x-axis must be numbers!'
        self.specialAttribHook()
        
        difX = float(self.maxX() - self.minX())
        if difX:
            self.xScale = float((self.gridboundx-self.gridbasex) / difX)
        else:
            self.xScale = 1.0
        return ''


    def confLT(self, text):
        """Convert the less than symbols in text ('<') to &lt;."""
        if type(text) in StringTypes:
            return text.replace("<", "&lt;")
        return text

    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.drawGraph,
                self.drawXYAxis,
                self.drawLegend,
                self.drawTitle]

    def drawGraph(self):
        "Abstract Method: Draw the the graph and name the columns."
        raise RuntimeError, "Can't use the abstract method drawGraph!"



    
class DataOnYAxis(BaseGraph):
    """Abstract class for DiagramKinds which have their data on y-axis.
    """

    def description():
        """see interfaces.IDiagamKind.description
        """
        return ['Continuous data on y-axis. Discrete data on x-axis.']
    description = staticmethod(description)


    def specialAttribHook(self):
        """Handling of the specialAttrib.

        Test datatype of specialAttrib & change data influenced by
          specialAttrib.

        Return: void
        On error: raise RuntimeError
        """
        pass # no specialAttrib things by default



class DataOnXAxis(BaseGraph):
    "Abstract class for DiagramKinds which have their data on x-axis."

    def description():
        "see interfaces.IDiagamKind.description"
        return ['Continuous data on x-axis. Discrete data on y-axis.']
    description = staticmethod(description)


    def specialAttribHook(self):
        """Handling of the specialAttrib.

        Test datatype of specialAttrib & change data influenced by
          specialAttrib.

        Return: void
        On error: raise RuntimeError
        """
        pass # no specialAttrib things by default


    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.computeXScale,
                self.drawXGridLines] + \
                BaseGraph.getDrawingActions(self)
