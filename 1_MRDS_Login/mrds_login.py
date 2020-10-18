from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
import resources
import os

from qgis.core import *
from qgis.gui import *

from functions import *
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal

# Import the code for the dialog
from mrds_logindialog import MRDS_LoginDialog

class MRDS_Login:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        #Create the dialog and keep reference
        self.dlg = MRDS_LoginDialog()
        #self.dlg.pushButton.clicked.connect(self.showAboutBox)
        self.dlg.btnAbout.clicked.connect(self.showAboutBox)
        self.dlg.btnConnect.clicked.connect(self.showConnectRDS)

        self.RAMSusername = ''
        self.RAMSpassword = ''
        self.RAMSserver = ''

    def initGui(self):

        # self.dlg.editUser.setText("mrams")
        # self.dlg.editPassword.setText("mrams")
        # self.dlg.editServer.setText("localhost")

        #define action
        icon = QIcon(":/plugins/1_MRDS_Login/connect.png")
        self.action = QAction(icon,"M-RAMS Login", self.iface.mainWindow())
        self.action.setWhatsThis("Login to the Myanmar RAMS")
        self.action.setStatusTip("Login to the Myanmar RAMS")
        self.action.triggered.connect(self.run)
        #QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        #add MRDS Menu
        ##https://gis.stackexchange.com/questions/136267/adding-new-menu-item-to-qgis-desktop-app
        ##https://gis.stackexchange.com/questions/169869/adding-multiple-plugins-to-custom-menu-in-qgis/169880#169880
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        if not self.menu:
            self.menu = QMenu("&Myanmar RAMS", self.iface.mainWindow().menuBar())
            self.menu.setObjectName('&Myanmar RAMS')
            actions = self.iface.mainWindow().menuBar().actions()
            ##g a menu to the second to last position of the menu bar,right before the Help menu.
            lastAction = actions[-1]
            self.iface.mainWindow().menuBar().insertMenu(lastAction,self.menu)
        self.menu.addAction(self.action)

        #add MRDS Toolbar
        ##https://gis.stackexchange.com/questions/217389/how-to-group-my-plugins-in-qgis-menu-and-toolbar/217392
        ##https://gis.stackexchange.com/questions/30886/adding-toolbar-via-pyqgis

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS' )
        if not self.toolbar:
            self.toolbar = self.iface.addToolBar('&Myanmar RAMS')      ##QToolbar("&Myanmar RDS", self.iface.mainWindow().toolBar())
            self.toolbar.setObjectName('&Myanmar RAMS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)
        #self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        self.menu.removeAction(self.action)
        #self.menu.clear() -->removes all menu items
        #self.iface.removePluginMenu("RDS Login", self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # create and show the ZoomToPoint dialog
        #dlg = MRDS_LoginDialog()

        #set login
        self.mrdlogin = LoadLogin()
        self.RAMSusername = self.mrdlogin.getLoginUser()
        self.RAMSpassword = self.mrdlogin.getLoginPwd()
        self.RAMSserver = self.mrdlogin.getLoginServer()

        self.dlg.editUser.setText( self.RAMSusername)
        self.dlg.editPassword.setText(self.RAMSpassword)
        self.dlg.editServer.setText(self.RAMSserver)

        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            QMessageBox.information(self.iface.mainWindow(), "QGIS","Passed")
	    pass

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.txt')
        self.dlg.lineEdit.setText(filename)

    def showAboutBox(self):
        #hide the main dialog, otherwise it disappears under the main window
        self.dlg.hide()
        s = """ "About Myanmar Road Asset Management System...\n
            Integration of ROMDAS, Open Streetmap, SROMP Road Network layers.\n
            Version 1.1 \n
            ADB-TA 8987 - July 2018.
            """
        QMessageBox.information(self.iface.mainWindow(), "About Myanmar RAMS", s)
        self.dlg.show()


    def showConnectRDS(self):
        #self.dlg.hide()
        #QMessageBox.information(self.iface.mainWindow(), "111 About Myanmar RDS", str(self.username) + "-" + str(self.password))
        self.RAMSusername = self.dlg.editUser.text().strip()
        self.RAMSpassword = self.dlg.editPassword.text().strip()
        self.RAMSserver = self.dlg.editServer.text().strip()

        #QMessageBox.information(self.iface.mainWindow(), "2222 About Myanmar RDS", (self.username) + "-" + (self.password))

        if str(self.RAMSusername)<>"" and str(self.RAMSpassword)<> "" : # and (self.username <> None) and (self.password <> None) :
            #QMessageBox.information(self.iface.mainWindow(), "333 About Myanmar RDS", str(self.username) + "-" + str(self.password))
            ##https://gis.stackexchange.com/questions/86983/how-to-properly-establish-a-postgresql-connection-using-qgscredentials
            #establish a postgis connection
            uri = QgsDataSourceURI()
            # assign this information before you query the QgsCredentials data store
            uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword, 2);
            uri.setDataSource("public", "mimu_national", "geom", "")
            layer = QgsVectorLayer(uri.uri(), "Myanmar Boundary", "postgres")

            if self.dlg.chkRemoveLayers.isChecked():
                QgsMapLayerRegistry.instance().removeAllMapLayers()


            if self.dlg.chkAddLayer.isChecked():
                #set polygon sybology
                myRenderer  = layer.rendererV2()
                if layer.geometryType() == QGis.Polygon:
                    mySymbol1 = QgsFillSymbolV2.createSimple({'color':'#969696',
                                                              'color_border':'#969696',
                                                              'width_border':'0.2'})

                    myRenderer.setSymbol(mySymbol1)
                    #layer.triggerRepaint()

                    #Just to be safe, make sure everything works:
                    if not layer.isValid():
                        QMessageBox.information(self.iface.mainWindow(), "M-RDS",  "Layer %s did not load" % layer.name(),QMessageBox.Ok)
                    #Finally, add the layer to the map if everything is okay:
                    QgsMapLayerRegistry.instance().addMapLayers([layer])
            self.mrdlogin.setLogin(self.RAMSusername,self.RAMSpassword, self.RAMSserver)
            self.dlg.close()
        else:
            QMessageBox.information(self.iface.mainWindow(),"RDS", "You must enter username and password", QMessageBox.Ok)
        #self.dlg.show()