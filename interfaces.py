################################################################################
## 
## SVGrafZ: Interfaces
## Version: $Id: interfaces.py,v 1.3 2003/04/10 13:58:50 mac Exp $
##
################################################################################

from Interface import Interface,Attribute

class IDiagramType(Interface):
    """Interface for DiagramTypes."""

    name = Attribute("Get the Name of the DiagramType.")
        



class IDiagramKind(Interface):
    """Interface for DiagramKinds."""

    name = Attribute ("Get the Name of the DiagramKind.")

    def __init__(data, width, height, gridlines, legend, colnames):
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


    
