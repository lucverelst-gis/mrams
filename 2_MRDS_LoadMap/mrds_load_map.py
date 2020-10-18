from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
import resources
import os

from qgis.core import *
from qgis.gui import *
#global variables
###https://gis.stackexchange.com/questions/159397/setting-variables-on-startup-using-pyqgis
from qgis.utils import plugins
from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal
from qgis.utils import plugins

# Import the code for the dialog
from mrds_loadmapdialog import MRDS_LoadMapDialog

class MRDS_Load_Map:

    def __init__(self, iface):
         # Save reference to the QGIS interface
        self.iface = iface
        #Create the dialog and keep reference
        self.dlg = MRDS_LoadMapDialog()

        #get variables from other plugins via instance and  from qgis.utils import plugins
        self.instance = plugins['1_MRDS_Login']


    def initGui(self):

        #define action
        icon = QIcon(":/plugins/2_MRDS_LoadMap/layer.png")
        self.action = QAction(icon,"Load RAMS Layers", self.iface.mainWindow())
        self.action.setStatusTip("Load standard RAMS Layers")
        self.action.triggered.connect(self.run)
        self.dlg.btnLoadLayers.clicked.connect(self.loadLayers)

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

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS' )
        if not self.toolbar:
            self.toolbar = self.iface.addToolBar('&Myanmar RAMS')      ##QToolbar("&Myanmar RDS", self.iface.mainWindow().toolBar())
            self.toolbar.setObjectName('&Myanmar RAMS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)

    def unload(self):
        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        self.menu.removeAction(self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)


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

    def run(self):

        """Run method that performs all the real work"""
        if not self.getGlobals():         #read paramaters to connect to database
            return

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def loadLanduse(self,uri):

        uri.setDataSource("public", "unep_landuse", "geom", "")
        layer = QgsVectorLayer(uri.uri(), "Land Use", "postgres")
        # Define style parameters: value, colour, legend
        land_class = {
            'Agriculture': ('#FFFFBE', 'Agriculture'),
            'Scrubland': ('#D3FFBE', 'Scrubland'),
            'Deciduous Forest': ('#D3FFBE', 'Deciduous Forest'),
            'Dry Mixed Deciduous Forest': ('#A8A800', 'Dry Mixed Deciduous Forest'),
            'Evergreen Forest': ('#64B33D', 'Evergreen Forest'),
            'Forest': ('#ABCD66', 'Forest'),
            'Mangrove': ('#F9CF6F', 'Mangrove'),
            'Moist Mixed Deciduous Forest': ('#87C989', 'Moist Mixed Deciduous Forest'),
            'No data': ('#D3FFFE', 'No data')
            }

        # Define a list for categories
        categories = []
        # Define symbology depending on layer type, set the relevant style parameters
        for classes, (color, label) in land_class.items():
            symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(QColor(color)))
            symbol.symbolLayers()[0].setOutlineColor(QColor(color))

            category = QgsRendererCategoryV2(classes, symbol, label)
            categories.append(category)

        # Column/field name to be used to read values from
        column = 'FIRST_TYPE'
        # Apply the style rendering
        renderer = QgsCategorizedSymbolRendererV2(column, categories)
        layer.setRendererV2(renderer)
        # Refresh the layer
        QgsMapLayerRegistry.instance().addMapLayers([layer])
        #layer.triggerRepaint()

    def loadSRTM(self):

        #QgsMessageLog.logMessage('raster from postgis', "RDS", 0)
        #connString= (" port=5432 dbname='mrams' user='mrams' host='localhost' password='mrams'")
        #connString = "PG: dbname=mrams host=localhost user=mrams password=mrams port=5432 mode=2 schema=public column=rast table=srtm500m"
        connString = "PG: dbname=mrams host=" + self.RAMSserver+ " user=" + self.RAMSusername+ " password=" + self.RAMSpassword + " port=5432 mode=2 schema=public column=rast table=srtm500m"
        layer = QgsRasterLayer( connString, "srtm500m" )
        ##simple
        ##if layer.isValid():
            ##layer.setContrastEnhancement( QgsContrastEnhancement.StretchToMinimumMaximum )
            ##QgsMapLayerRegistry.instance().addMapLayer( layer )
            ##QgsMessageLog.logMessage('loaded', "RDS", 0)
        if layer.isValid():
            renderer = layer.renderer()
            provider = layer.dataProvider()
            extent = layer.extent()
            stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)

            if (stats.minimumValue < 0):
                min = 0
            else:
                min= stats.minimumValue

            max = stats.maximumValue
            range = max - min
            add = range//2
            interval = min + add

            colDic = {'red':'#91df69', 'yellow':'#ffff00','blue':'#0000ff'}
            valueList =[min, interval, max]

            lst = [ QgsColorRampShader.ColorRampItem(valueList[0], QColor(colDic['red'])),
                    QgsColorRampShader.ColorRampItem(valueList[1], QColor(colDic['yellow'])),
                    QgsColorRampShader.ColorRampItem(valueList[2], QColor(colDic['blue']))]

            myRasterShader = QgsRasterShader()
            myColorRamp = QgsColorRampShader()

            myColorRamp.setColorRampItemList(lst)
            myColorRamp.setColorRampType(QgsColorRampShader.INTERPOLATED)
            myRasterShader.setRasterShaderFunction(myColorRamp)

            myPseudoRenderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(),
                                                                layer.type(),
                                                                myRasterShader)

            layer.setRenderer(myPseudoRenderer)
            QgsMapLayerRegistry.instance().addMapLayer( layer )

