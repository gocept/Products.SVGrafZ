# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: DataTypes ... Classes which do not get instanced
##
## $Id$
################################################################################

from Products.SVGrafZ.interfaces import IDiagramType, IDataSource


## DiagramTypes
class BarGraphs:
    """DiagramType of bar graphs."""

    __implements__ = IDiagramType

    name = 'bar diagrams'


class RowGraphs:
    """DiagramType of row graphs."""

    __implements__ = IDiagramType

    name = 'column diagrams'

class LineGraphs:
    """DiagramType of line graphs."""

    __implements__ = IDiagramType

    name = 'line diagrams'



## DataSources
class DS_PythonScript:
    """DataSource: Python-Script (Should not need any conversion)."""

    __implements__ = IDataSource

    name = 'Script (Python)'

class DS_ZSQLMethod:
    """DataSource: Z SQL Method."""

    __implements__ = IDataSource

    name = 'Z SQL Method'
