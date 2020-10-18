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
import psycopg2

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mrds_romdas_dialog import MRDS_RomdasDialog
import os.path
from PyQt4 import uic
import csv
from os.path import basename
from datetime import datetime
from PyQt4 import QtGui
 ###https://gis.stackexchange.com/questions/159397/setting-variables-on-startup-using-pyqgis
from qgis.utils import plugins
import subprocess



class MRDS_Romdas:
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
     #  self.dlg.btnCreate.clicked.connect(self.makeMap)
        self.dlg = MRDS_RomdasDialog()
        self.dlg.btnSelectMDB.clicked.connect(self.selectMDB)
        #self.dlg.btnSelectIRI.clicked.connect(self.selectCSViri)
        self.dlg.btnImportIRI.clicked.connect(self.importCSViri)
        self.dlg.btnUpdateSegments.clicked.connect(self.updateLineSegments)

        #Data editing and rebuilding
        self.dlg.btnUpdateMOCidentifier.clicked.connect(self.updateMOCidentifier)
        self.dlg.btnRebuildSegments.clicked.connect(self.rebuildSegments)
        self.dlg.btnBuildMOCroads.clicked.connect(self.buildMOCroads)

        self.dlg.btnSelectAsset.clicked.connect(self.selectCSVasset)
        self.dlg.btnImportAssets.clicked.connect(self.importCSVasset)

        self.path = ""

        #get variables from other plugins via instance and  from qgis.utils import plugins
        self.instance = plugins['1_MRDS_Login']


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

    def initGui(self):

        icon = QIcon(':/plugins/6_MRDS_ROMDAS/icon.png')
        self.action = QAction(icon,"Load ROMDAS", self.iface.mainWindow())
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
            self.toolbar = self.iface.addToolBar('&Myanmar RAMS')      ##QToolbar("&Myanmar RDS", self.iface.mainWindow().toolBar())
            self.toolbar.setObjectName('&Myanmar RAMS')
        # connect the action to the run method
        self.toolbar.addAction(self.action)
        #self.iface.addToolBarIcon(self.action)


    def unload(self):

        self.menu = self.iface.mainWindow().findChild( QMenu, '&Myanmar RAMS' )
        self.menu.removeAction(self.action)

        self.toolbar = self.iface.mainWindow().findChild( QToolBar, '&Myanmar RAMS')
        self.toolbar.removeAction(self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):

        if not self.getGlobals():         #read paramaters to connect to database
            return

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

    def updateMOCidentifier(self):
        reply = QMessageBox.question(self.iface.mainWindow(), 'Continue?','The attribute MOC_ROAD_ID of all Selected Features for the ACTIVE LAYER will be updated. Are you sure?', QMessageBox.Yes, QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        MOC_code = self.dlg.edtIdentifier.text()
        if MOC_code is None or MOC_code == '':
            QMessageBox.information(self.iface.mainWindow(), "Error" , "You must enter the MOC code before proceeding.")
            return

        layer = self.iface.activeLayer()
        features = layer.selectedFeatures()
        nrFeatures = str(layer.selectedFeatureCount())
        fields = layer.dataProvider().fields()

        if not layer.isValid():
            return

        layer.startEditing()
        layer.updateFields()
        for f in features:
            fid= f.id()
            layer.changeAttributeValue(fid,fields.indexFromName('moc_road_id'), MOC_code)

        layer.commitChanges()
        QMessageBox.information(self.iface.mainWindow(), "Success" , "Attributes have been updated (number of features updated: " + nrFeatures + ")")


    def selectMDB(self):
        fname = QFileDialog.getOpenFileName(self.dlg, "Open ROMDAS MDB File:", self.path, 'MDB Files (*.MDB)')
        if fname == '': return
        self.path = QFileInfo(fname).path();      #store path for next time
        self.dlg.edtRomdasMDB.setText(fname)

##    def selectCSViri(self):
##        fname = QFileDialog.getOpenFileName(self.dlg, "Open CSV File with IRI information", self.path, 'CSV Files (*.CSV)')
##        if fname == '': return
##        self.path = QFileInfo(fname).path();
##        self.dlg.edtRomdasIRI.setText(fname)

    def selectCSVasset(self):
        fname = QFileDialog.getOpenFileName(self.dlg, "Open MDB File with ASSET information", self.path, 'MDB Files (*.MDB)')
        if fname == '': return
        self.path = QFileInfo(fname).path();
        self.dlg.edtRomdasAsset.setText(fname)

    def getConnSettings(self):
        #return("dbname='mrams' user='mrams' host='localhost' password='mrams'")
        return("dbname='mrams' user='" + self.RAMSusername+ "' host='" + self.RAMSserver + "' password='" + self.RAMSpassword + "'")

    def getdQote(self,s):
        dqote = '"'
        return (dqote + s + dqote)

    def getsQote(self,s):
        sqote = "'"
        return (sqote + s + sqote)

    def loadlayer (self, layerName, layerAlias,geofield, layerColor, layerWidth, uri):

        uri.setDataSource("public", layerName, geofield, "")
        layer = QgsVectorLayer(uri.uri(), layerAlias, "postgres")
        #Just to be safe, make sure everything works:
        if not layer.isValid():
            QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Layer %s" %(layer.name()) + " is not valid!", QMessageBox.Ok)


        #check if layer is already loaded in TOC
        layers = self.iface.legendInterface().layers()
        for layer1 in layers:
            layer1Name =  layer1.name()
            if layerAlias == layer1Name:
                return

        #------------- set symbology--------------
        #set the color from RGB
        color = QColor(layerColor)
        s="nothing"

        #--------- POINT --------------------------
        if layer.wkbType()==QGis.WKBPoint:
            s='POINT'

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

        #Finally, add the layer to the map if everything is okay:
        QgsMapLayerRegistry.instance().addMapLayers([layer])
        QgsMessageLog.logMessage(s, "LOG", 0)
        return



    def importCSVasset(self):
        fname = self.dlg.edtRomdasAsset.text()

        if not(os.path.isfile(fname)) :
            QMessageBox.information(self.iface.mainWindow(), "Error" , "The selected file does not exist! (" + fname + ")")
            return

        dqote = '"'
        sqote = "'"

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()

         #run executable to extract CSV from MDB
        basepath = os.path.dirname(os.path.realpath(__file__))
        dqote = '"'
        FNULL = open(os.devnull, 'w')
        dos_command = basepath +'/extract_asset.exe '  + dqote + fname + dqote
        #QMessageBox.information(self.iface.mainWindow(), "M-RAMS", dos_command,QMessageBox.Ok)
        subprocess.call(dos_command, stdout=FNULL, stderr=FNULL, shell=False)          #blocks further running of the python
        ## read csv files created
        path = os.path.dirname(fname)
        fname = path + '/convert.log'
        f = open(fname, "r")
        try:
            ASSSET_CSV = path + '/' + f.readline().rstrip() #rstrip removes \n
        finally:
            f.close()


        #cur.execute("truncate table " + dqote + "tmpROMDAS_LRP" + dqote )

        #get the session name from the filename
        session_name = basename(os.path.splitext(fname)[0])
        n = session_name.rfind('_') +1
        session_name = session_name[n:]

        #"CHAINAGE_START","CHAINAGE_END","EVENT","SWITCH_GROUP","EVENT_DESC","LRP_CHAINAGE_START","LRP_CHAINAGE_END","LRP_NUMBER_START","LRP_NUMBER_END","PHOTO_SET","LATITUDE","LONGITUDE","ALTITUDE","OFFSET","HEADING","HORZ_DIST","INCLINE","COMMENT"
        #5147.300,5147.300,"1","","post",5147.300,5147.300,0,0,0,19.822900,96.147740,142.5435,0.000000,0.000000,0.000000,0.000000,""

        fname =  ASSSET_CSV
        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            #read header line
            header = reader.next()
            header2 = [w.upper() for w in header]
            QgsMessageLog.logMessage(header2[1], "RAMS")

            event_idx = header2.index("EVENT")
            event_desc_idx = header2.index("EVENT_DESC")
            lat_idx = header2.index("LATITUDE")
            lon_idx = header2.index("LONGITUDE")
            alt_idx = header2.index("ALTITUDE")
            lrp_idx = header2.index("LRP_OFFSET_START")

            #---------------loop the CSV file and insert the data into ROMDAS_Point
            for row in reader:
                query = "insert into " + dqote + "ROMDAS_Asset" + dqote + " (session_name, event_id, event_description, Longitude, Latitude, altitude, geom) values (" + \
 			            self.getsQote(session_name) + ","+ self.getsQote(row[event_idx]) + "," + self.getsQote(row[event_desc_idx]) + "," + str(row[lon_idx]) + "," + str(row[lat_idx]) + "," + str(row[lat_idx]) + \
                         ", ST_Transform(ST_SetSRID(ST_MakePoint(" + row[lon_idx] + ","+ row[lat_idx] +"),4326),32647))"
                QgsMessageLog.logMessage(query, "RAMS")
                cur.execute(query)

            conn.commit()
            conn.close()


            if self.dlg.chkLoadAssets.isChecked():
                uri = QgsDataSourceURI()
                uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)
                ##add layer  tmpROMDAS_LRP
                self.loadlayer("ROMDAS_Asset", "ROMDAS Assets", "geom",'#FF4040', 2, uri)
                self.iface.mapCanvas().refresh()

            QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Import of ROMDAS Asset informaiton is successfully completed", QMessageBox.Ok)
            self.dlg.show()


    def importCSViri(self):

        fname =  self.dlg.edtRomdasMDB.text()
        #fname2 = self.dlg.edtRomdasIRI.text()
        #fname = 'D:/_QGIS/__Tutorial/ROMDAS/Magway-Kanbya Rd.mdb'

        uri = QgsDataSourceURI()
        uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)

        if not(os.path.isfile(fname)) :
            QMessageBox.information(self.iface.mainWindow(), "Error" , "The selected file does not exist! (" + fname + ")")
            return

        #run executable to extract CSV from MDB
        basepath = os.path.dirname(os.path.realpath(__file__))
        dqote = '"'
        FNULL = open(os.devnull, 'w')
        dos_command = basepath +'/extract_line.exe '  + dqote + fname + dqote
        #dos_command = 'notepad.exe d:/r ams.txt'#  + dqote + ' d:/rams.txt' + dqote
        #QMessageBox.information(self.iface.mainWindow(), "M-RAMS", dos_command,QMessageBox.Ok)
        subprocess.call(dos_command, stdout=FNULL, stderr=FNULL, shell=False)          #blocks further running of the python
        ## read csv files created
        path = os.path.dirname(fname)
        fname = path + '/convert.log'
        f = open(fname, "r")
        try:
            GPS_CSV = path + '/' + f.readline().rstrip() #rstrip removes \n
            IRI_CSV= path + '/' + f.readline().rstrip()
        finally:
            f.close()


        try:
            self.importCSV_GPS(GPS_CSV)
            self.importCSV_IRI(IRI_CSV)
            self.updateIRIpoints()
            QMessageBox.information(self.iface.mainWindow(), "Success" , "Import of LRP/IRI Data is successfully completed.")

            if self.dlg.chkLoadNodes.isChecked():
                ##add layer  tmpROMDAS_LRP
                self.loadlayer("ROMDAS_Point", "ROMDAS Nodes", "geom",'#FF4040', 2, uri)
                self.iface.mapCanvas().refresh()

        except Exception as e:
            QMessageBox.information(e.message + "(Check message if data was already imported: )")
            QMessageBox.information(e.__doc__ )
            raise

    #logging.error(traceback.format_exc())
    # Logs the error appropriately.

    def rebuildSegments(self):

        reply = QMessageBox.question(self.iface.mainWindow(), 'Continue?','Are you sure you want to rebuild the table with ROMDAS segments?', QMessageBox.Yes, QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        uri = QgsDataSourceURI()
        uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)

        dqote = '"'
        sqote = "'"
        # truncate table ROMDAS_Segment
        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        cur.execute("truncate table " + dqote + "ROMDAS_Segment" + dqote )
        #conn.commit()

        # loop on distinct session_name and LRP_Number
        # select distinct session_name, LRP_Number from "ROMDAS_Point"
        cur.execute("select distinct session_name, LRP_Number from " + dqote + "ROMDAS_Point" + dqote )
        item_list = cur.fetchall()
        conn.close()

