# -*- coding: latin1 -*-
################################################################################
## 
## SVGrafZ: Configure File
##
## $Id$
################################################################################

# explanation of the variable meanings see customconfig.py.*

SVGrafZ_default_Color = u"lightgreen"
SVGrafZ_legend_name = u"Legende:"
SVGrafZ_empty_dataset = u"Keine Daten! Also kann nichts dargestellt werden."
SVGrafZ_SVG_not_supported = u"Ihr Browser unterstützt leider nicht die Anzeige "\
                            u"von SVG-Grafiken."
SVGrafZ_error_name = u"Fehler"
SVGrafZ_download_PDF = u"PDF-Dokument herunterladen"

SVGrafZ_BatikServer_Host = u"localhost"
SVGrafZ_BatikServer_Port = 54822

SVGrafZ_Java_Path = u"set by customconfig.py"
SVGrafZ_Batik_Path = u"set by customconfig.py"

try:
    from Products.SVGrafZ.customconfig import *
except ImportError:
    pass

