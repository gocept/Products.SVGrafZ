# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: Configure File
##
## $Id: config.py,v 1.14 2005/02/16 07:43:55 mac Exp $
################################################################################


### global SVGrafZ options ###

## default color for the graph curves. used when no stylesheet is given.
SVGrafZ_default_Color = 'lightgreen'

## name of 'legend' in local language
# deutsch (German)
SVGrafZ_legend_name = 'Legende:'
# English
#SVGrafZ_legend_name = 'Legend:'

## error text, if dataset is empty
# deutsch (German)
SVGrafZ_empty_dataset = 'Keine Daten! Also kann nichts dargestellt werden.'
# English
#SVGrafZ_empty_dataset = "No data, so I can not display anything."

## error text, if SVG images are not supported by browser
# deutsch (German)
SVGrafZ_SVG_not_supported = u"Es können bei Ihnen keine SVG-Grafiken darstellt werden. Bitte stellen Sie im Modul 'Voreinstellungen' unter 'Diagrammdarstellung' auf PNG-Grafiken um oder wenden Sie sich an Ihren Administrator, um entsprechende Software installieren zu lassen, so dass SVG-Grafiken dargestellt werden können."
# English
# SVGrafZ_SVG_not_supported = "Your Browser does not support SVG images. Please contact your Administrator."

## word 'error' in local language
# deutsch (German)
SVGrafZ_error_name = 'Fehler'
# English
#SVGrafZ_error_name = 'Error'

## text for link to download PDF-File
# deutsch (German)
SVGrafZ_download_PDF = "PDF-Datei herunterladen"
# English
#SVGrafZ_download_PDF = "download PDF file"


#### either you use batikServer or batikRasterizer
#### batikServer is about 3 times faster than batikRasterizer

### batikServer -- you should also configure batikRasterizer as fallback
## batikServer - host name
SVGrafZ_BatikServer_Host = 'localhost'
## batikServer - port number
SVGrafZ_BatikServer_Port = 54822
## If you want to start Batikserver when you start Zope enter here the
## classpath to your batikServer.class file.
SVGrafZ_BatikServer = '/home/mac/bin/'

### batikRasterizer
## batikRasterizer - absolute Path to Java 1.3+ interpreter binary
SVGrafZ_Java_Path = '/usr/bin/java'
## absolute Path to batik-rasterizer jar-file (version 1.5beta5 or higher)
SVGrafZ_Batik_Path = '/usr/share/java/batik.jar:/usr/share/java/xerces.jar:/usr/share/java/fop.jar'