##        item_list= []
##        for row in cur:
##            session_name = row[0]
##            LRP_Number = row[1]
##            if session_name is not None:
##                item_list.append([session_name,LRP_Number])
##        conn.commit()
        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        for item in item_list:
            if item[0] is not None:
                query = "INSERT INTO " + dqote + "ROMDAS_Segment"+ dqote + " (moc_road_id, session_name, gps_time,  LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, geom) " + \
                        " (select moc_road_id, session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, ST_MakeLine(geom, lead(geom) over (order by LRP_chainage))" + \
                        " from " + dqote + "ROMDAS_Point" + dqote + " where LRP_Number = " + str(item[1]) + " and session_name= " + sqote + item[0] + sqote  +')'

                cur.execute(query)
        conn.commit()
        conn.close()


        QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Rebuilding Segments successfully completed.", QMessageBox.Ok)
        # loop LRP_Number
##        INSERT INTO "ROMDAS_Segment"
##       (session_name, gps_time,  LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, geom)
##       (select session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI,
##        ST_SetSRID(ST_MakeLine(ST_Transform(geom,32647), lead(ST_Transform(geom,32647)) over (order by LRP_chainage)),32647)
##        from "ROMDAS_Point" where LRP_Number = X and session_name=Y


    def importCSV_GPS(self, filename):

        #fname = filename.replace("/","\\") # self.dlg.edtRomdasCSV.text()
        #fname = filename.encode('ascii', 'ignore')
        #fname = fname.replace("/","\\")
        #fname = 'D:\\aa\\GPS_PROCESSED_MAGWAY-KANBYA_RD.csv'
        #fname.replace("/","\\")
        fname = filename
        dqote = '"'
        sqote = "'"
        #fileReader = csv.reader(open(), delimiter=",")
        #header1 = file1reader.next() #header

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()

        cur.execute("truncate table " + dqote + "tmpROMDAS_LRP" + dqote )

        #get the session name from the filename
        session_name = basename(os.path.splitext(fname)[0]).encode('ascii','ignore')

        #n = session_name.rfind('_') +1
        #session_name = session_name[n:]

        n = session_name.rfind('GPS_PROCESSED_') +14
        session_name = session_name[n:]

        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            #read header line
            header = reader.next()
            header2 = [w.upper() for w in header]
            QgsMessageLog.logMessage(header2[1], "RAMS")

            time_idx = header2.index("GPS_TIME")
            lon_idx = header2.index("LONGITUDE")
            lat_idx = header2.index("LATITUDE")
            chain_idx = header2.index("CHAINAGE") #do not use LRP_Chainage
            speed_idx = header2.index("SPEED")
            time_idx = header2.index("GPS_TIME")
            number_idx = header2.index("LRP_NUMBER")
            #---------------loop the CSV file and insert the data into ROMDAS_Point

            number_list= []  #list with all not-null LRP_Numbers
            for row in reader:

                if int(row[number_idx]) > -1:
                    QgsMessageLog.logMessage("LRP_Number is " + row[number_idx] , "RAMS")
                    if row[number_idx] not in number_list:
                        number_list.append(row[number_idx])
                    query = "insert into " + dqote + "tmpROMDAS_LRP" + dqote + " (session_name, LRP_Number, LRP_Chainage, GPS_TIME, Longitude, Latitude, geom) values (" + \
			                sqote + session_name + sqote + "," + row[number_idx] +  "," + row[chain_idx] + ", " + sqote + row[time_idx] + sqote + "," + row[lon_idx] + "," + row[lat_idx] +  \
                            ",ST_SetSRID(ST_MakePoint(" + row[lon_idx] + ", "+ row[lat_idx] +"),4326))"
                    QgsMessageLog.logMessage(query, "RAMS")
                    cur.execute(query)

            conn.commit()
            conn.close()
            self.iface.messageBar().pushInfo(u'ROMDAS Import', u'Import of LRP Data is successfully completed.')

            self.dlg.show()


    def importCSV_IRI(self,filename):

        fname = filename #self.dlg.edtRomdasIRI.text()
        dqote='"'
        sqote = "'"

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        cur.execute("truncate table " + dqote + "tmpROMDAS_IRI" + dqote )

        #get the session name from the filename
        session_name = basename(os.path.splitext(fname)[0])
        n = session_name.rfind('_') +1
        session_name = session_name[n:]


        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            #read header line
            header = reader.next()
            header2 = [w.upper() for w in header]
            QgsMessageLog.logMessage(header2[1], "RAMS")

            chain_idx = header2.index("CHAINAGE")
            number_idx = header2.index("LRP_NUMBER_START")
            speed_idx = header2.index("SPEED")

            rwp_idx = header2.index("RWP_IRI")
            lwp_idx = header2.index("LWP_IRI")
            lane_idx = header2.index("LANE_IRI")


            #---------------loop the CSV file and insert the data into table
            for row in reader:

                if int(row[number_idx]) > -1:
                    QgsMessageLog.logMessage("LRP_Number is " + row[number_idx] , "RAMS")
                    query = "insert into " + dqote + "tmpROMDAS_IRI" + dqote + " (session_name, LRP_Chainage, LRP_Number, Speed, RWP_IRI, LWP_IRI, LANE_IRI) values (" + \
					         sqote + session_name + sqote + "," + row[chain_idx] +  "," + row[number_idx] + "," + row[speed_idx] + "," + row[rwp_idx] + "," + row[lwp_idx] + "," + row[lane_idx] + ")"
                    QgsMessageLog.logMessage(query, "RAMS")
                    cur.execute(query)

            conn.commit()
            conn.close()
            self.iface.messageBar().pushInfo(u'ROMDAS Import', u'Import of IRI Data is successfully completed.')



    def updateIRIpoints(self):
        dqote='"'
        lrp_number_list=[]

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        query = "select distinct(LRP_Number) from " + dqote + "tmpROMDAS_LRP" +dqote
        cur.execute(query)
        for row in cur:
             lrp_number_list.append(row[0])

        for n in lrp_number_list:

            # ROMDAS_Point
            query = "INSERT INTO " + dqote + "ROMDAS_Point" + dqote + " (session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, geom) \
                (select session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, \
                ST_SetSRID(ST_Transform(geom,32647),32647)  from " \
                + dqote + "tmpROMDAS_Segment" + dqote + " where LRP_Number = " + str(n) + ")"

            QgsMessageLog.logMessage(query, "RAMS")
            cur.execute(query)
            conn.commit()

        conn.close()
        self.dlg.show()
        self.iface.messageBar().pushInfo(u'ROMDAS Import', u'Creation of Point IRI Data is successfully completed.')
        #QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Creation of Point IRI Data is successfully completed.", QMessageBox.Ok)



    def updateLineSegments(self):
    ##update ROMDAS_Line table -do this for the LRS_numbers in the list
    #get first unique LRP_Number, segments with chainage from the query

        dqote='"'
        lrp_number_list=[]

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        query = "select distinct(LRP_Number) from " + dqote +"tmpROMDAS_LRP" +dqote
        cur.execute(query)
        for row in cur:
             lrp_number_list.append(row[0])

        QgsMessageLog.logMessage( "Listing Numberlist: ", "RAMS")
        for n in lrp_number_list:
            QgsMessageLog.logMessage( "LRS_numbers: " + str(n), "RAMS")

        #if self.dlg.chkROMDASline.isChecked():
        for n in lrp_number_list:
            # ROMDAS_Segment
            query = "INSERT INTO " + dqote + "ROMDAS_Segment" + dqote + " (session_name, gps_time,  LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, geom) \
                (select session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, \
                ST_SetSRID(ST_MakeLine(ST_Transform(geom,32647), lead(ST_Transform(geom,32647)) over (order by LRP_chainage)),32647)  from " \
                + dqote + "tmpROMDAS_Segment" + dqote + " where LRP_Number = " + str(n) + ")"

            QgsMessageLog.logMessage(query, "RAMS")
            cur.execute(query)
            conn.commit()