##        QgsMessageLog.logMessage('raster from postgis', "RDS", 0)
##        #connString= (" port=5432 dbname='mrams' user='mrams' host='localhost' password='mrams'")
##        connString = "PG: dbname=mrams host=localhost user=mrams password=mrams port=5432 mode=2 schema=public column=rast table=srtm500m"
##        layer = QgsRasterLayer( connString, "srtm500m_utm2" )
##        ##simple
##        ##if layer.isValid():
##            ##layer.setContrastEnhancement( QgsContrastEnhancement.StretchToMinimumMaximum )
##            ##QgsMapLayerRegistry.instance().addMapLayer( layer )
##            ##QgsMessageLog.logMessage('loaded', "RDS", 0)
##        if layer.isValid():
##            renderer = layer.renderer()
##            provider = layer.dataProvider()
##            extent = layer.extent()
##            stats = provider.bandStatistics(1, QgsRasterBandStats.All,extent, 0)
##
##            if (stats.minimumValue < 0):
##                min = 0
##            else:
##                min= stats.minimumValue
##
##            max = stats.maximumValue
##            range = max - min
##            add = range//2
##            interval = min + add
##
##            colDic = {'red':'#ff0000', 'yellow':'#ffff00','blue':'#0000ff'}
##            #colDic = {'red':'#91df69', 'yellow':'#ffff00','blue':'#0000ff'}
##
##            valueList =[min, interval, max]# interval+add, interval+add+add, max]
##
##            lst = [ QgsColorRampShader.ColorRampItem(valueList[0], QColor(colDic['red'])),
##                    QgsColorRampShader.ColorRampItem(valueList[1], QColor(colDic['yellow'])),
##                    QgsColorRampShader.ColorRampItem(valueList[2], QColor(colDic['blue']))]
##
####            lst = [ QgsColorRampShader.ColorRampItem(valueList[0], QColor('#ffffcc')),
####                    QgsColorRampShader.ColorRampItem(valueList[1], QColor('#a1dab4')),
####                    QgsColorRampShader.ColorRampItem(valueList[2], QColor('#41b6c4')),
####                    QgsColorRampShader.ColorRampItem(valueList[3], QColor('#2c7fb8')),
####                    QgsColorRampShader.ColorRampItem(valueList[4], QColor('#253494'))]
##
##            myRasterShader = QgsRasterShader()
##            myColorRamp = QgsColorRampShader()
##
##            myColorRamp.setColorRampItemList(lst)
##            myColorRamp.setColorRampType(QgsColorRampShader.INTERPOLATED)
##            myRasterShader.setRasterShaderFunction(myColorRamp)
##
##            myPseudoRenderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(),
##                                                                layer.type(),
##                                                                myRasterShader)
##
##            layer.setRenderer(myPseudoRenderer)
##            QgsMapLayerRegistry.instance().addMapLayer( layer )


    def loadlayer (self, layerName, layerAlias,geofield, layerColor, layerWidth, uri):

        uri.setDataSource("public", layerName, geofield, "")
        layer = QgsVectorLayer(uri.uri(), layerAlias, "postgres")
        #Just to be safe, make sure everything works:
        if not layer.isValid():
            QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Layer %s" %(layer.name()) + " is not valid!", QMessageBox.Ok)

        #------------- set symbology--------------
        #set the color from RGB
        color = QColor(layerColor)
        s="nothing"

        #--------- POINT --------------------------
        if layer.wkbType()==QGis.WKBPoint:
            s='POINT'
            # create a new symbol layer with default properties
           # symbol_layer = QgsSimpleMarkerSymbolLayerV2()
            #QMessageBox.information(self.iface.mainWindow(), "1", "Loading point", QMessageBox.Ok)

