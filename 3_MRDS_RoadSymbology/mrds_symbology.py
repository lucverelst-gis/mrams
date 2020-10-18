# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_RoadSymbology
                                 A QGIS plugin
 Create Road maps from attributes
                              -------------------
        begin                : 2017-10-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by LV
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
from qgis.core import *
#from qgis.core import QgsDataSourceURI
import db_manager.db_plugins.postgis.connector as con
import psycopg2                  #Psycopg – PostgreSQL database adapter for Python —access direct with SQL.

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mrds_symbology_dialog import MRDS_RoadSymbologyDialog
import os.path
from PyQt4 import uic
 ###https://gis.stackexchange.com/questions/159397/setting-variables-on-startup-using-pyqgis
from qgis.utils import plugins



class MRDS_RoadSymbology:
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
        self.dlg = MRDS_RoadSymbologyDialog()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.dlg.btnCreate.clicked.connect(self.makeMap)

        #get variables from other plugins via instance and  from qgis.utils import plugins
        self.instance = plugins['1_MRDS_Login']
        #self.RAMSserver = "hello " + self.instance.dlg.editServer.text()
        #self.RAMSserver = self.instance.RAMSserver


    def getGlobals(self):

        #QMessageBox.information(self.iface.mainWindow(), "M-RDS", "yyy.",QMessageBox.Ok)
        success = True
        self.RAMSserver = self.instance.RAMSserver
        self.RAMSusername = self.instance.RAMSusername
        self.RAMSpassword = self.instance.RAMSpassword
        if not self.RAMSserver:
            self.RAMSserver = self.instance.dlg.editServer.text()
        if not self.RAMSusername:
            self.RAMSusername = self.instance.dlg.editUser.text()
        if not self.RAMSpassword:
            self.RAMSpassword = self.instance.dlg.editPassword.text()

        if not self.RAMSserver:
            success = False
        if not self.RAMSusername:
            success = False
        if not self.RAMSpassword:
            success = False

        if not success:
            QMessageBox.information(self.iface.mainWindow(), "M-RAMS", "You need first to connect to the RAMS database via the Login screen.",QMessageBox.Ok)

        #QMessageBox.information(self.iface.mainWindow(), "M-RDS", "Success!!." + self.RAMSserver,QMessageBox.Ok)

        return success

    def getConnSettings(self):
        #return("dbname='mrams' user='mrams' host='localhost' password='mrams'")
        return("dbname='mrams' user='" + self.RAMSusername+ "' host='" + self.RAMSserver + "' password='" + self.RAMSpassword + "'")

    def fillComponents(self):

        #action on combobox
        self.dlg.comboLayer.currentIndexChanged.connect(self.changeLayer)
        self.dlg.comboAttribute.currentIndexChanged.connect(self.changeAttribute)
        self.dlg.comboClass.currentIndexChanged.connect(self.changeClassification)

        #fill combobox and set quantile
        self.dlg.comboClass.clear()
        self.dlg.comboClass.addItems(["EqualInterval", "Quantile (Equal Count)", "Natural Breaks (Jenks)", "StdDev", "Pretty Breaks"])
        self.dlg.comboClass.setCurrentIndex(1)
        #self.classMode = 0

        #load line layers
        ###https://gis.stackexchange.com/questions/180427/retrieve-available-postgis-connections-in-pyqgis
        ### BETTER select * from geometry_columns
        ###https://gis.stackexchange.com/questions/31061/how-to-select-only-spatial-tables-from-the-postgres-database

        uri = QgsDataSourceURI()
        uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword) #database,user,pasword
        c = con.PostGisDBConnector(uri)

        #select tables to consider for mapping
        tableList = c.getTables()
        self.dlg.comboLayer.clear()
        for layer in tableList:
            if len(layer)>9 and ("road" in layer[1] or "Segment" in layer[1]) and ("geom" in layer[8]) and (layer[9]=='MULTILINESTRING' or layer[9]=='LINESTRING'):
                self.dlg.comboLayer.addItem(layer[1])



    def initGui(self):

        icon = QIcon(':/plugins/3_MRDS_RoadSymbology/icon.png')
        self.action = QAction(icon,"Road Symbology", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

		#add MRDS Menu
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
        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS' )
        if not self.toolbar:
            self.toolbar = self.iface.addToolBar('&Myanmar RAMS')
            self.toolbar.setObjectName('&Myanmar RAMS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)


    def unload(self):

        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        self.menu.removeAction(self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)


    def run(self):
        """Run method that performs all the real work"""

        if not self.getGlobals():         #read paramaters to connect to database
            return

        self.fillComponents()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    ###################################
    # function to apply graduated symbology to a layer
    ###################################
    def applyGraduatedSymbology(vectorLayer, targetField, classes, mode):

        print 'applying graduated symbology'

        # set up renderer
        symbol =  QgsLineSymbolV2()

        colorRamp = QgsVectorGradientColorRampV2.create({'color1' : '0,255,0,255',
                                                         'color2' : '255,0,0,255',
                                                         'stops' : '0.5;255,255,0,255'})

        renderer = QgsGraduatedSymbolRendererV2.createRenderer(vectorLayer, targetField, classes, classMode, symbol, colorRamp)

        vectorLayer.setRendererV2(renderer)
        return




    def makeMap(self):

        if not self.getGlobals():
            return

        #QMessageBox.information(self.iface.mainWindow(), "M-RDS", "RAMSserver = " +  self.RAMSserver,QMessageBox.Ok)
        classMode = self.dlg.comboClass.currentIndex()
        layerName =self.dlg.comboLayer.currentText()

        fieldName = self.dlg.comboAttribute.currentText()
        #-1--------------connection to PostgreSQL database
        uri = QgsDataSourceURI()
        # set host name, port, database name, username and password
        uri.setConnection( self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword, 2)
        uri.setDataSource("public", layerName, "geom", "")
        layer = QgsVectorLayer(uri.uri(), "Thema: " + layerName, "postgres")

        #Just to be safe, make sure everything works:
        if layer.isValid():
            if self.dlg.radioColorRamp.isChecked():
                layerWidth = 1.2
                color = QColor("#000000")
                symbol =  QgsLineSymbolV2()
                symbol.setWidth(layerWidth)

                colorRamp = QgsVectorGradientColorRampV2.create({'color1' : '0,255,0,255','color2' : '255,0,0,255', 'stops' : '0.5;255,255,0,255'})
                renderer = QgsGraduatedSymbolRendererV2.createRenderer(layer, fieldName, 8, classMode, symbol, colorRamp)
                layer.setRendererV2(renderer)

###https://gis.stackexchange.com/questions/76976/how-to-create-a-symbol-with-graduated-marker-size-and-line-width-in-pyqgis
###https://gis.stackexchange.com/questions/48613/how-to-apply-a-graduated-renderer-in-pyqgis
            if self.dlg.radioSize.isChecked():
                rangeList=[]

                ###get min and max value to compute range
                sql = 'SELECT min(' + fieldName + '), max(' +fieldName + ') from ' + '"'+layerName + '"'

                #QMessageBox.information(self.iface.mainWindow(), "M-RDS",  sql ,QMessageBox.Ok)
                conn = psycopg2.connect(self.getConnSettings())
                cur = conn.cursor()
                cur.execute(sql)
                for row in cur:
                    minValue = row[0]
                    maxValue = row[1]
                conn.close()
                #QMessageBox.information(self.iface.mainWindow(), "M-RDS",  'Min-Max=' + str(minValue) + ' '  + str(maxValue) ,QMessageBox.Ok)
                width = [0.01, 0.1, 0.5, 0.8, 2]
                classes = 4
                for x in range(1,classes+1):
                    symbol1 = QgsLineSymbolV2()
                    symbol1.setWidth(width[x])
                    symbol1.setColor( QColor("#000000") )
                    class_min = minValue + (maxValue-minValue) / classes * (x-1)
                    class_max = minValue + (maxValue-minValue) /classes * (x)
                    range1 = QgsRendererRangeV2(class_min, class_max, symbol1, str(class_min) +'-'+ str(class_max))
                    rangeList.append(range1)
                    #QMessageBox.information(self.iface.mainWindow(), "M-RDS",  str(x) + ': ' +str(class_min) + ' '  + str(class_max) ,QMessageBox.Ok)


                #===========

##                symbol2 = QgsLineSymbolV2()
##                symbol2.setWidth(0.5)
##                symbol2.setColor( QColor("#000000") )
##                range2 = QgsRendererRangeV2(6, 10, symbol2, "b")
##                rangeList.append(range2)
##
##                symbol3 = QgsLineSymbolV2()
##                symbol3.setWidth(0.8)
##                symbol3.setColor( QColor("#000000") )
##                range3 = QgsRendererRangeV2(11, 50, symbol3, "c")
##                rangeList.append(range3)


                renderer = QgsGraduatedSymbolRendererV2(fieldName, rangeList)
                renderer.setMode(classMode)
                #renderer.setMode( QgsGraduatedSymbolRendererV2.Custom )
                renderer.setClassAttribute(fieldName)
                layer.setRendererV2(renderer)

##                #renderer = QgsGraduatedSymbolRendererV2('', rangeList)
##                renderer = QgsGraduatedSymbolRendererV2(layer, fieldName, 8, classMode, symbol, rangeList)
##                #renderer.setClassAttribute(fieldName)
##                #renderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
##                layer.setRendererV2(renderer)
##                #QgsMapLayerRegistry.instance().addMapLayer(layer)
                #===========


                #renderer = QgsGraduatedSymbolRendererV2( layer, fieldName, 8, classMode, symbol, rangeList )
                #renderer.setMode( QgsGraduatedSymbolRendererV2.Custom )
                #layer.setRendererV2( renderer )

               # pass


##            symbols = layer.rendererV2().symbols()
##            symbol = symbols[0]
##            symbol.setWidth(layerWidth)
##            symbol.setColor(color)
##            layer.rendererV2().setSymbol(symbol)
            #Finally, add the layer to the map if everything is okay:
            QgsMapLayerRegistry.instance().addMapLayers([layer])
        else:
            QMessageBox.information(self.iface.mainWindow(), "M-RAMS",  "Layer %s did not load" % layer.name(),QMessageBox.Ok)


    def changeAttribute(self):
        return

    def changeLayer(self):
        ###https://dba.stackexchange.com/questions/22362/how-do-i-list-all-columns-for-a-specified-table
        table=self.dlg.comboLayer.currentText()
        self.dlg.comboAttribute.clear()
        sql = "SELECT table_name, column_name,data_type FROM information_schema.columns where table_name = '" + table + "'"

        #QMessageBox.information(self.iface.mainWindow(), "M-RDS",  sql ,QMessageBox.Ok)

        #conn = psycopg2.connect("dbname='mrams'host='localhost' user='mrams'")
        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        cur.execute(sql)
        self.dlg.comboAttribute.clear()
        for row in cur:
            if row[2]=='integer' or row[2]=='smallint' or row[2]=='numeric':
                self.dlg.comboAttribute.addItem(row[1])
        conn.close()

        return


    def changeClassification(self):
        #self.classMode = self.dlg.comboClass.currentIndex()
        return