##        if not self.dlg.chkConvertCoordinates.isChecked():
##            query = "ALTER TABLE " + dqote + "ROMDAS_Segment" + dqote + " ALTER COLUMN geom TYPE Geometry(LineString, 32647) USING ST_Transform(geom, 32647);"
##            QgsMessageLog.logMessage(query, "RDS")
##            cur.execute(query)

        if self.dlg.chkLoadSegments.isChecked():
            uri = QgsDataSourceURI()
            uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)
            ##add layer  ROMDAS_Segment
            self.loadlayer("ROMDAS_Segment", "ROMDAS Segments", "geom",'#FF4040', 1, uri)
            self.iface.mapCanvas().refresh()

        conn.close()
        self.dlg.show()
        QMessageBox.information(self.iface.mainWindow(),"Myanmar RAMS", "Merging of IRI Point Data in segments is successfully completed.", QMessageBox.Ok)



    def buildMOCroads(self):
        #Rebuilding MOC Road network layer based on moc_road_id from Road_segment table.
        reply = QMessageBox.question(self.iface.mainWindow(), 'Continue?','Are you sure you want to rebuild the layer with MOC Roads?', QMessageBox.Yes, QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return

        uri = QgsDataSourceURI()
        uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)

        dqote = '"'
        sqote = "'"

        # truncate table ROMDAS_Segment
        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        cur.execute("truncate table " + dqote + "ROMDAS_Line" + dqote )

        # loop on distinct moc_road_id in layer ROMDAS_Line with sql select distinct moc_road_id from ROMDAS_Segment
        cur.execute("select distinct moc_road_id from " + dqote + "ROMDAS_Segment" + dqote )
        item_list = cur.fetchall()
        conn.close()

        conn = psycopg2.connect(self.getConnSettings())
        cur = conn.cursor()
        for item in item_list:
            if item[0] is not None:
                #get Lon and Lat of start and end coordinates


                query = "insert into " + dqote + "ROMDAS_Line" + dqote + " (moc_road_id,  speed, latitude, longitude, geom) " +\
                        "(select moc_road_id,  avg(speed), ST_X(ST_Transform(ST_StartPoint(ST_LineMerge(ST_UNION(geom))),4326))," + \
                        "ST_Y(ST_Transform(ST_StartPoint(ST_LineMerge(ST_UNION(geom))),4326)), ST_LineMerge(ST_UNION(geom)) from " + \
                        dqote + "ROMDAS_Segment" + dqote + " where moc_road_id = " + sqote + str(item[0]) + sqote + " group by moc_road_id)"

