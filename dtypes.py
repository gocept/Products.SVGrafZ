################################################################################
## 
## SVGrafZ: DataTypes ... Classes which do not get instanced
##
## $Id: dtypes.py,v 1.2 2003/05/30 11:42:24 mac Exp $
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



## DataSources
class DS_PythonScript:
    """DataSource: Python-Script (Should not need any conversion)."""

    __implements__ = IDataSource

    name = 'Script (Python)'

class DS_ZSQLMethod:
    """DataSource: Z SQL Method."""

    __implements__ = IDataSource

    name = 'Z SQL Method'
