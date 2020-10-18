# -*- coding: utf-8 -*-
"""
/***************************************************************************
 4_Thematic_Template
                                 A QGIS plugin
 Load predefined Template
                             -------------------
        begin                : 2017-11-03
        copyright            : (C) 2017 by LuV
        email                : luc.verelst@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MRDS_ThematicTemplate class from file thematic_template.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .thematic_template import MRDS_ThematicTemplate
    return MRDS_ThematicTemplate(iface)
