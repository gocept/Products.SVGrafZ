################################################################################
## 
## SVGrafZ
##
## $Id: svgrafz.py,v 1.17 2003/06/04 08:56:17 mac Exp $
################################################################################

import os
from OFS.SimpleItem import SimpleItem
from registry import Registry
from icreg import ICRegistry
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.TALES import CompilerError
from helper import TALESMethod
from ZODB.PersistentMapping import PersistentMapping
from svgconverters import SVG2SVG, SVG2PNG

_www                   = os.path.join(os.path.dirname(__file__), 'www')
_defaultSVGrafZ        = 'defaultSVGrafZ'
_useDefaultDiagramKind = 'default diagramkind'
_useDefaultConverter   = 'default Converter'

def pdb():
    import pdb
    pdb.set_trace()

class SVGrafZProduct(SimpleItem):
    """ProductClass of SVGrafZ."""

    meta_type = 'SVGrafZ'
    version = '0.1a4'

    manage_options = (
        {'label':'Properties',
         'action':'manage_editForm',
         'help':('SVGrafZ','SVGrafZ_Properties.html')},
        {'label':'View as SVG', 'action':'manage_view'},
        {'label':'View as PNG', 'action':'manage_viewPNG'},
        ) + SimpleItem.manage_options


    security=ClassSecurityInfo()

    security.declareProtected('View management screens', 'manage_editForm')
    manage_editForm = PageTemplateFile('SVGrafZEdit', _www)

    security.declareProtected('View management screens', 'manage_view')
    manage_view = PageTemplateFile('SVGrafZView', _www)

    
    security.declareProtected('View management screens', 'manage_viewPNG')
    manage_viewPNG = PageTemplateFile('SVGrafZViewPNG', _www)


    security.declareProtected('View management screens', 'manage_edit')
    def manage_edit(self, REQUEST=None):
        """Save the new property values."""
        try:
            self.changeProperties(REQUEST)
            msg = 'Properties successfully saved.'
        except ValueError:
            import sys
            msg = 'ERROR: ' + str(sys.exc_info()[1])
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
            if req:
                self.dat[d] = req
            else:
                self.dat[d] = None

        try:
            dataInt = ["gridlines", "height", "width"]
            for dd in dataInt:
                if REQUEST.get(dd):
                    self.dat[dd] = int(REQUEST.get(dd))
                else:
                    self.dat[dd] = None
        except ValueError:
            raise ValueError, '%s must be an integer number' % (dd)
        
        # Update TALES Methods
        tales = ["data", "legend", "colnames", ]
        for x in tales:
            expression = REQUEST.get(x)
            if expression is None:
                self.dat[x] = TALESMethod(None)
            else:
                self.dat[x] = TALESMethod(unicode(expression, encoding))


    security.declareProtected('View management screens', 'getSpecialAttribName')
    def getSpecialAttribName(self):
        "Get the name of the specialattrib of the currently selected diagram."
        return Registry.getKind(self.graphname()).specialAttribName


    def __init__(self, id):
        self.id        = id
        self.dat = PersistentMapping() # automatical Persictence of Dictionary
        self.dat.update({'title':     None,
                         'graphname': None,
                         'gridlines': None,
                         'height':    None,
                         'width':     None,
                         'data':      TALESMethod(None),
                         'legend':    TALESMethod(None),
                         'colnames':  TALESMethod(None),
                         'stylesheet':None,
                         'convertername': None,
                         'fixcolumn': None,
                         'specialattrib': None
                         })

    def _update(self):
        """Update older versions."""
        if self.dat['graphname'] == 'Einfaches Balkendiagramm' or \
               self.dat['graphname'] == 'Zweifaches Balkendiagramm':
           self.dat['graphname'] =  'simple bar diagram'
        elif self.dat['graphname'] == 'Einfaches Liniendiagramm':
            self.dat['graphname'] = 'simple line diagram'
        elif self.dat['graphname'] == 'Gespiegeltes Liniendiagramm':
            self.dat['graphname'] = 'mirrored line diagram'
        elif self.dat['graphname'] == 'Einfaches Säulendiagramm':
            self.dat['graphname'] = 'simple column diagram'
        else:
            print self.dat['graphname']



        
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
        diagramTypes = Registry.getKind(self.graphname()).registration()
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
        else:
            return SVG2PNG(), 1


    security.declareProtected('View', 'html')
    def html(self, REQUEST=None):
        """Get HTML-Text to embed Image."""
        converter, value = self._getOutputConverter()
        url = self.id + '?SVGrafZ_PixelMode=%s' % (value,)
        return converter.getHTML(url,
                                 self.height(),
                                 self.width())
    


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
        errortext      = legend = colnames = stylesheet = data = None

        try:
            data = self.getValue(current['data'])
            try:
                data = inputConverter.convert(data, current['fixcolumn'])
            except RuntimeError:
                import sys
                errortext = str(sys.exc_info()[1])

        except (AttributeError, KeyError, CompilerError):
            errortext = 'DataSource "%s" is not existing.' % (current['data'])
        try:
            legend = self.getValue(current['legend'])
        except (AttributeError, KeyError, CompilerError):
            errortext = 'Legend "%s" is not existing.' % (current['legend'])
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

        graph = graphClass(data      = data,
                           legend    = legend,
                           colnames  = colnames,
                           title     = current['title'] or '',
                           gridlines = current['gridlines'],
                           height    = current['height'],
                           width     = current['width'],
                           stylesheet= stylesheet,
                           errortext = errortext)
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
        value = method.__of__(self)(here=context, 
                                    request=getattr(root, 'REQUEST', None), 
                                    root=root)
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
    def having_errors(self):
        """Test if we have errors.

        e.g. conflicts between diagramKind and converter
        """
        diagramTypesOfConverter = ICRegistry.getConverter(
            self.convertername()).registration().keys()

        for diagramType in Registry.getKind(self.graphname()).registration():
            if diagramType in diagramTypesOfConverter:
                return False
        return "DiagramKind and Converter are incompatible. Please choose another Converter."

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
