# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: helper.py,v 1.2 2003/10/15 07:08:34 mac Exp $
##
################################################################################
"""
Utility functions and classes
Partly taken from Formulon which is (C) by gocept gmbh & co. kg
"""

import Acquisition
import Shared.DC.ZRDB.Results
from Persistence import Persistent
from Products.PageTemplates.Expressions import getEngine


class TALESMethod(Persistent, Acquisition.Implicit):
    """A method object; calls method name in acquisition context.

        Taken from Formulator.
    """
    
    def __init__(self, text):
        self.setExpression(text)

    def __call__(self, **kw):
        if self._text == "":
            return None
        expr = getEngine().compile(self._text)
        return getEngine().getContext(kw).evaluate(expr)

    def getExpression(self):
        return self._text

    def setExpression(self, text):
        #if isinstance(text, str):
        #    text = unicode(text, 'UTF-8')
        #assert isinstance(text, unicode), 'Expression must be a unicode '\
        #    'type (%r)' % (text, )
        self._text = text

    def __str__(self):
        return self.getExpression().encode('UTF-8')

