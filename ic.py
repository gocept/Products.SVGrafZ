################################################################################
## 
## SVGrafZ: InputConverters
##
## $Id: ic.py,v 1.6 2003/06/10 10:11:06 mac Exp $
################################################################################

from interfaces import IInputConverter, IInputConverterWithLegend
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
    """Abstract class for conversion from Z SQL Method."""

    def legend(self):
        """Returns the legend extracted out of the input data using
           self.convert."""
        return self._legend

    
    def _getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        raise RuntimeError, \
              'ConvertFrom_ZSQLMethod is abstract class'

class ConvertFrom_ZSQLMethod_DataInColumns (ConvertFrom_ZSQLMethod):
    """Abstract class for conversion from Z SQL Method.

    The sql result data has one column for each dataset (graph) in the
      diagram.
    """
    def convert(self, data, fixColumn):
        """Converts data to SVGrafZ input format.

        data      ... object, as returned by Z SQL Method
        fixColumn ... string, name of the column conaining data for axis with
                         discrete values
        Return:    list fitting to SVGrafZ' input format.
        Exception RuntimeError with error-text if an error occured.
        """
        try:
            res  = data.dictionaries()
            cols = data.names()
        except AttributeError:
            raise RuntimeError, \
                  "Data does not come from a Z SQL Method, can't convert it."

        if fixColumn is None:
            raise RuntimeError, \
                  "Reference Column not set, but it's required by converter."
        print res
        ret = []

        params = len(res[0])
        for i in range(0,params-1):
            ret.append([])

        for dict in res:
            i = 0
            for col in cols:
                if col == fixColumn:
                    continue
                try:
                    ret[i].append(self._getValList(dict[col], dict[fixColumn]))
                except KeyError:
                    raise RuntimeError, \
                          'Reference Column is not in source data.' 
                i += 1

        del cols[cols.index(fixColumn)]
        self._legend = cols
        
        print ret
        return ret



class yGraph_ZSQLMethod_DataInColumns(ConvertFrom_ZSQLMethod_DataInColumns):
    """Convert data from Z SQL Method with data in separate columns to y-axis.
    """
   
    __implements__ = IInputConverterWithLegend
    
    name = 'ZSQL (Data in Columns) to y-Axis'

    def registration(self):
        return {BarGraphs: [DS_ZSQLMethod]}

    def _getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        return [float(value), colname]

class xGraph_ZSQLMethod_DataInColumns(ConvertFrom_ZSQLMethod_DataInColumns):
    """Convert data from Z SQL Method with data in separate columns to x-axis.
    """
    
    __implements__ = IInputConverterWithLegend
    
    name = 'ZSQL (Data in Columns) to x-Axis'

    def registration(self):
        return {LineGraphs: [DS_ZSQLMethod],
                RowGraphs:  [DS_ZSQLMethod]}

    def _getValList(self, value, colname):
        """Put value and colname into a list in the right order."""
        return [colname, float(value)]




class ConvertFrom_ZSQLMethod_DataInRows (ConvertFrom_ZSQLMethod):
    """Abstract class for conversion from Z SQL Method.

    The result data of the Z SQL Method has to have 3 Columns:
    discColumn ... values for the axis displaying discrete data
    contColumn ... values for the axis displaying continuous data
    dataSetID  ... values identifying the dataset the tuple belonges to

    The value of 'Reference Column(s)' (fixcolumn) must look like:
      <name of discColumn>;<name of datasetID>

    The data must be ordered by column datasetID!
    
    """
    def convert(self, data, refCols):
        """Converts data to SVGrafZ input format.

        data    ... object: as returned by Z SQL Method
        refCols ... string: value of fixcolumn (see above)
         
        Return:    list fitting to SVGrafZ' input format.
        Exception RuntimeError with error-text if an error occured.
        """
        try:
            res  = data.dictionaries()
            cols = data.names()
        except AttributeError:
            raise RuntimeError, \
                  "Data does not come from a Z SQL Method, can't convert it."

        if refCols is None:
            raise RuntimeError, \
                  "Reference Columns not set, but it's required by converter."
        
        if len(cols) != 3:
            raise RuntimeError, \
                  "Z SQL Method must return exactly 3 columns."

        if len(res) == 0:
            return None
        
        refColNames = [x.strip() for x in str(refCols).split(';')]
        if len(refColNames) != 2:
            raise RuntimeError, \
                  "Reference Columns must have the format: <name of discrete column>;<name of dataset-id>."
               
        discColumn, datasetID = tuple(refColNames)
        if discColumn not in cols or datasetID not in cols:
            raise RuntimeError, \
                  "Column names from 'Reference Columns' must be in input data."
        
        print res
        print discColumn
        print datasetID
        ret = []
        self._legend = []
        
        curDatasetID = False
        dummy = res[0].copy()
        del dummy[datasetID]
        del dummy[discColumn]
        contColumn = dummy.keys()[0]
        curDataset = -1

        for dict in res:
            if curDatasetID != dict[datasetID]:
                ret.append([])
                curDatasetID = dict[datasetID]
                curDataset += 1
                self._legend.append(curDatasetID)
            ret[curDataset].append(self._getValList(dict[contColumn],
                                                   dict[discColumn]))
        print ret
        return ret

    

class yGraph_ZSQLMethod_DataInRows(ConvertFrom_ZSQLMethod_DataInRows):
    """Convert data from Z SQL Method with data in rows to y-axis.
    """
    
    __implements__ = IInputConverterWithLegend
    
    name = 'ZSQL (Data in Rows) to y-Axis'

    def registration(self):
        return {BarGraphs: [DS_ZSQLMethod]}

    def _getValList(self, contVal, discVal):
        """Put continuous and discrete value into a list in the right order."""
        return [float(contVal), discVal]

class xGraph_ZSQLMethod_DataInRows(ConvertFrom_ZSQLMethod_DataInRows):
    """Convert data from Z SQL Method with data in rows to x-axis.
    """
    
    __implements__ = IInputConverterWithLegend
    
    name = 'ZSQL (Data in Rows) to x-Axis'

    def registration(self):
        return {LineGraphs: [DS_ZSQLMethod],
                RowGraphs:  [DS_ZSQLMethod]}

    def _getValList(self, contVal, discVal):
        """Put continuous and discrete value into a list in the right order."""
        return [discVal, float(contVal)]