##            # set the size and color using methods
##            symbol_layer.setSize(15.0)
##            symbol_layer.setColor(color)
##            #symbol_layer.outlineColor(color)

            symbol = QgsMarkerSymbolV2.createSimple({'name': 'square'})
            # Delete first default symbollayer:
            symbol.deleteSymbolLayer(0)

            new_symbollayer = QgsSimpleMarkerSymbolLayerV2()
            new_symbollayer.setSize(layerWidth)
            new_symbollayer.setFillColor(color)
            # Add symbollayer to the symbol:
            symbol.appendSymbolLayer(new_symbollayer)
            layer.rendererV2().setSymbol(symbol)


        if layer.wkbType()==QGis.WKBLineString or layer.wkbType()==QGis.WKBMultiLineString:
            s = 'LINE'
            symbols = layer.rendererV2().symbols()
            symbol = symbols[0]
            symbol.setWidth(layerWidth)
            symbol.setColor(color)
            layer.rendererV2().setSymbol(symbol)

##            #crashes
##            props = { 'width' : '2', 'color' : '0,0,255' }
##            sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleLine").createSymbolLayer(props)
##            s = QgsLineSymbolV2([sl])
##            layer.setRendererV2( QgsSingleSymbolRendererV2( s ) )

        if layer.wkbType()==QGis.WKBPolygon or layer.wkbType()==QGis.WKBMultiPolygon:
            s='POLY'
            symbol_layer = QgsSimpleLineSymbolLayerV2()
            symbol_layer.setColor(color)
            symbol_layer.setWidth(layerWidth)
            symbol_layer.setOutlineColor(color)
            layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
##            #QMessageBox.information(self.iface.mainWindow(), "1", "Loading polygon", QMessageBox.Ok)
##            symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
##            symbol.setColor(color)
##            symbol.setAlpha(0)
##            symbol.symbolLayer(0).setOutlineColor(color)
##            #layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol.symbolLayer(0))
##            symbol.appendSymbolLayer(layer)

