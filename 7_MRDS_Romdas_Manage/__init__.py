# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_Romdas_Manage
                                 A QGIS plugin
 Romdas: Manage and Display
                             -------------------
        begin                : 2018-03-08
        copyright            : (C) 2018 by LV
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
    """Load MRDS_Romdas_Manage class from file MRDS_Romdas_Manage.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mrdsRomdasManage import MRDS_Romdas_Manage
    return MRDS_Romdas_Manage(iface)
