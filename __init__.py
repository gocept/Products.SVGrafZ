# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.10 2003/11/21 12:22:01 ctheune Exp $
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
import config

from zLOG import *
import os


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
if config.SVGrafZ_BatikServer_Binary:
    streams = os.popen3(config.SVGrafZ_BatikServer_Binary)
    LOG("SVGrafZ", 0, "Starting Batikserver [TODO: Status check]")