##                query = "INSERT INTO " + dqote + "ROMDAS_Segment"+ dqote + " (moc_road_id, session_name, gps_time,  LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, geom) " + \
##                        " (select moc_road_id, session_name, gps_time, LRP_Number, LRP_Chainage, longitude, latitude, speed, RWP_IRI, RWP_QUALITY, LWP_IRI, LWP_QUALITY, LANE_IRI, ST_MakeLine(geom, lead(geom) over (order by LRP_chainage))" + \
##                        " from " + dqote + "ROMDAS_Point" + dqote + " where LRP_Number = " + str(item[1]) + " and session_name= " + sqote + item[0] + sqote  +')'

                cur.execute(query)
        conn.commit()
        conn.close()


        if self.dlg.chkLoadMOCroad.isChecked():
            uri = QgsDataSourceURI()
            uri.setConnection(self.RAMSserver, "5432", "mrams", self.RAMSusername, self.RAMSpassword,2)
            ##add layer  ROMDAS_Segment
            self.loadlayer("ROMDAS_Line", "MOC Roads (ROMDAS)", "geom",'#FF4040', 1.5, uri)
            self.iface.mapCanvas().refresh()

        QMessageBox.information(self.iface.mainWindow(), "Succes!" , "Success in rebuilding MOC Road network layer based on moc_road_id.")


        #simple query looping distinct moc_road_id and convert ROMDAS_Points to MOC ROAD linestring




