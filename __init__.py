# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.14 2004/03/09 21:23:57 ctheune Exp $
##
################################################################################

from registry import Registry
from icreg import ICRegistry
import bar, line, row
import ic
from svgrafz import SVGrafZProduct
from interfaces import IInputConverter, IDiagramKind
from telnetlib import Telnet

from svgrafz import SVGrafZProduct, manage_addDiagramForm, \
     manage_addDiagramFunction, manage_defaultPossible
import config

from zLOG import *
import os
import socket
from telnetlib import Telnet
from time import sleep

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
def startBatikServer():
    def connect_BatikServer(logtxt):
        conn = Telnet(config.SVGrafZ_BatikServer_Host,
                      config.SVGrafZ_BatikServer_Port)
        conn.write('HELLO BatikServer\n\n')
        res = conn.read_all()
        if res:
            LOG("SVGrafZ", 0, logtxt)
        conn.close()
        return res
    
    # Start a new batik server blindly
    LOG("SVGrafZ", 0, "Starting new BatikServer.")
    os.spawnl(os.P_NOWAIT, config.SVGrafZ_Java_Path, "-Djava.awt.headless==true", "-classpath", "%s;%s" % (config.SVGrafZ_Batik_Path, config.SVGrafZ_BatikServer), "batikServer", "-l", "batikserver.log")
    sleep(3)

    try:
        res = connect_BatikServer("Connecting to BatikServer ... success.")
    except socket.error:
        res = None

    if res != '0':
        LOG("SVGrafZ", 100, "Connecting to BatikServer ... failure. Maybe later.")

