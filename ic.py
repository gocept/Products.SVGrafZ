################################################################################
## 
## SVGrafZ: InputConverters
##
## $Id: ic.py,v 1.1 2003/05/30 11:42:24 mac Exp $
################################################################################

from interfaces import IInputConverter
from dtypes import *


class NoneConverter:
    """DefaultConverter which does no conversion."""
    
    __implements__ = IInputConverter
    
    name = 'NoneConverter'
    
    def registration(self):
        return {BarGraphs: [DS_PythonScript],
                RowGraphs: [DS_PythonScript]}

    def convert(self, data, fixColumn):
        """Converts data to SVGrafZ input format.

        Parameter: data ... type depending on converter
        Return:    list fitting to SVGrafZ input format.
        """
        return data

class RowGraph_ZSQLMethod:
    """Convert data from Z SQL Method to RowGraph."""
    
    __implements__ = IInputConverter
    
    name = 'Z SQL Method to RowGraph'

    def registration(self):
        return {BarGraphs: [DS_ZSQLMethod]}

    def convert(self, data, fixColumn):
        """Converts data to SVGrafZ input format.

        Parameter: data ... type depending on converter
        Return:    list fitting to SVGrafZ input format.
        Exception RuntimeError with error-text if an error occured.
        """
        try:
            res = data.dictionaries()
        except AttributeError:
            raise RuntimeError, "Error: Data does not come from a Z SQL Method, can't convert it."

        if fixColumn is None:
            raise RuntimeError, "Error: Reference Column not set, but it's required by converter."

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
                    ret[i].append([float(dict[val]), dict[fixColumn]])
                except KeyError:
                    raise RuntimeError, 'Error: Reference Column is not in source data.' 
                i += 1
        print(ret)
        return ret
