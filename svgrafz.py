################################################################################
## 
## SVGrafZ
## Version: $Id: svgrafz.py,v 1.4 2003/04/16 14:14:38 mac Exp $
##
################################################################################

import os
from OFS.SimpleItem import SimpleItem
from registry import Registry
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from helper import TALESMethod

_www = os.path.join(os.path.dirname(__file__), 'www')
_defaultSVGrafZ = 'defaultSVGrafZ'


class SVGrafZProduct(SimpleItem):
    """ProductClass of SVGrafZ."""

    meta_type = 'SVGrafZ'

    manage_options = (
        {'label':'Properties', 'action':'manage_editForm'},
        {'label':'View', 'action':'html'},
        ) + SimpleItem.manage_options


    security=ClassSecurityInfo()

    security.declareProtected('View management screens', 'manage_editForm')
    manage_editForm = PageTemplateFile('SVGrafZEdit', _www)


    security.declareProtected('View management screens', 'manage_edit')
    def manage_edit(self, REQUEST=None):# title, graph, gridlines, height, width, REQUEST=None):
        """Save the new property values."""
        self.changeProperties(REQUEST)
        REQUEST.RESPONSE.redirect('../manage_main')

    security.declareProtected('View management screens', 'changeProperties')
    def changeProperties(self, REQUEST=None, encoding='iso-8859-1', **kw):
        if REQUEST is None:
            REQUEST = kw
        if REQUEST == {}:
            return
        
        
        self.dat['title']     = REQUEST.get("title", self.title)
        self.dat['graphname'] = REQUEST.get("graph", self.graphname)
        self.dat['stylesheet']= REQUEST.get("stylesheet", self.stylesheet)
        try:
            if REQUEST.get("gridlines"):
                self.dat['gridlines'] = int(REQUEST.get("gridlines"))
            if REQUEST.get("height"):
                self.dat['height']    = int(REQUEST.get("height"))
            if REQUEST.get("width"):
                self.dat['width']     = int(REQUEST.get("width"))
        except ValueError:
            raise ValueError, 'gridlines, height, width must be integer numbers'
        

        # Update TALES Methods
        tales = ["data", "legend", "colnames", ]
        for x in tales:
            expression = REQUEST.get(x)
            if expression is None:
                continue
            self.dat[x] = TALESMethod(unicode(expression, encoding))

        self._p_changed = 1 # tell Persistence Module of change


    def __init__(self, id):
        self.id        = id
        self.dat = {'title':     None,
                    'graphname': None,
                    'gridlines': None,
                    'height':    None,
                    'width':     None,
                    'data':      None,
                    'legend':    None,
                    'colnames':  None,
                    'stylesheet':None,
                    }

    security.declareProtected('View', 'title')
    def title(self, default=None):
        "get title."
        self.getAttribute('title', None, default)

    security.declareProtected('View', 'graphname')
    def graphname(self, default=None):
        "get graphname."
        self.getAttribute('graphname', Registry.getDefaultKindName(), default)

    security.declareProtected('View', 'gridlines')
    def gridlines(self, default=None):
        "get gridlines."
        self.getAttribute('gridlines', 9, default)

    security.declareProtected('View', 'height')
    def height(self, default=None):
        "get height."
        self.getAttribute('height', 300, default)

    security.declareProtected('View', 'width')
    def width(self, default=None):
        "get width."
        self.getAttribute('width', 600, default)

    security.declareProtected('View', 'data')
    def data(self, default=None):
        "get data."
        self.getAttribute('data', None, default)

    security.declareProtected('View', 'legend')
    def legend(self, default=None):
        "get legend."
        self.getAttribute('legend', None, default)

    security.declareProtected('View', 'colnames')
    def colnames(self, default=None):
        "get colnames."
        self.getAttribute('colnames', None, default)

    security.declareProtected('View', 'stylesheet')
    def stylesheet(self, default=None):
        "get stylesheet."
        self.getAttribute('stylesheet', None, default)


    def getAttribute(self, attrib, defaultVal, default=None):
        "Get the value of an attribute or aquire it."
        if not default: # try in self first if not excplicitly getting defaults
            if self.dat[attrib] is not None:
                return self.dat[attrib]
        return self.aquireAttribute(attrib, defaultVal)


    def aquireAttribute(self, attrib, defaultVal):
        "Aquire an attribute from default."
        try:
            default = getattr(self, _defaultSVGrafZ)
            return default.getAttribute(attrib, defaultVal)
        except AttributeError:
            return defaultVal
        
        
        

    security.declareProtected('View management screens', 'getPossibleDiagrams')
    def getPossibleDiagrams(self):
        """Get a Dictionary ot available Diagrams."""
        types = Registry.getTypes()
        print types
        res = []
        for typ in types:
            kinds = []
            for kind in Registry.getKindNames(typ):
                kinds.append({'name':kind})
                res.append({'name':typ, 'kinds':kinds})
        res.sort()
        return res

    security.declareProtected('View management screens',
                              'getDefaultPropertyValues')
    def getDefaultPropertyValues(self):
        """Get the aquired PropertyValues."""
        return self._getAllAttributes(1)
    
    def getPropertyValues(self):
        "Get the real or aquired PropertyValues."
        return self._getAllAttributes(0)

    def _getAllAttributes(self, default):
        "Get the values of all attibutes as dictionary"
        res ={}
        for p in self.dat.keys():
            res[p] = getattr(self, p)(default=default)
        return res
        

    security.declareProtected('View', 'html')
    def html(self):
        """Get HTML-Text to embed SVG-Image."""
        return u'<object type="image/svg+xml" width="%s" height="%s" data="%s">Ihr Browser unterstützt keine SVG-Grafiken. Schade.</object>' % (self.dat['width'], self.dat['height'], self.id)

    security.declareProtected('View', 'index_html')
    def index_html(self, client=None, REQUEST=None):
        """Render Image."""
        return self(client, REQUEST)

    def __call__(self, client=None, REQUEST={}):
        """Render the diagram."""
        graphClass = Registry.getKind(self.graphname())
        current    = self.getPropertyValues()
        title      = current['title']
        try:
            data = self.getValue(current['data'])
        except KeyError:
            title = 'Error: Given DataSource "%s" is not existing.' % (
                self.getDataMethodExpression())
            data = [[[1,1]]]
        try:
            legend = self.getValue(curent['legend'])
        except KeyError:
            title = 'KeyError: legend not existing'
            legend = None
        try:
            colnames = self.getValue(curent['colnames'])
        except KeyError:
            title = 'KeyError: column names not existing'
            colnames = None

        stylesheet = None
        if curent['stylesheet']:
            try:
                stylesheet = getattr(self, curent['stylesheet']).absolute_url()
            except AttributeError:
                title = 'AttributeError: stylesheet not existing'

        graph = graphClass(data      = data,
                           legend    = legend,
                           colnames  = colnames,
                           title     = title,
                           gridlines = curent['gridlines'],
                           height    = curent['height'],
                           width     = curent['width'],
                           stylesheet= stylesheet)
        if REQUEST.RESPONSE:
            REQUEST.RESPONSE.setHeader('Content-Type', 'image/svg+xml')
        return graph.compute().encode('UTF-8')

    
    def _getMethodExpression(self, method):
        """returns expression of method or '' if method is not a TALESMethod
        """
        # Uh.. this is ugly, but Python2.1's isinstance does not work with
        # extension classes
        try:
            if method.__class__.__name__ == 'TALESMethod':
                return method.getExpression()
        except AttributeError:            
            pass
        return ''

    security.declareProtected('View management screens',
        'getDataMethodExpression')
    def getDataMethodExpression(self):
        return self._getMethodExpression(self.data)

    security.declareProtected('View management screens',
        'getLegendMethodExpression')
    def getLegendMethodExpression(self):
        return self._getMethodExpression(self.legend)

    security.declareProtected('View management screens',
        'getColnamesMethodExpression')
    def getColnamesMethodExpression(self):
        return self._getMethodExpression(self.colnames)


    security.declareProtected('View', 'getValue')
    def getValue(self, method, context=None):
        """returns value returned by method

            method: TALESMethod instance to be evaluated, if None, None is
                returned.
        """
        if not isinstance(method, TALESMethod): 
            return None

        if not context:
            context = self
        root = self.getPhysicalRoot()
        value = method.__of__(self)(here=context, 
            request=getattr(root, 'REQUEST', None), 
            root=self.getPhysicalRoot())
        if callable(value):
            value = value.__of__(self)
        return value

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
