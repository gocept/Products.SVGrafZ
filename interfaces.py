# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: Interfaces
##
## $Id: interfaces.py,v 1.18 2005/02/16 09:06:52 mac Exp $
################################################################################

# Zope imports
from Interface import Interface, Attribute

class IDiagramType(Interface):
    """Interface for DiagramTypes."""

    name = Attribute("Name of the DiagramType.")
        



class IDiagramKind(Interface):
    """Interface for DiagramKinds."""

    name = Attribute("Name of the DiagramKind.")
    specialAttribName = Attribute("Name of the special Attribute or None.")

    def __init__(data        = None,
                 legend      = None,
                 colnames    = None,
                 title       = None,
                 stylesheet  = None,
                 errortext   = None,
                 otherParams = {}):
        """Initialize and set the parameters for the graph.

        Format of data:
        data = [[[x11,y11],[x12,y12],[x13,y13],...],
                [[x21,y21],[x22,y22],[x23,y23],...],
                [[x31,y31],[x32,y32],[x33,y33],...],
                ...
               ]
        (First index is  number of datarow,
         second index is index of value of datarow.
         The Number of Values per datarow may vary.)
        legend     ... values for the Legend
                    should be is defined as:
                    legend = ['Name_Datarow_1', 'Name_Datarow_2', ...] || None
        colnames   ... names of the Datacolumns
                    sould be defined as:
                    colnames = ['Name_Column_1', 'Name_Column_2', ...] || None
        errortext  ... textual description of occured error during getting
                    data or None if no error
        title      ... title of the Diagram
        stylesheet ... name/path of stylesheet to be used for rednering the
                    diagram on client
        otherParams... dictionary which must contain the following keys
                    width      ... width of image
                    height     ... height of image
                    gridlines  ... number of gridlines
                    intcaption ... 0->float caption on axis
                                   1->int caption
                    fillgaps   ... 0->use data as is
                                   1->fill out missing values data source col
                                      (must be integer!)
        """

    def compute():
        """Compute the Diagram."""

    def registration():
        """Tells which DiagramTypes this DiagramKind is assigned to.

        This method must be a class method using following code inside class:
        registration = staticmethod(registration)

        Returns: [DiagrammKind1, DiagrammKind2, ...]
          (The names are references to classes!)
        """
        
    def setSpecialAttrib(value):
        """Set the value of the special attribute.

        No tests are done here, do them in compute.
        """

    def description():
        """Description of the abilities of the DiagramKind.

        This method must be a class method!
        Use following code inside class:
        description = staticmethod(description)

        Return: list of strings describing DiagramKind. each string is for one
                  paragraph.
        """



class IDefaultDiagramKind(IDiagramKind):
    """MarkerInterface for default DiagramKind."""



class ISVGConverter(Interface):
    """Interface for Classes which convert DataFormats."""


    def getDestinationFormat():
        """Return the mine type of the DestinationFormat the Converter produces.
        static method!
        """

    def setHTTPHeaders(response, filename):
        """Set the necessary HTTP-Headers on response (e.g. mime type).

        response: REQUEST.RESPONSE
        filename: string ... name of the file without extension
        """

    def setSourceData(sourceData):
        """Put the data for conversion into the Class.

        Parameter:
          inputData: string which is to convert."""


    def getStyleSheetURL(obj):
        """Compute the URL of the Stylesheet.

        Necessary because of problems on conversion which environments where
        authentification is necessary.
        
        Parameter:
          obj: the stylesheet object wraped into context
        Returns:
          URL or path of stylesheet
        """

    def convert():
        """Do the conversion from source to destination format.

        Returns boolean value telling if conversion was successful.
        """

    def getErrorResult():
        """Return data(in destination format) describing error, if conversion unsuccessful."""

    def getResultData():
        """Returns the result data after the conversion."""

    def getHTML(url, height, width):
        """Returns a string to integrate result into HTML.

        static method!
        
        Parameters:
          url:    string containing the url (absolute or relative) to the result
          heigth: height of the image
          width:  width of the image
          """


class IDataSource(Interface):
    """Interface for DataSources (Database, Python, ...)."""

    name = Attribute("Name of the DataSource.")
        



class IInputConverter(Interface):
    """Interface for InputConverters.
    
    InputConverters work as filters, they do not store data in itself.
    """

    name = Attribute ("Name of the InputConverter.")

    def registration():
        """Tells which DiagramTypes and DataSources this Converter serves.

        Returns: {DiagrammKind1:[DataSource1, DataSource2, ...],
                  DiagrammKind2:[DataSource3, ...]}
          (The names are references to classes!)
        """

    def convert(data, fixColumn):
        """Converts data to SVGrafZ input format.

        data ... data to convert, type depending on converter
        fixColumn ... string or None: column on which are the other values
           depending
        Return:    list fitting to SVGrafZ input format.
        Exception RuntimeError with error-text if an error occured
        """

    def description():
        """Description of the abilities of the InputConverter.

        Return: list of strings describing InputConverter. each string is for
                  one paragraph.
        """

class IInputConverterWithLegend(IInputConverter):
    """InputConverter which is able to generate the legend from its input
       data.
    """

    def legend():
        """Returns the legend extracted out of the input data using
           self.convert."""
        

class IDefaultInputConverter(IInputConverter):
    """MarkerInterface to telling that the implementing class is the
    DefaultInputConverter.
    
    There should only be one.
    """
