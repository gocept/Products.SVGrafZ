################################################################################
## 
## SVGrafZ
## Version: $Id: svgrafz.py,v 1.7 2003/04/17 13:24:32 mac Exp $
##
################################################################################

import os
from OFS.SimpleItem import SimpleItem
from registry import Registry
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from helper import TALESMethod
from ZODB.PersistentMapping import PersistentMapping

_www = os.path.join(os.path.dirname(__file__), 'www')
_defaultSVGrafZ = 'defaultSVGrafZ'
_useDefaultDiagramKind = 'default diagramkind'
def pdb():
    import pdb
    pdb.set_trace()


class SVGrafZProduct(SimpleItem):
    """ProductClass of SVGrafZ."""

    meta_type = 'SVGrafZ'

    manage_options = (
        {'label':'Properties', 'action':'manage_editForm'},
        {'label':'View', 'action':'manage_view'},
        ) + SimpleItem.manage_options


    security=ClassSecurityInfo()

    security.declareProtected('View management screens', 'manage_editForm')
    manage_editForm = PageTemplateFile('SVGrafZEdit', _www)

    security.declareProtected('View management screens', 'manage_view')
    manage_view = PageTemplateFile('SVGrafZView', _www)


    security.declareProtected('View management screens', 'manage_edit')
    def manage_edit(self, REQUEST=None):
        """Save the new property values."""
        self.changeProperties(REQUEST)
        return self.manage_editForm(manage_tabs_message = 'Properties saved.')


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

        data = ['title', 'stylesheet']
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
                         })


    security.declareProtected('View management screens', 'equalsGraphName')
    def equalsGraphName(self, name):
        """Test if the given name is equal to real graphname."""
        if name == _useDefaultDiagramKind and \
           self.dat['graphname'] is None:
            return 1
        if name == self.dat['graphname']:
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
        

    security.declareProtected('View', 'html')
    def html(self):
        """Get HTML-Text to embed SVG-Image."""
        return u'<object type="image/svg+xml" width="%s" height="%s" data="%s">Ihr Browser unterstützt keine SVG-Grafiken. Schade.</object>' % (self.width(), self.height(), self.id)



    security.declareProtected('View', 'index_html')
    def index_html(self, client=None, REQUEST=None):
        """Render Image."""
        return self(client, REQUEST)

    def __call__(self, client=None, REQUEST={}):
        """Render the diagram."""
        graphClass = Registry.getKind(self.graphname())
        print graphClass
        current    = self.getPropertyValues()
        title      = current['title']
        try:
            data = self.getValue(current['data'])
        except KeyError:
            title = 'Error: Given DataSource "%s" is not existing.' % (
                self.getDataMethodExpression())
            data = [[[1,1]]]
        try:
            legend = self.getValue(current['legend'])
        except KeyError:
            title = 'KeyError: legend not existing'
            legend = None
        try:
            colnames = self.getValue(current['colnames'])
        except KeyError:
            title = 'KeyError: column names not existing'
            colnames = None

        stylesheet = None
        if current['stylesheet']:
            try:
                stylesheet = getattr(self, current['stylesheet']).absolute_url()
            except AttributeError:
                title = 'AttributeError: stylesheet not existing'

        graph = graphClass(data      = data,
                           legend    = legend,
                           colnames  = colnames,
                           title     = title,
                           gridlines = current['gridlines'],
                           height    = current['height'],
                           width     = current['width'],
                           stylesheet= stylesheet)
        if REQUEST.RESPONSE:
            REQUEST.RESPONSE.setHeader('Content-Type', 'image/svg+xml')
        return graph.compute().encode('UTF-8')

    

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
