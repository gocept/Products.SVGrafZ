################################################################################
## 
## SVGrafZ: FormatConverters
## Version: $Id: svgconverters.py,v 1.2 2003/05/23 12:47:55 mac Exp $
##
################################################################################

from os import popen, unlink, path
from tempfile import mktemp

from interfaces import ISVGConverter
from config import SVGrafZ_Java_Path, SVGrafZ_Batik_Path


class SVG2SVG:
    """Convert SVG2SVG, so it's a dummy converter."""
    
    __implements__ = ISVGConverter

    def __init__(self):
        """Init."""
        pass

    def getSourceFormat():
        """Return the mine type of the SourceFormat the Converter can handle."""
        return 'image/svg+xml'

    getSourceFormat = staticmethod(getSourceFormat)

    def getDestinationFormat():
        "Return the mine type of the DestinationFormat the Converter produces."
        return 'image/svg+xml'

    getDestinationFormat = staticmethod(getDestinationFormat)

    def setSourceData(self, sourceData):
        """Put the data for conversion into the Class.

        Parameter:
          inputData: string which is to convert."""
        self.source = sourceData

    def getStyleSheetURL(self, obj):
        """Compute the URL of the Stylesheet.

        Necessary because of problems on conversion which environments where
        authentification is necessary.
        
        Parameter:
          obj: the stylesheet object wraped into context
        Returns:
          URL or path of stylesheet
        """
        return obj.absolute_url()

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
        return u'<object type="%s" width="%s" height="%s" data="%s">\
        Ihr Browser unterstützt keine SVG-Grafiken. \
        Wenden Sie sich an Ihren Administor, um Unterstützung für SVG-Grafiken \
        zu bekommen bzw. auf PNG-Grafiken umzustellen.</object>' % (
            SVG2SVG.getDestinationFormat(), width, height, url)
    getHTML = staticmethod(getHTML)




class SVG2PNG:
    """Convert SVG to PNG, using batik from http://xml.apache.org/batik/."""
    
    __implements__ = ISVGConverter

    error_text = ''

    def __init__(self):
        """Init."""
        global SVGrafZ_Java_Path, SVGrafZ_Batik_Path

        try:
            a = SVGrafZ_Java_Path
            a = SVGrafZ_Batik_Path
        except (NameError):
            self.error_text = 'Java or Batik-Path not set in config.py. \
            Please talk to your Administrator.'
        

    def getSourceFormat():
        """Return the mine type of the SourceFormat the Converter can handle."""
        return 'image/svg+xml'
    getSourceFormat = staticmethod(getSourceFormat)


    def getDestinationFormat():
        "Return the mine type of the DestinationFormat the Converter produces."
        return 'image/png'
    getDestinationFormat = staticmethod(getDestinationFormat)


    def setSourceData(self, sourceData):
        """Put the data for conversion into the Class.

        Parameter:
          inputData: string which is to convert."""
        self.source = sourceData


    def getStyleSheetURL(self, obj):
        """Compute the URL of the Stylesheet.

        Necessary because of problems on conversion which environments where
        authentification is necessary.
        
        Parameter:
          obj: the stylesheet object wraped into context
        Returns:
          URL or path of stylesheet
        """
        self.stylesheetPath = mktemp('SVGrafZ')
        sfh = open(self.stylesheetPath, 'w')
        sfh.write(obj.__str__())
        sfh.close()
        
        return self.stylesheetPath


    def convert(self):
        """Do the conversion from source to destination format.

        Returns boolean value telling if conversion was successful.
        """
        ret = False
        if self.error_text:
            return ret

        global SVGrafZ_Java_Path, SVGrafZ_Batik_Path
        
        # write source data to tmp-file
        sourceFile = mktemp('SVGrafZ')
        sfh        = open(sourceFile, 'w')
        sfh.write(self.source)
        sfh.close()

        # create result file
        resultFile = mktemp('SVGrafZ')
        rfh        = open(resultFile, 'w')
        rfh.write('ResultFile of SVGrafZ.')
        rfh.close()

        cmd = SVGrafZ_Java_Path + \
              ' -jar ' + \
              SVGrafZ_Batik_Path + \
              ' -d ' + resultFile + \
              ' -m ' + SVG2PNG.getDestinationFormat() + \
              ' ' + sourceFile
        pfh = popen(cmd)
        res = pfh.read()
        if res[-8:-1] == 'success':
            # read result
            rfh = open(resultFile, 'r')
            self.result = rfh.read()
            rfh.close()
            ret = True

        unlink(self.stylesheetPath)
        unlink(sourceFile)
        unlink(resultFile)
        
        return ret

    def getErrorResult(self):
        """Return data(in destination format) describing error, if conversion unsuccessful."""
        erp = path.join(path.join(path.dirname(__file__), 'www'), 'error.png')
        efh = open(erp, 'r')
        errorResult = efh.read()
        efh.close()
        return errorResult

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
        return u'<img src="%s" width="%s" height="%s"/>' % (
            url, width, height)

    getHTML = staticmethod(getHTML)
