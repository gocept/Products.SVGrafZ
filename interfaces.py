################################################################################
## 
## SVGrafZ: Interfaces
## Version: $Id: interfaces.py,v 1.6 2003/05/23 12:43:18 mac Exp $
##
################################################################################

from Interface import Interface,Attribute

class IDiagramType(Interface):
    """Interface for DiagramTypes."""

    name = Attribute("Get the Name of the DiagramType.")
        



class IDiagramKind(Interface):
    """Interface for DiagramKinds."""

    name = Attribute ("Get the Name of the DiagramKind.")

    def __init__(data=None,
                 width=None,
                 height=None,
                 gridlines=None,
                 legend=None,
                 colnames=None,
                 title=None,
                 stylesheet=None):
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

        width, height ... width, height of image
        gridlines     ... number of gridlines
        legend        ... values for the Legend
                    should be is defined as:
                    legend = ['Name_Datarow_1', 'Name_Datarow_2', ...] || None
        colnames      ... names of the Datacolumns
                    sould be defined as:
                    colnames = ['Name_Column_1', 'Name_Column_2', ...] || None
        """

    def compute():
        """Compute the Diagram."""
    



class IDiagramKindDefault(IDiagramKind):
    """MarkerInterface for DefaultDiagramKinds."""


    
class ISVGConverter(Interface):
    """Interface for Classes which convert DataFormats."""


    def getDestinationFormat():
        """Return the mine type of the DestinationFormat the Converter produces.
        static method!
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