##            myRenderer  = layer.rendererV2()
##            mySymbol1 = QgsFillSymbolV2.createSimple({'color': layerColor,
##                                                      'color_border':'#000000',
##                                                      'width_border': str(layerWidth)})
##            myRenderer.setSymbol(mySymbol1)


        #Finally, add the layer to the map if everything is okay:
        QgsMapLayerRegistry.instance().addMapLayers([layer])
        QgsMessageLog.logMessage(s, "LOG", 0)
        return

    def loadLayers(self):

        #-1--------------connection to PostgreSQL database
        uri = QgsDataSourceURI()
        # set host name, port, database name, username and password
        #uri.setConnection("localhost", "5432", "mrams", "mrams", "mrams", 2)
        uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2) #database,user,pasword

        if self.dlg.chkLanduse.isChecked():
            self.loadLanduse(uri)

        #- ROMDAS layers--------------------------
        if self.dlg.chkRomdasNetwork.isChecked():
            self.loadlayer("ROMDAS_Line", "ROMDAS MOC Roads", "geom",'#FF4040', 2, uri)
        if self.dlg.chkRomdasSegments.isChecked():
            self.loadlayer("ROMDAS_Segment", "ROMDAS Segments", "geom",'#FF4040', 1, uri)
        if self.dlg.chkRomdasNodes.isChecked():
            self.loadlayer("ROMDAS_Point", "ROMDAS Nodes", "geom",'#FF4040', 2, uri)
        if self.dlg.chkRomdasAssets.isChecked():
            self.loadlayer("ROMDAS_Asset", "ROMDAS MOC Assets", "geom",'#FF4040', 2, uri)

        #-2------------- check checkboxes
        #Open Streetmap
        if self.dlg.chkOSM.isChecked():
            self.loadlayer("osm_road_conn", "OSM Road", "geom",'##cd3a10', .5, uri)
            self.loadlayer("osm_junction_conn", "OSM Junctions", "geom",'##cd3a10', 1, uri)

        if self.dlg.chkSROMP.isChecked():
            uri.setDataSource("public", "sromp_road_line", "geom", "")
            layer = QgsVectorLayer(uri.uri(), "Road SROMP", "postgres")
            #Just to be safe, make sure everything works:
            if not layer.isValid():
                QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Layer %s" %(layer.name()) + " is not valid!", QMessageBox.Ok)
            #Finally, add the layer to the map if everything is okay:
            QgsMapLayerRegistry.instance().addMapLayers([layer])

        #Railway
        if self.dlg.chkRailway.isChecked():
            self.loadlayer("osm_railway", "OSM Railway", "geom",'#000000', .1, uri)

        #load RIVER
        if self.dlg.chkRiver.isChecked():
            self.loadlayer("mimu_river", "River", "geom",'#0000ff', 0.4, uri)

        #load Nation
        if self.dlg.chkNation.isChecked():
            self.loadlayer("mimu_national", "Nation", "geom",'#555555', 1, uri)
        #load STATE
        if self.dlg.chkStates.isChecked():
            self.loadlayer("mimu_state", "State/Region", "geom",'#555555', .6, uri)
        #load DISTRICT
        if self.dlg.chkDistrict.isChecked():
            self.loadlayer("mimu_district", "District", "geom",'#000000', .3, uri)
       #load TOWNSHIP
        if self.dlg.chkTownship.isChecked():
            self.loadlayer("mimu_township", "Township", "geom",'#000000', 0.1, uri)
       #load CITY
        if self.dlg.chkCities.isChecked():
            self.loadlayer("mimu_city", "City", "geom",'#ffffff', 1, uri)
        ###https://gis.stackexchange.com/questions/132726/load-postgis-or-oracle-spatial-raster-layer-using-pyqgis
        ###https://gis.stackexchange.com/questions/148829/how-to-update-raster-color-ramp-with-new-min-max-values-using-pyqgis
        #load SRTM first to be background layer
        if self.dlg.chkSRTM.isChecked():
            self.loadSRTM()

        if self.dlg.chkFullExtent.isChecked():
            #set map extent
            #QMessageBox.information(self.iface.mainWindow(), "1", "Zooming Full Extent", QMessageBox.Ok)
            canvas = self.iface.mapCanvas()
            #canvas.setExtent(layer.extent())
            canvas.setExtent(canvas.fullExtent())

        self.dlg.chkRomdasNetwork.setChecked(False)
        self.dlg.chkRomdasSegments.setChecked(False)
        self.dlg.chkRomdasNodes.setChecked(False)
        self.dlg.chkRomdasAssets.setChecked(False)

        self.dlg.chkRiver.setChecked(False)
        self.dlg.chkStates.setChecked(False)
        self.dlg.chkNation.setChecked(False)
        self.dlg.chkDistrict.setChecked(False)
        self.dlg.chkTownship.setChecked(False)
        self.dlg.chkCities.setChecked(False)
        self.dlg.chkOSM.setChecked(False)
        self.dlg.chkSROMP.setChecked(False)
        self.dlg.chkSRTM.setChecked(False)

        self.dlg.chkLanduse.setChecked(False)
        self.dlg.chkRailway.setChecked(False)
        self.dlg.chkFullExtent.setChecked(False)
        self.dlg.close()
