################################################################################
## 
## SVGrafZ: Configure File
##
## $Id: config.py,v 1.4 2003/06/17 09:42:43 mac Exp $
################################################################################

#### either you use batikServer or batikRasterizer
#### batikServer is about 3 times faster than batikRasterizer

### batikServer -- you should also configure batikRasterizer as fallback
## batikServer - host name
SVGrafZ_BatikServer_Host = 'localhost'
## batikServer - port number
SVGrafZ_BatikServer_Port = 54822


### batikRasterizer
## batikRasterizer - absolute Path to Java 1.3+ interpreter binary
SVGrafZ_Java_Path = '/usr/bin/java'
## absolute Path to batik-rasterizer jar-file (version 1.5beta5 or higher)
SVGrafZ_Batik_Path = '/home/mac/data/pkg/batik-1.5/batik-rasterizer.jar'


## default color for the graph curves. used when no stylesheet is given.
SVGrafZ_default_Color = 'lightgreen'

## name of 'legend' in local language
SVGrafZ_legend_name = 'Legende:'
