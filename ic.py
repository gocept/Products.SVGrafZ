# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: InputConverters
##
## $Id: ic.py,v 1.15 2004/02/23 08:33:22 mac Exp $
################################################################################

from interfaces import IInputConverter, IInputConverterWithLegend, \
     IDefaultInputConverter
from dtypes import *
from DateTime import DateTime

class NoneConverter:
    """DefaultConverter which does no conversion."""

    __implements__ = IDefaultInputConverter

    name = 'NoneConverter'

    def description(self):
        "See interfaces.IInputConverter.description."
        return ['''Converter which does no real conversion. It only returns its
        input data, so input data must be in SVGrafZ-InputFormat.''']

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

    def description(self):
        "See interfaces.IInputConverter.description."
        return ['DataSource must be a Z SQL Method.',
                'This Converter can extract the legend from the DataSource. \
                To use this feature, enter "string:converter" (without the \
                quotes) into the field Legend.']

    def __init__(self):
        self._legend = []

    def legend(self):
        "Returns the legend extracted out of the input data using self.convert."
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

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod.description(self) + \
               ['The result of the Z SQL Method must have one column for each \
               dataset in the diagram, plus one column for the discrete values \
               which are assigned to them. The name of column containing \
               discrete values must be written in field ReferenceColumn above.']

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
        ret = []

        if not len(res):
            raise RuntimeError, \
                  "No Data to display."
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

        return ret



class yGraph_ZSQLMethod_DataInColumns(ConvertFrom_ZSQLMethod_DataInColumns):
    """Convert data from Z SQL Method with data in separate columns to y-axis.
    """

    __implements__ = IInputConverterWithLegend

    name = 'ZSQL (Data in Columns) to y-Axis'

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod_DataInColumns.description(self) + [
            'Continuous values are put to the x-axis.']
    
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

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod_DataInColumns.description(self) + \
               ['Continouus values are converted to y-axis.']

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

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod.description(self) + [
            'The result of the Z SQL Method must have exactly 3 columns:',
            'discColumn ... values for the axis displaying discrete data',
            'contColumn ... values for the axis displaying continuous data',
            'dataSetID ... values identifying the dataset the tuple belongs to',
            'The value of "Reference Column(s)" must look like:',
            '<name of discColumn>;<name of datasetID> \
            (all lower case (for most DBMS))',
            'The data must be ordered by column datasetID!']

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

        if len(res)  == 0: # no result
            return None

        if len(cols) != 3:
            raise RuntimeError, \
                  "Z SQL Method must return exactly 3 columns."


        refColNames = [x.strip() for x in str(refCols).split(';')]
        if len(refColNames) != 2:
            raise RuntimeError, \
                  "Reference Columns must have the format: \
                  <name of discrete column>;<name of dataset-id>."

        discColumn, datasetID = tuple(refColNames)
        if discColumn not in cols or datasetID not in cols:
            raise RuntimeError, \
                  "Column names from 'Reference Columns' must be in input data."

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
        return ret



class yGraph_ZSQLMethod_DataInRows(ConvertFrom_ZSQLMethod_DataInRows):
    """Convert data from Z SQL Method with data in rows to y-axis.
    """

    __implements__ = IInputConverterWithLegend

    name = 'ZSQL (Data in Rows) to y-Axis'

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod_DataInRows.description(self) + [
            'discColumn: y-axis',
            'contColumn: x-axis']

    def registration(self):
        return {BarGraphs: [DS_ZSQLMethod]}

    def _getValList(self, contVal, discVal):
        """Put continuous and discrete value into a list in the right order."""
        try:
            return [float(contVal), discVal]
        except (ValueError):
            raise RuntimeError, \
                  'Continuous data column contains "%s" which is no number.' % \
                  contVal

class xGraph_ZSQLMethod_DataInRows(ConvertFrom_ZSQLMethod_DataInRows):
    """Convert data from Z SQL Method with data in rows to x-axis.
    """

    __implements__ = IInputConverterWithLegend

    name = 'ZSQL (Data in Rows) to x-Axis'

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod_DataInRows.description(self) + [
            'discColumn: x-axis',
            'contColumn: y-axis']

    def registration(self):
        return {LineGraphs: [DS_ZSQLMethod],
                RowGraphs:  [DS_ZSQLMethod]}

    def _getValList(self, contVal, discVal):
        """Put continuous and discrete value into a list in the right order."""
        try:
            return [discVal, float(contVal)]
        except ValueError:
            raise RuntimeError, \
                  'Continuous data column contains "%s" which is no number.' % \
                  contVal
        



class xGraph_ZSQLMethod_DataInRows_Date(ConvertFrom_ZSQLMethod_DataInRows):
    """Convert data from Z SQL Method with data in rows to x-axis.
    discrete value must be a german date (DD.MM.YYYY)
    """

    __implements__ = IInputConverterWithLegend

    name = 'ZSQL (Data in Rows) to x-Axis (discrete = Date)'

    def description(self):
        "See interfaces.IInputConverter.description."
        return ConvertFrom_ZSQLMethod_DataInRows.description(self) + [
            'discColumn: x-axis',
            'contColumn: y-axis',
            'In discColumn must be a dates with day showing up before month.']

    def registration(self):
        return {LineGraphs: [DS_ZSQLMethod],
                RowGraphs:  [DS_ZSQLMethod]}

    def _getValList(self, contVal, discVal):
        """Put continuous and discrete value into a list in the right order."""
        try: 
            return [DateTime_GermanStr(discVal, datefmt = "international"),
                    contVal]
        except ValueError:
            raise RuntimeError, \
                  'Continuous data column contains "%s" which is no number.' % \
                  contVal
        


class DateTime_GermanStr (DateTime):
    """DateTime with German string representation."""
    def __str__(self):
        return self.strftime('%d.%m.%Y')

    def __float__(self):
        """Nevessary because SVGrafZ tries to cast everything to float."""
        raise ValueError

