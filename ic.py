################################################################################
## 
## SVGrafZ: InputConverters
##
## $Id: ic.py,v 1.2 2003/06/03 12:41:32 mac Exp $
################################################################################

from interfaces import IInputConverter
from dtypes import *


class NoneConverter:
    """DefaultConverter which does no conversion."""
    
    __implements__ = IInputConverter
    
    name = 'NoneConverter'
    
    def registration(self):
        return {BarGraphs:  [DS_PythonScript],
                RowGraphs:  [DS_PythonScript],
                LineGraphs: [DS_PythonScript],}

    def convert(self, data, fixColumn):
        """Converts data to SVGrafZ input format.

        Parameter: data ... list as returned by python.
        Return:    list fitting to SVGrafZ input format.
        """
        return data

class ConvertFrom_ZSQLMethod:
    """Abstract Class for conversion from Z SQL Method."""
    def convert(self, data, fixColumn):
        """Converts data to SVGrafZ input format.

        Parameter: data ... object as returned by Z SQL Method
        Return:    list fitting to SVGrafZ input format.
        Exception RuntimeError with error-text if an error occured.
        """
        try:
            res = data.dictionaries()
        except AttributeError:
            raise RuntimeError, \
                  "Data does not come from a Z SQL Method, can't convert it."

        if fixColumn is None:
            raise RuntimeError, \
                  "Reference Column not set, but it's required by converter."

        ret = []

        params = len(res[0])
        for i in range(0,params-1):
            ret.append([])

        for dict in res:
            i = 0
            for val in dict.keys():
                if val == fixColumn:
                    continue
                try:
                    ret[i].append(self.getValList(dict[val], dict[fixColumn]))
                except KeyError:
                    raise RuntimeError, \
                          'Reference Column is not in source data.' 
                i += 1
        return ret
    def getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        raise RuntimeError, \
              'Direct use of class ConvertFrom_ZSQLMethod is prohibited.'


class RowGraph_ZSQLMethod(ConvertFrom_ZSQLMethod):
    """Convert data from Z SQL Method to RowGraph."""
    
    __implements__ = IInputConverter
    
    name = 'Z SQL Method to RowGraph'

    def registration(self):
        return {BarGraphs: [DS_ZSQLMethod]}

    def getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        return [float(value), colname]

class LineRowGraph_ZSQLMethod(ConvertFrom_ZSQLMethod):
    """Convert data from Z SQL Method to a line- or bar-graph."""
    
    __implements__ = IInputConverter
    
    name = 'Z SQL Method to Graph'

    def registration(self):
        return {LineGraphs: [DS_ZSQLMethod],
                RowGraphs:  [DS_ZSQLMethod]}

    def getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        return [colname, float(value)]

