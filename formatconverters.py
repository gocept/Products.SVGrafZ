################################################################################
## 
## SVGrafZ: FormatConverters
## Version: $Id: formatconverters.py,v 1.1 2003/05/22 14:22:21 mac Exp $
##
################################################################################

from interfaces import IDataFormatConverter



class SVG2SVG:
    """Convert SVG2SVG, so it's a dummy converter."""
    
    __implements__ = IDataFormatConverter

    def __init__(self):
        """Init."""
        pass

    def getSourceFormat():
        """Return the mine type of the SourceFormat the Converter can handle."""
        return 'image/svg+xml'

    getSourceFormat = staticmethod(getSourceFormat)

    def getDestinationFormat():
        """Return the mine type of the DestinationFormat the Converter produces."""
        return 'image/svg+xml'

    getDestinationFormat = staticmethod(getDestinationFormat)

    def setSourceData(self, sourceData):
        """Put the data for conversion into the Class.

        Parameter:
          inputData: string which is to convert."""
        self.source = sourceData

    def convert(self):
        """Do the conversion from source to destination format.

        Returns boolean value telling if conversion was successful.
        """
        self.result = self.source
        return True

    def getErrorResult(self):
        """Return data(in destination format) describing error, if conversion unsuccessful."""
        return 'There will be no error!' # there will be no error

    def getResultData(self):
        """Returns the result data after the conversion."""
        return self.result

    def getHTML(url, height, width):
        """Returns a string to integrate result into HTML.

        static method!
        
        Parameters:
          url: string containing the url (absolute or relative) to the result
          heigth: height of the image
          width:  width of the image
          """
        return u'<object type="image/svg+xml" width="%s" height="%s" data="%s">\
        Ihr Browser unterstützt keine SVG-Grafiken. \
        Wenden Sie sich an Ihren Administor, um Unterstützung für SVG-Grafiken \
        zu bekommen bzw. auf PNG-Grafiken umzustellen.</object>' % (
            width, height, url)

    getHTML = staticmethod(getHTML)
