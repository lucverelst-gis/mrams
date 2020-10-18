# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_RoadSymbology
                                 A QGIS plugin
 Create Road maps from attributes
                             -------------------
        begin                : 2017-10-31
        copyright            : (C) 2017 by LV
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
    """Load MRDS_RoadSymbology class from file MRDS_RoadSymbology.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mrds_romdas import MRDS_Romdas
    return MRDS_Romdas(iface)
