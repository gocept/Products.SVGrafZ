################################################################################
## 
## SVGrafZ: FormatConverters
## Version: $Id: svgconverters.py,v 1.4 2003/06/17 09:42:43 mac Exp $
##
################################################################################

from os import popen, unlink, path
from tempfile import mktemp
from telnetlib import Telnet
import socket
from urllib import quote

from interfaces import ISVGConverter
from config import SVGrafZ_Java_Path, SVGrafZ_Batik_Path
from config import SVGrafZ_BatikServer_Host, SVGrafZ_BatikServer_Port


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
    """Convert SVG to PNG, using batik from http://xml.apache.org/batik/.
       or batikServer from
       http://cvs.gocept.com/cgi-bin/viewcvs/viewcvs.cgi/batikServer/"""
    
    __implements__ = ISVGConverter

    error_text = ''

    def __init__(self):
        """Init."""
        global SVGrafZ_Java_Path, SVGrafZ_Batik_Path
        global SVGrafZ_BatikServer_Host, SVGrafZ_BatikServer_Port

        try:
            a = SVGrafZ_Java_Path
            a = SVGrafZ_Batik_Path
            a = SVGrafZ_BatikServer_Host
            a = SVGrafZ_BatikServer_Port
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
        self.stylesheetPath = mktemp('SVGrafZ.css')
        sfh = open(self.stylesheetPath, 'w')
        sfh.write(str(obj))
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
        global SVGrafZ_BatikServer_Host, SVGrafZ_BatikServer_Port
        
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

        # try connection to batikServer
        try:
            conn = Telnet(SVGrafZ_BatikServer_Host, SVGrafZ_BatikServer_Port)
            cmd = 'CONF %s TO %s AS %s BSP 1.0\n\n' % (
                quote(sourceFile),
                quote(resultFile),
                self.getDestinationFormat()
                )
            conn.write(cmd)
            if conn.read_all():
                ret = True
            conn.close()
        except (socket.error): # no batikServer, use batikRenderer
            cmd = SVGrafZ_Java_Path + \
                  ' -jar ' + \
                  SVGrafZ_Batik_Path + \
                  ' -d ' + resultFile + \
                  ' -m ' + self.getDestinationFormat() + \
                  ' ' + sourceFile
            pfh = popen(cmd)
            res = pfh.read()
            if res[-8:-1] == 'success':
                ret = True
                
        # read result
        if ret:
            rfh = open(resultFile, 'r')
            self.result = rfh.read()
            rfh.close()

        # cleaning up
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
