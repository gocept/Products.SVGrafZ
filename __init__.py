# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.9 2003/11/20 15:18:21 ctheune Exp $
##
################################################################################

from registry import Registry
from icreg import ICRegistry
import bar, line, row
import ic
from svgrafz import SVGrafZProduct
from interfaces import IInputConverter, IDiagramKind

from svgrafz import SVGrafZProduct, manage_addDiagramForm, \
     manage_addDiagramFunction, manage_defaultPossible

from zLOG import *
import os

BATIK_SERVER_LOCATION = ""

def initialize(registrar):
    # register diagramkinds
    registerDiagramKinds(bar)
    registerDiagramKinds(line)
    registerDiagramKinds(row)

    # register InputConverters
    registerConverters(ic)
    
    registrar.registerClass(
        SVGrafZProduct, 
        constructors = (manage_addDiagramForm,
                        manage_addDiagramFunction,
                        manage_defaultPossible,
                        ),
        icon = 'www/icon.gif'
        )
    registrar.registerHelp()

def registerConverters(module):
    """Registers all input converters found in the given module."""
    for attrib in dir(module):
        try:
            potentialCoverter = getattr(module, attrib)
            if IInputConverter.isImplementedByInstancesOf(potentialCoverter):
                ICRegistry.register(potentialCoverter)
        except TypeError:
            pass


def registerDiagramKinds(module):
    """Registers all diagramKinds found in the given module."""
    for attrib in dir(module):
        try:
            potentialDiagramK = getattr(module, attrib)
            if IDiagramKind.isImplementedByInstancesOf(potentialDiagramK):
                Registry.register(potentialDiagramK)
        except TypeError:
            pass


# Initialize BatikServer 
if BATIK_SERVER_LOCATION:
    streams = os.popen3(BATIK_SERVER_LOCATION)
    LOG("SVGrafZ", 0, "Starting Batikserver [TODO: Status check]")

