# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: FormatConverters
## Version: $Id: svgconverters.py,v 1.20 2005/02/16 09:06:52 mac Exp $
##
################################################################################

# python imports
import os
import os.path
from tempfile import mktemp

from telnetlib import Telnet
import socket
from urllib import quote

import Queue
from thread import start_new_thread
from time import sleep


# sibling imports
from Products.SVGrafZ.interfaces import ISVGConverter
from Products.SVGrafZ import config

unlink_queue = Queue.Queue(0)

def unlinker(queue):
    while 1:
        try:
            x, times = queue.get()
        except Exception, m:
            sleep(1)
            continue
        try:
            os.unlink(x)
        except Exception, m:
            if times < 20:
                queue.put((x, times+1))
        sleep(1)

start_new_thread(unlinker, (unlink_queue,))

class SVG2xxx:
    """Abstract base class for converters."""

    def getSourceFormat():
        """Return the mine type of the SourceFormat the Converter can handle."""
        return 'image/svg+xml'
    getSourceFormat = staticmethod(getSourceFormat)

    def setSourceData(self, sourceData):
        """Put the data for conversion into the Class.

        Parameter:
          inputData: string which is to convert."""
        self.source = sourceData

    def getResultData(self):
        """Returns the result data after the conversion."""
        return self.result

    def setHTTPHeaders(self, response, filename):
        """Set the necessary HTTP-Headers on response (e.g. mime type)."""
        response.setHeader('Content-Type',
                           self.getDestinationFormat())


class SVG2SVG (SVG2xxx):
    """Convert SVG2SVG, so it's a dummy converter."""
    
    __implements__ = ISVGConverter

    def __init__(self):
        """Init."""
        pass

    def getDestinationFormat():
        "Return the mine type of the DestinationFormat the Converter produces."
        return 'image/svg+xml'
    getDestinationFormat = staticmethod(getDestinationFormat)


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
    
    def getHTML(url, height, width):
        """Returns a string to integrate result into HTML.

        static method!
        
        Parameters:
          url: string containing the url (absolute or relative) to the result
          heigth: height of the image
          width:  width of the image
          """
        return u'<object type="%s" width="%s" height="%s" data="%s">%s</object>'\
               %(SVG2SVG.getDestinationFormat(),
                 width,
                 height,
                 url,
                 config.SVGrafZ_SVG_not_supported)
    getHTML = staticmethod(getHTML)


class SVG2Batik (SVG2xxx):
    """Convert SVG to other formats using batik from http://xml.apache.org/batik
       or batikServer from
       http://cvs.gocept.com/cgi-bin/viewcvs/viewcvs.cgi/batikServer/"""
    
    error_text = ''
    error_file = None # name of file displayed in error-case

    def __init__(self):
        """Init."""
        self.stylesheetPath = None

        try:
            a = config.SVGrafZ_Java_Path
            a = config.SVGrafZ_Batik_Path
            a = config.SVGrafZ_BatikServer_Host
            a = config.SVGrafZ_BatikServer_Port
        except (NameError):
            self.error_text = 'Java or Batik-Path not set in config.py. \
            Please talk to your Administrator.'


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
        
        return os.path.basename(self.stylesheetPath)

    def convert(self):
        """Do the conversion from source to destination format.

        Returns boolean value telling if conversion was successful.
        """
        ret = False
        if self.error_text:
            return ret
        
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
            conn = Telnet(config.SVGrafZ_BatikServer_Host, config.SVGrafZ_BatikServer_Port)
            cmd = 'CONF %s TO %s AS %s BSP 1.0\n\n' % (
                quote(sourceFile),
                quote(resultFile),
                self.getDestinationFormat()
                )
            conn.write(cmd)
            if conn.read_all():
                ret = True
            conn.close()
        except Exception: # no batikServer, use batikRenderer
            cmd = config.SVGrafZ_Java_Path + \
                  ' -Djava.awt.headless=true -jar ' + \
                  config.SVGrafZ_Batik_Path + \
                  ' -d ' + resultFile + \
                  ' -m ' + self.getDestinationFormat() + \
                  ' ' + sourceFile
            pfh = os.popen(cmd)
            res = pfh.read()
            if res[-8:-1] == 'success':
                ret = True
                
        # read result
        if ret:
            rfh = open(resultFile, 'rb')
            self.result = rfh.read()
            rfh.close()

        # cleaning up
        if self.stylesheetPath:     # XXX this can fail badly on windows
            unlink_queue.put((self.stylesheetPath, 0))
        unlink_queue.put((sourceFile, 0))
        unlink_queue.put((resultFile, 0))
        return ret

    def getErrorResult(self):
        """Return data(in destination format) describing error, if conversion unsuccessful."""
        erp = os.path.join(os.path.join(os.path.dirname(__file__), 'www'),
                        self.error_file)
        efh = open(erp, 'rb')
        errorResult = efh.read()
        efh.close()
        return errorResult



class SVG2PNG (SVG2Batik):
    """Convert SVG to PNG."""
    
    __implements__ = ISVGConverter

    error_file = 'error.png' # name of file displayed in error-case

    def getDestinationFormat():
        "Return the mine type of the DestinationFormat the Converter produces."
        return 'image/png'
    getDestinationFormat = staticmethod(getDestinationFormat)

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



class SVG2PDF (SVG2Batik):
    """Convert SVG to PDF."""
    
    __implements__ = ISVGConverter

    error_file = 'error.pdf' # name of file displayed in error-case
    file_extension = '.pdf'

    def getDestinationFormat():
        "Return the mine type of the DestinationFormat the Converter produces."
        return 'application/pdf'
    getDestinationFormat = staticmethod(getDestinationFormat)

    def setHTTPHeaders(self, response, filename):
        """Set the necessary HTTP-Headers on response (e.g. mime type)."""
        response.setHeader('Content-Type',
                           '%s; name=%s%s'% (self.getDestinationFormat(),
                                             filename,
                                             self.file_extension))
        response.setHeader('Content-Disposition',
                           'attachment; filename=%s%s' % (filename,
                                                          self.file_extension))


    def getHTML(url, height, width):
        """Returns a string to integrate result into HTML.

        static method!
        
        Parameters:
          url: string containing the url (absolute or relative) to the result
          heigth: height of the image
          width:  width of the image
        """
        return u'<object type="%s" width="%s" height="%s" data="%s">\
        <a href="%s">%s</a></object>' % (
            SVG2PDF.getDestinationFormat(),
            width,
            height,
            url,
            url,
            config.SVGrafZ_download_PDF)
    getHTML = staticmethod(getHTML)
