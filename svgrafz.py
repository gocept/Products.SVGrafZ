# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
##
## $Id: svgrafz.py,v 1.30 2003/10/15 07:08:34 mac Exp $
################################################################################

import os
from sys import exc_info
import random
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.TALES import CompilerError
from ZODB.PersistentMapping import PersistentMapping

from interfaces import IInputConverterWithLegend
from registry import Registry
from icreg import ICRegistry
from svgconverters import SVG2SVG, SVG2PNG, SVG2PDF
from helper import TALESMethod

_www                   = os.path.join(os.path.dirname(__file__), 'www')
_defaultSVGrafZ        = 'defaultSVGrafZ'
_useDefaultDiagramKind = 'default diagramkind'
_useDefaultConverter   = 'default Converter'

class SVGrafZProduct(SimpleItem):
    """ProductClass of SVGrafZ."""

    meta_type = 'SVGrafZ'
    version = '0.21'

    manage_options = (
        {'label':'Properties',
         'action':'manage_editForm',
         'help':('SVGrafZ','SVGrafZ_Properties.html')},
        {'label':'View as SVG', 'action':'manage_view'},
        {'label':'View as PNG', 'action':'manage_viewPNG'},
        {'label':'View as PDF', 'action':'manage_viewPDF'},
        ) + SimpleItem.manage_options


    security=ClassSecurityInfo()

    security.declareProtected('View management screens', 'manage_editForm')
    manage_editForm = PageTemplateFile('SVGrafZEdit', _www)

    security.declareProtected('View management screens', 'manage_view')
    manage_view = PageTemplateFile('SVGrafZView', _www)

    
    security.declareProtected('View management screens', 'manage_viewPNG')
    manage_viewPNG = PageTemplateFile('SVGrafZViewPNG', _www)

    security.declareProtected('View management screens', 'manage_viewPDF')
    manage_viewPDF = PageTemplateFile('SVGrafZViewPDF', _www)


    security.declareProtected('View management screens', 'manage_edit')
    def manage_edit(self, REQUEST=None):
        """Save the new property values."""
        try:
            self.changeProperties(REQUEST)
            msg = 'Properties successfully saved.'
        except ValueError:
            msg = 'ERROR: ' + str(exc_info()[1])
        return self.manage_editForm(manage_tabs_message = msg)


    security.declareProtected('View management screens', 'changeProperties')
    def changeProperties(self, REQUEST=None, encoding='iso-8859-1', **kw):
        if REQUEST is None:
            REQUEST = kw
        if REQUEST == {}:
            return

        d = 'graphname'
        req = REQUEST.get(d, None)
        if not req or req == _useDefaultDiagramKind:
            self.dat[d] = None
        else:
            self.dat[d] = req

        d = 'convertername'
        req = REQUEST.get(d, None)
        if not req or req == _useDefaultConverter:
            self.dat[d] = None
        else:
            self.dat[d] = req


        data = ['title', 'stylesheet', 'fixcolumn', 'specialattrib']
        for d in data:
            req = REQUEST.get(d, None)
            if req: # catch also empty strings
                self.dat[d] = req
            else:
                self.dat[d] = None

        try:
            dataInt = ["gridlines", "height", "width"]
            for dd in dataInt:
                if REQUEST.get(dd): # catch also empty strings
                    self.dat[dd] = int(REQUEST.get(dd))
                else:
                    self.dat[dd] = None
        except ValueError:
            raise ValueError, '%s must be an integer number' % (dd)

        try:
            dataBool = ["intcaption", "fillgaps"]
            for dd in dataBool:
                if REQUEST.get(dd): # catch also empty strings
                    self.dat[dd] = int(REQUEST.get(dd))
                    if self.dat[dd] == 2:
                        self.dat[dd] = None
                else:
                    self.dat[dd] = None
        except ValueError:
            raise ValueError, '%s must be an integer number' % (dd)

        # Update TALES Methods
        tales = ["data", "legend", "colnames", "taltitle", ]
        for x in tales:
            expression = REQUEST.get(x)
            if expression is None:
                self.dat[x] = TALESMethod(None)
            else:
                self.dat[x] = TALESMethod(unicode(expression, encoding))


    security.declareProtected('View management screens', 'getSpecialAttribName')
    def getSpecialAttribName(self):
        "Get the name of the specialattrib of the currently selected diagram."
        try:
            return Registry.getKind(self.graphname()).specialAttribName
        except RuntimeError:
            return ''


    def __init__(self, id):
        self.id        = id
        self.dat = PersistentMapping() # automatical Persictence of Dictionary
        self.dat.update({'title':         None,
                         'graphname':     None,
                         'gridlines':     None,
                         'height':        None,
                         'width':         None,
                         'data':          TALESMethod(None),
                         'legend':        TALESMethod(None),
                         'colnames':      TALESMethod(None),
                         'stylesheet':    None,
                         'convertername': None,
                         'fixcolumn':     None,
                         'specialattrib': None,
                         'intcaption':    None,
                         'fillgaps':      None,
                         'taltitle':      TALESMethod(None),
                         })
        self.rnd = random.Random()
        self.current_version = self.version # set at creation & update

    def _update(self):
        """Update older versions."""
        try:
            version = self.current_version
        except AttributeError:
            # from 0.1a3 --> 0.1a4
            if self.dat['graphname'] == 'Einfaches Balkendiagramm' or \
                   self.dat['graphname'] == 'Zweifaches Balkendiagramm':
                self.dat['graphname'] =  'simple bar diagram'
            elif self.dat['graphname'] == 'Einfaches Liniendiagramm':
                self.dat['graphname'] = 'simple line diagram'
            elif self.dat['graphname'] == 'Gespiegeltes Liniendiagramm':
                self.dat['graphname'] = 'mirrored line diagram'
            elif self.dat['graphname'] == 'Einfaches Säulendiagramm':
                self.dat['graphname'] = 'simple column diagram'

            # from 0.1a4 --> 0.15
            self.current_version = '0.15'
            if self.dat['convertername'] == 'Z SQL Method to RowGraph':
                self.dat['convertername'] = 'ZSQL (Data in Columns) to y-Axis'
            elif self.dat['convertername'] == 'Z SQL Method to Graph':
                self.dat['convertername'] = 'ZSQL (Data in Columns) to x-Axis'
        if self.current_version == '0.15':
            self.current_version = '0.16'
            # nothing else to do
        if self.current_version < '0.19':
            self.rnd = random.Random()
            self.current_version = '0.19'
        if self.current_version < '0.20':
            self.dat['intcaption'] = None
            self.dat['fillgaps'] = None
            self.current_version = '0.20'
        if self.current_version < '0.21':
            self.dat['taltitle'] = TALESMethod(None)
            self.current_version = '0.21'
        if self.current_version < '0.22':
            # set self.current_version to new version
            pass


    security.declareProtected('View management screens', 'equalsGraphName')
    def equalsGraphName(self, name):
        """Test if the given name is equal to real graphname."""
        if name == _useDefaultDiagramKind and \
           self.dat['graphname'] is None:
            return 1
        if name == self.dat['graphname']:
            return 1
        return 0

    security.declareProtected('View management screens', 'equalsConverterName')
    def equalsConverterName(self, name):
        """Test if the given name is equal to real converterName."""
        if name == _useDefaultConverter and \
           self.dat['convertername'] is None:
            return 1
        if name == self.dat['convertername']:
            return 1
        return 0


    security.declareProtected('View', 'title')
    def title(self, default=None):
        "get title."
        return self.getAttribute('title', None, default)

    security.declareProtected('View', 'taltitle')
    def taltitle(self, default=None):
        "get taltitle."
        return self.getAttribute('taltitle', TALESMethod(None), default)

    security.declareProtected('View', 'graphname')
    def graphname(self, default=None):
        "get graphname."
        return self.getAttribute('graphname',
                                 Registry.getDefaultKindName(),
                                 default)

    security.declareProtected('View', 'gridlines')
    def gridlines(self, default=None):
        "get gridlines."
        return self.getAttribute('gridlines', 9, default)

    security.declareProtected('View', 'height')
    def height(self, default=None):
        "get height."
        return self.getAttribute('height', 300, default)

    security.declareProtected('View', 'width')
    def width(self, default=None):
        "get width."
        return self.getAttribute('width', 600, default)

    security.declareProtected('View', 'convertername')
    def convertername(self, default=None):
        "get convertername."
        return self.getAttribute('convertername',
                                 ICRegistry.getDefaultConverterName(),
                                 default)

    security.declareProtected('View', 'fixcolumn')
    def fixcolumn(self, default=None):
        "get fixcolumn."
        return self.getAttribute('fixcolumn', None, default)

    security.declareProtected('View', 'data')
    def data(self, default=None):
        "get data."
        return self.getAttribute('data', TALESMethod(None), default)

    security.declareProtected('View', 'legend')
    def legend(self, default=None):
        "get legend."
        return self.getAttribute('legend', TALESMethod(None), default)

    security.declareProtected('View', 'colnames')
    def colnames(self, default=None):
        "get colnames."
        return self.getAttribute('colnames', TALESMethod(None), default)

    security.declareProtected('View', 'stylesheet')
    def stylesheet(self, default=None):
        "get stylesheet."
        return self.getAttribute('stylesheet', None, default)

    security.declareProtected('View', 'specialattrib')
    def specialattrib(self, default=None):
        "get specialattrib."
        return self.getAttribute('specialattrib', None, default)

    security.declareProtected('View', 'intcaption')
    def intcaption(self, default=None):
        "get intcaption."
        return self.getAttribute('intcaption', 0, default)

    security.declareProtected('View', 'fillgaps')
    def fillgaps(self, default=None):
        "get fillgaps."
        return self.getAttribute('fillgaps', 0, default)


    def getAttribute(self, attrib, defaultVal, default=None):
        "Get the value of an attribute or aquire it."
        if not default: # try in self first if not excplicitly getting defaults
            if self.dat[attrib] is not None:
                if isinstance(self.dat[attrib], TALESMethod):
                    if self.dat[attrib].getExpression():
                        return self.dat[attrib]
                else:
                    return self.dat[attrib]
        return self.aquireAttribute(attrib, defaultVal)


    def aquireAttribute(self, attrib, defaultVal):
        "Aquire an attribute from default."
        try:
            if self.id == _defaultSVGrafZ:
                # go one directory up, if self is defaultGraph
                default = getattr(self.aq_inner.aq_parent.aq_parent,
                                  _defaultSVGrafZ)
            else:
                # search in same dir first
                default = getattr(self.aq_parent, _defaultSVGrafZ)
            if default == self:
                # no default graph found in upper direction, use defaultDefault
                raise AttributeError
            return default.getAttribute(attrib, defaultVal)
        except AttributeError:
            return defaultVal
        
        
    security.declareProtected('View management screens', 'getPossibleDiagrams')
    def getPossibleDiagrams(self):
        """Get a Dictionary ot available Diagrams."""
        types = Registry.getTypes()
        res = []
        for typ in types:
            kinds = []
            for kind in Registry.getKindNames(typ):
                kinds.append({'name':kind})
            res.append({'name':typ, 'kinds':kinds})
        res.append({'name':' ','kinds':[{'name':_useDefaultDiagramKind}]})
        res.sort(lambda x,y: cmp(x['name'],y['name']))
        return res


    security.declareProtected('View management screens','getPossibleConverters')
    def getPossibleConverters(self):
        """Get a Dictionary ot available Converters."""
        try:
            diagramTypes = Registry.getKind(self.graphname()).registration()
        except RuntimeError:
            diagramTypes = []
        ret = [{'name': ' ',
                'sources': [{'name': ' ',
                             'converters': [{'name': _useDefaultConverter}]
                             }
                            ]
                }
               ]

        for dt in diagramTypes:
            sources = []
            for source in ICRegistry.getSources(dt.name):
                converters = [{'name': conv}
                              for conv in ICRegistry.getConverters(dt.name,
                                                                   source)]
                sources.append({'name':       source,
                                'converters': converters})
            ret.append({'name':    dt.name,
                        'sources': sources})
        return ret
    


    security.declareProtected('View management screens',
                              'getDefaultPropertyValues')
    def getDefaultPropertyValues(self):
        """Get the aquired PropertyValues."""
        return self._getAllAttributes(1)
    
    def getPropertyValues(self):
        "Get the real or aquired PropertyValues."
        return self._getAllAttributes(0)
    
    security.declareProtected('View management screens',
                              'getRealPropertyValues')
    def getRealPropertyValues(self):
        "Get the real PropertyValues."
        r = {}
        for i,v in self.dat.items():
            if isinstance(v, TALESMethod):
                n = v.getExpression()
            else:
                n = v
            r[i] = n
        return r


    def _getAllAttributes(self, default):
        "Get the values of all attibutes as dictionary"
        res ={}
        for p in self.dat.keys():
            res[p] = getattr(self, p)(default=default)
            if default and isinstance(res[p], TALESMethod):
                res[p] = res[p].getExpression()
        return res


    def _getOutputConverter(self):
        """Compute output converter and value of SVGrafZ_PixelMode."""
        mode = self.REQUEST.get('SVGrafZ_PixelMode', None)
        if mode is None:
            mode = self.REQUEST.SESSION.get('SVGrafZ_PixelMode', None)
        if mode in [None, 0, '0']:
            return SVG2SVG(), 0
        elif mode in ['PDF', 'pdf']:
            return SVG2PDF(), 'pdf'
        else:
            return SVG2PNG(), 1


    security.declareProtected('View', 'html')
    def html(self, REQUEST=None):
        """Get HTML-Text to embed Image."""
        converter, value = self._getOutputConverter()
        url = self.absolute_url() + '?SVGrafZ_PixelMode=%s&rnd=%s' % (
            value,
            self.rnd.random())
        # rnd is to prevent caching of browser
        return converter.getHTML(url,
                                 self.height(),
                                 self.width())

        security.declareProtected('View', 'html')
    def html2(self, REQUEST=None):
        """HTML-Text to embed Image + HTML-tags"""
        return '<HTML><HEAD><TITLE>%s</TITLE></HEAD><BODY>%s</BODY></HTML>'%(
            self.title(), self.html(REQUEST))



    security.declareProtected('View', 'index_html')
    def index_html(self, client=None, REQUEST=None):
        """Render Image."""
        return self(client, REQUEST)

    def __call__(self, client=None, REQUEST={}):
        """Render the diagram."""
        graphClass     = Registry.getKind(self.graphname())
        current        = self.getPropertyValues()
        outputConverter, dummy = self._getOutputConverter()
        inputConverter = ICRegistry.getConverter(current['convertername'])
        errortext      = legend = colnames = stylesheet = data = title = None

        try:
            data = self.getValue(current['data'])
            try:
                data = inputConverter.convert(data, current['fixcolumn'])
            except RuntimeError:
                errortext = str(exc_info()[1])
        except (AttributeError, KeyError, CompilerError):
            errortext = 'DataSource "%s" is not existing.' % (current['data'])
        except RuntimeError:
            errortext = str(exc_info()[1])
        try:
            legend = self.getValue(current['legend'])
        except (AttributeError, KeyError, CompilerError):
            errortext = 'Legend "%s" is not existing.' % (current['legend'])

        if legend == 'converter':
            if IInputConverterWithLegend.isImplementedBy(inputConverter):
                legend = inputConverter.legend() # cause convert is already done
            else:
                errortext = "DataConverter '%s' can't be used with '%s'." % (
                    current['convertername'],
                    'string:converter')
        try:
            colnames = self.getValue(current['colnames'])
        except (AttributeError, KeyError, CompilerError):
            errortext = 'ColumnNames "%s" do not exist.' % (current['colnames'])

        if current['stylesheet']:
            try:
                stylesheet = getattr(self, current['stylesheet'])
                stylesheet = outputConverter.getStyleSheetURL(stylesheet)
            except AttributeError:
                errortext = 'Stylesheet "%s" is not existing.' % (
                    current['stylesheet'])
        try:
            title = self.getValue(current['taltitle'])
        except (AttributeError, KeyError, CompilerError, RuntimeError):
            errortext = '"Title with TALES" has Errors.'
        if title is None:
            title = current['title'] or ''
                
        otherParams = {'gridlines':  current['gridlines'],
                       'height':     current['height'],
                       'width':      current['width'],
                       'intcaption': current['intcaption'],
                       'fillgaps':   current['fillgaps'],
                       }
        graph = graphClass(data       = data,
                           legend     = legend,
                           colnames   = colnames,
                           title      = title,
                           stylesheet = stylesheet,
                           otherParams= otherParams,
                           errortext  = errortext)
        graph.setSpecialAttrib(current['specialattrib'])
        if REQUEST.RESPONSE:
            REQUEST.RESPONSE.setHeader('Content-Type',
                                       outputConverter.getDestinationFormat())
        outputConverter.setSourceData(graph.compute().encode('UTF-8'))
        if not outputConverter.convert():
            return outputConverter.getErrorResult()
        else:
            return outputConverter.getResultData()
        

    

    security.declareProtected('View', 'getValue')
    def getValue(self, method, context=None):
        """returns value returned by method

            method: TALESMethod instance to be evaluated, if None, None is
                returned.
        """
        if not isinstance(method, TALESMethod): 
            return None
        if not method.getExpression():
            return None

        if not context:
            context = self
        root = self.getPhysicalRoot()
        try:
            value = method.__of__(self)(here=context, 
                                        request=getattr(root, 'REQUEST', None), 
                                        root=root)
        except:
            raise RuntimeError, \
                  'DataSource-Method failed:\n%s'%str(exc_info()[1])
        if callable(value):
            value = value.__of__(self)
        return value

    def om_icons(self):
        """Return a list of icon URLs to be displayed by an ObjectManager."""
        icons = ({'path': 'misc_/SVGrafZ/icon.gif',
                  'alt': self.meta_type, 'title': self.meta_type},)
        if self.having_errors():
            icons = icons + ({'path': 'misc_/PageTemplates/exclamation.gif',
                              'alt': 'Error',
                              'title': 'This SVGrafZ has an error!'},)
        return icons

    security.declareProtected('View management screens', 'having_errors')
    def having_errors(self, whichTests='all'):
        """Test if we have errors.

        e.g. conflicts between diagramKind and converter
        """
        if whichTests == 'all':
            if self.current_version < self.version:
                return "Diagram is older than SVGrafZ-Product. \
                Please update the diagram as described in doc/update.txt"

            if self.current_version > self.version:
                return "Diagram is newer than SVGrafZ-Product. \
                Please update your SVGrafZ-Product to the latest version."

        diagramTypesOfConverter = ICRegistry.getConverter(
            self.convertername()).registration().keys()

        try:
            for diagramType in Registry.getKind(self.graphname()).registration():
                if diagramType in diagramTypesOfConverter:
                    return False
        except RuntimeError:
            return "DiagramKind does not exist any more.\
            Please choose another."
        return "DiagramKind and Converter are incompatible. \
        Please choose another Converter."


    security.declareProtected('View management screens',
                              'viewInputConverterDesription')
    def viewInputConverterDesription(self):
        return self._list2dictlist(ICRegistry.getConverter(
            self.convertername()).description())


    security.declareProtected('View management screens',
                              'viewDiagramKindDesription')
    def viewDiagramKindDesription(self):
        try:
            return self._list2dictlist(Registry.getKind(
                self.graphname()).description())
        except RuntimeError:
            return self._list2dictlist(['WARNING: Not existing DiagramKind!'])


    def _list2dictlist(self, list):
        return [{'item': x} for x in list]


InitializeClass(SVGrafZProduct)


manage_addDiagramForm = PageTemplateFile('addDiagramForm', _www)


def manage_addDiagramFunction(dispatcher, id, REQUEST=None):
    """Create a new graph and add it to myself."""
    if REQUEST:
        default = REQUEST.get('makeDefault', 0)
        if default:
            id = _defaultSVGrafZ
        REQUEST.RESPONSE.redirect('../../%s/manage_editForm'%(id))
    g = SVGrafZProduct(id)
    dispatcher.Destination()._setObject(id, g)


def manage_defaultPossible(dispatcher):
    """Test if it is possible to add an Default-SVGrafZ to the current dir."""
    return _defaultSVGrafZ not in dispatcher.Destination().objectIds(spec='SVGrafZ')
