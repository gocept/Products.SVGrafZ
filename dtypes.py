################################################################################
## 
## SVGrafZ: DataTypes ... Classes which do not get instanced
##
## $Id: dtypes.py,v 1.3 2003/06/03 12:41:32 mac Exp $
################################################################################

from interfaces import IDiagramType, IDataSource


## DiagramTypes
class BarGraphs:
    """DiagramType of bar graphs."""

    __implements__ = IDiagramType

    name = 'Balkendiagramme'


class RowGraphs:
    """DiagramType of row graphs."""

    __implements__ = IDiagramType

    name = 'Säulendiagramme'

class LineGraphs:
    """DiagramType of line graphs."""

    __implements__ = IDiagramType

    name = 'Liniendiagramme'



## DataSources
class DS_PythonScript:
    """DataSource: Python-Script (Should not need any conversion)."""

    __implements__ = IDataSource

    name = 'Script (Python)'

class DS_ZSQLMethod:
    """DataSource: Z SQL Method."""

    __implements__ = IDataSource

    name = 'Z SQL Method'
