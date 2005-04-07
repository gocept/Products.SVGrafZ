# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.18 2005/04/07 09:00:43 mac Exp $
##
################################################################################

# python imports
from telnetlib import Telnet
import os
import socket
from time import sleep

# Zope imports
from zLOG import *

# sibling imports
from Products.SVGrafZ.registry import Registry
from Products.SVGrafZ.icreg import ICRegistry
from Products.SVGrafZ import bar, line, row, ic
from Products.SVGrafZ.svgrafz import SVGrafZProduct
from Products.SVGrafZ.interfaces import IInputConverter, IDiagramKind
from Products.SVGrafZ.svgrafz import \
     SVGrafZProduct, manage_addDiagramForm, manage_addDiagramFunction, \
     manage_defaultPossible
from Products.SVGrafZ import config

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


# Start BatikServer 
def testConnectionToBatikServer():
    try:
        conn = Telnet(config.SVGrafZ_BatikServer_Host,
                      config.SVGrafZ_BatikServer_Port)
        conn.write('HELLO BatikServer\n\n')
        res = conn.read_all()
        if res:
            LOG("SVGrafZ", 0, "Connecting to BatikServer ... success.")
        conn.close()
    except socket.error:
        res = None
    if res != '0':
        LOG("SVGrafZ", 100, "Connecting to BatikServer ... failure.")

