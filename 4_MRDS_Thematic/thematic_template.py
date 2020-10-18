# -*- coding: utf-8 -*-
"""
/***************************************************************************
 4_Thematic_Template
                                 A QGIS plugin
 Load predefined Template
                              -------------------
        begin                : 2017-11-03
        git sha              : $Format:%H$
        copyright            : (C) 2017 by LuV
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
from qgis.core import *
# Import the code for the dialog
from thematic_template_dialog import MRDS_ThematicDialog
import os.path


def resolve(name, basepath=None):
    if not basepath:
        basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, name)

class MRDS_ThematicTemplate:
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
        #Create the dialog and keep reference
        self.dlg = MRDS_ThematicDialog()

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #define action
        icon = QIcon(":/plugins/4_Thematic_Template/icon.png")
        self.action = QAction(icon,u'&Thematic Templates', self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        #add MRDS Menu
        ##https://gis.stackexchange.com/questions/136267/adding-new-menu-item-to-qgis-desktop-app
        ##https://gis.stackexchange.com/questions/169869/adding-multiple-plugins-to-custom-menu-in-qgis/169880#169880
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        if not self.menu:
            self.menu = QMenu("&Myanmar RAMS", self.iface.mainWindow().menuBar())
            self.menu.setObjectName(u'&Thematic Templates')
            actions = self.iface.mainWindow().menuBar().actions()
            ##g a menu to the second to last position of the menu bar,right before the Help menu.
            lastAction = actions[-1]
            self.iface.mainWindow().menuBar().insertMenu(lastAction,self.menu)
        self.menu.addAction(self.action)

        #add MRDS Toolbar
        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS' )
        if not self.toolbar:
            self.toolbar = self.iface.addToolBar('&Myanmar RAMS')      ##QToolbar("&Myanmar RDS", self.iface.mainWindow().toolBar())
            self.toolbar.setObjectName('&Myanmar RAMS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        self.menu.removeAction(self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)

    def load_project(self, fname):
        ###https://stackoverflow.com/questions/43573726/how-to-load-a-project-into-qgis-with-pyqgiss
        project = QgsProject.instance()
        project.read(QFileInfo(fname))
        self.iface.mainWindow().setWindowTitle(fname)
        ###print project.fileName()

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        mapNr=0

        #fname = QgsApplication.pluginPath() + '\\1_MRAMS_Generic.qgs'
        fname = resolve('1_MRAMS_Generic.qgs')
        if self.dlg.radioTemplate2.isChecked():
            mapNr=1
            fname = resolve('2_HillShade_Template.qgs')
        if self.dlg.radioTemplate3.isChecked():
            mapNr=2
            fname = resolve('3_Google_Maps_Style.qgs')
        if self.dlg.radioTemplate4.isChecked():
            mapNr=3
            fname = resolve('4_Street_with_labeling_Local.qgs')

        #QMessageBox.information(self.iface.mainWindow(), "M-RDS",fname ,QMessageBox.Ok)
        #canvas = self.iface.mapCanvas()

        # See if OK was pressed
        if result:
            self.load_project(fname)
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
