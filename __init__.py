# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ
## Version: $Id: __init__.py,v 1.11 2003/12/03 10:11:49 mac Exp $
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
if config.SVGrafZ_BatikServer_Invoke_Cmd:
    def connect_BatikServer(logtxt):
        conn = Telnet(config.SVGrafZ_BatikServer_Host,
                      config.SVGrafZ_BatikServer_Port)
        conn.write('HELLO BatikServer\n\n')
        res = conn.read_all()
        if res:
            LOG("SVGrafZ", 0, logtxt)
        conn.close()
        return res
    
    succesfulConnect = 0            
    try: # first look, if Batikserver is already running
        res = connect_BatikServer("Starting BatikServer ... already runs.")
        if res != '0':
            LOG("SVGrafZ", 100, "Connecting BatikServer ... failure."\
                "(The process listening on %s:%s is not BatikServer.)" %
                (config.SVGrafZ_BatikServer_Host,
                 config.SVGrafZ_BatikServer_Port))
        succesfulConnect = 1
    except (socket.error): # not runnig ... so start it
        streams = os.popen3(config.SVGrafZ_BatikServer_Invoke_Cmd)
        for i in range(1, 10): # test if Batikserver is now running
            try:
                succesfulConnect = connect_BatikServer(
                    "Starting BatikServer ... success.")
                break
            except (socket.error): 
                sleep(1) # no batikServer runing, try again in 1 sec

    if not succesfulConnect:
        LOG("SVGrafZ",
            100,
            "Starting BatikServer ... failure (Server does not (yet) run "\
            "(see BatikServer's logfile)")

