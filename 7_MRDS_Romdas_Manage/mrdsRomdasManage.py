# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_Romdas_Manage
                                 A QGIS plugin
 Romdas: Manage and Display
                              -------------------
        begin                : 2018-03-08
        git sha              : $Format:%H$
        copyright            : (C) 2018 by LV
        email                : luc.verelst@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mrdsRomdasManage_dialog import MRDS_Romdas_ManageDialog
import os.path
from PyQt4 import uic
import subprocess


class MRDS_Romdas_Manage:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.dlg = MRDS_Romdas_ManageDialog()

        self.dlg.btnRebuildLRS.clicked.connect(self.rebuildLRS)
        self.dlg.btnRoadIdentifier.clicked.connect(self.roadIdentifier)
        self.dlg.btnRoadAssets.clicked.connect(self.roadAssets)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon = QIcon(':/plugins/7_MRDS_Romdas_Manage/icon.png')
        self.action = QAction(icon,"ROMDAS Manage & Display", self.iface.mainWindow())
        self.action.triggered.connect(self.run)


        #add MRDS Menu
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RDS' )
        if not self.menu:
            self.menu = QMenu("&Myanmar RDS", self.iface.mainWindow().menuBar())
            self.menu.setObjectName('&Myanmar RDS')
            actions = self.iface.mainWindow().menuBar().actions()
            ##g a menu to the second to last position of the menu bar,right before the Help menu.
            lastAction = actions[-1]
            self.iface.mainWindow().menuBar().insertMenu(lastAction,self.menu)
        self.menu.addAction(self.action)

        #add MRDS Toolbar
        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RDS' )
        if not self.toolbar:
            self.toolbar = self.iface.addToolBar('&Myanmar RDS')      ##QToolbar("&Myanmar RDS", self.iface.mainWindow().toolBar())
            self.toolbar.setObjectName('&Myanmar RDS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RDS' )
        self.menu.removeAction(self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RDS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass


    def rebuildLRS(self):
##     dqote = '"'
##     FNULL = open(os.devnull, 'w')
##
##     dos_command = 'notepad.exe d:/r ams.txt'#  + dqote + ' d:/rams.txt' + dqote
##     QMessageBox.information(self.iface.mainWindow(), "M-RDS", dos_command,QMessageBox.Ok)
##     subprocess.call(dos_command, stdout=FNULL, stderr=FNULL, shell=False)

        #fname = 'D:/_QGIS/__Tutorial/ROMDAS/Magway-Kanbya Rd.mdb'
        fname = 'D:/aa/Magway-Kanbya Rd.mdb'
        basepath = os.path.dirname(os.path.realpath(__file__))

        #run executable to extract CSV from MDB
        dqote = '"'
        FNULL = open(os.devnull, 'w')
        dos_command = basepath +'/extract.exe '  + dqote + fname + dqote
        #dos_command = basepath +'/extract.exe '  + fname
        #dos_command = 'notepad.exe d:/r ams.txt'#  + dqote + ' d:/rams.txt' + dqote
        QMessageBox.information(self.iface.mainWindow(), "M-RDS", dos_command,QMessageBox.Ok)
        subprocess.call(dos_command, stdout=FNULL, stderr=FNULL, shell=False)          #blocks further running of the python



        return

    def roadIdentifier(self):
        return

    def roadAssets(self):
        return


