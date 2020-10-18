# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_Query
                                 A QGIS plugin
 Query and reporting
                             -------------------
        begin                : 2017-10-25
        copyright            : (C) 2017 by luv
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
    """Load MRDS_Query class from file MRDS_Query.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mrds_query import MRDS_Query
    return MRDS_Query(iface)
