################################################################################
## 
## SVGrafZ: Base
## Version: $Id: base.py,v 1.18 2003/08/18 13:00:53 mac Exp $
##
################################################################################

from math import log10,floor,ceil
from types import *
from config import SVGrafZ_default_Color, SVGrafZ_legend_name
from string import split

# set this var to 1 to use the dom generation (not complete yet)
usedom = 0
if usedom:
    from xml.dom.minidom import Document


class BaseGraph:
    """Abstract base class for all diagramKinds providing base functionallity.
    """

    __computed_results__ = None
    specialAttribName    = None


    def setSpecialAttrib(self, value):
        """Set the value of the special attribute."""
        self.specialAttrib = value


    def hasLegend(self):
        "Has the graph a legend?"
        return (type(self.legend) == type([])) and self.legend

    def getDom(self):
        import pdb2
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
                                         InstanceType,
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
        <text x="%s" y="%s" style="%s">%s</text>
        """ % ((self.gridboundx + self.width) / 2,
               self.gridboundy + 10,
               'text-anchor: middle; font-weight: bold;',
               SVGrafZ_legend_name)
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

        step = 0
        print `self.errortext`
        for errortext in split(self.confLT('Error: ' + self.errortext), '\n'):
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
                    self.gridboundy - 10,)
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
            res += '<text x="5" y="%s" style="text-anchor:start;">%s</text>\n'\
                   % (self.gridbasey - i * yHeight - firstHeight,
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
                self.errortext = str(sys.exc_info()[1])
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
        """Convert the littler than symbols ('<') to &lt;."""
        return str(text).replace('<', '&lt;')

    def getDrawingActions(self):
        """Returns the methods which are used to draw the graph."""
        return [self.drawGraph,
                self.drawXYAxis,
                self.drawLegend,
                self.drawTitle]


    
class DataOnYAxis(BaseGraph):
    """Abstract class for DiagramKinds which have their data on y-axis.
    """

    def description():
        """see interfaces.IDiagamKind.description
        """
        return ['Continuous data on y-axis. Discrete data on x-axis.']
    description = staticmethod(description)

    def __init__(self,
                 data=None,
                 width=0,
                 height=0,
                 gridlines=0,
                 legend=None,
                 colnames=None,
                 title=None,
                 stylesheet=None,
                 errortext=None):
        "See IDiagramKind.__init__"
        self.data       = data
        self.width      = width
        self.height     = height
        self.legend     = legend
        self.colnames   = colnames
        self.gridlines  = gridlines
        self.title      = title
        self.stylesheet = stylesheet
        self.errortext  = errortext

        self.result   = ''

##      Achtung: die Koordinaten 0,0 sind im SVG links oben!
##        gridbasey   unteres Ende in y-Richtung
##        gridboundy  oberes  Ende in y-Richtung
##        gridbasey groesser gridboundy!
##        gridbasex   unteres (linkes) Ende in x-Richtung
##        gridboundx  oberes (rechtes) Ende in x-Richtung
##        gridbasex kleiner gridboundx!

        self.gridbasey  = self.height * 0.9333
        self.gridboundy = self.height * 0.0333
        self.gridbasex  = self.width  * 0.0666
        if self.hasLegend():
            self.gridboundx = self.width * 0.8
        else:
            self.gridboundx = self.width * 0.98


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
        return [self.computeYScale,
                self.drawYGrindLines,] + \
                BaseGraph.getDrawingActions(self)

    def drawGraph(self):
        "Abstract Method: Draw the Lines of the graph and name the columns."
        raise RuntimeError, "Can't use the abstract methon drawGraph!"

