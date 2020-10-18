# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MRDS_Query
                                 A QGIS plugin
 Query and reporting
                              -------------------
        begin                : 2017-10-25
        git sha              : $Format:%H$
        copyright            : (C) 2017 by luv
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
from PyQt4.QtSql import *

from qgis.core import * ###QgsMessageLog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from mrds_query_dialog import MRDS_QueryDialog
import os.path
import psycopg2
from functions import *
import csv
from qgis.utils import plugins

class MRDS_Query:
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
        self.dlg = MRDS_QueryDialog()
        self.dlg.btnQuery.clicked.connect(self.showQuery)
        self.dlg.btnPDF.clicked.connect(self.makeTableDocument)
        self.dlg.comboQuery.currentIndexChanged.connect(self.selectionchange)
        #self.dlg.btnHighlight.clicked.connect(self.highlightFeatures)

        #get variables from other plugins via instance and  from qgis.utils import plugins
        self.instance = plugins['1_MRDS_Login']

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon = QIcon(':/plugins/5_MRDS_Query/icon.png')
        self.action = QAction(icon,"M-RAMS Query", self.iface.mainWindow())
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
        """Removes the plugin menu item and icon from QGIS GUI."""
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

        ###combobox key/value
        ###https://stackoverflow.com/questions/2675296/key-value-pyqt-qcombobox
        self.dlg.comboQuery.clear()

        desc =  "Query: Length of OSM road network , summarized by type?"
        sql = "SELECT fclass, Sum(ST_Length(geom)) AS length FROM osm_road_conn GROUP BY fclass ORDER BY length DESC;"
        self.dlg.comboQuery.addItem  (desc, sql)

        desc = "Query: What is the length of road network in Naypjydaw state, summarized by type?"
        sql = "SELECT o.fclass, Sum(ST_Length(o.geom)) AS length FROM osm_road_conn o, mimu_state s  where s.st='Naypyitaw' GROUP BY fclass ORDER BY length DESC;"
        self.dlg.comboQuery.addItem  (desc, sql)

        desc = "Query: average IRI by state (SROMP)"
        sql = "SELECT s.st, count(r.geom), sum(ST_length(r.geom)), avg(r.calculatediri) FROM mimu_state s, sromp_road_point r WHERE ST_Intersects(r.geom, s.geom) group by s.st;"
        self.dlg.comboQuery.addItem  ( desc, sql) #key/value

        desc = "Query: Number of roads and total length by state (OSM)"
        sql = "SELECT s.st, count(r.geom), sum(ST_length(r.geom)) FROM mimu_state s, osm_road_conn r WHERE ST_Intersects(r.geom, s.geom) group by s.st;"
        self.dlg.comboQuery.addItem  ( desc,sql)

        desc = "Query: Regions/States and their capital."
        sql = ("SELECT pol.gid, pol.st, poi.gid, poi.name"
                " FROM mimu_state pol, mimu_city poi"
                " WHERE ST_Intersects(pol.geom, poi.geom)")
        self.dlg.comboQuery.addItem  ( desc, sql) #key/value

        desc = "Query: States of Myanmar"
        sql = "select * from mimu_state"
        self.dlg.comboQuery.addItem( desc,sql ) #key/value

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def selectionchange(self,i):
        print "Current index",i,"selection changed ",self.dlg.comboQuery.currentText()
        QgsMessageLog.logMessage(str(i), "RAMS")
        self.dlg.textSQL.setText(self.dlg.comboQuery.itemData(i)) #currentText(i) for the key
        return

    def showQuery(self):
        #QMessageBox.information(self.iface.mainWindow(), "QGIS","Passed")
        QgsMessageLog.logMessage("RDS1", "RAMS", 0)

        try:
            qTable= self.dlg.tableWidget
            qTable.setRowCount(0)
            qTable.setColumnCount(0)

            ##https://stackoverflow.com/questions/38703529/python-pyqt-and-psycopg2-with-tablewidget
            #conn = psycopg2.connect("dbname='mrams' user='mrams' host='localhost' password='mrams'")
            conn = psycopg2.connect("dbname='mrams' user='" + self.RAMSusername +"' host='" + self.RAMSserver + "' password='" + self.RAMSpassword +"'")


            QgsMessageLog.logMessage("RDS2", "RAMS", 0)

            sql = self.dlg.textSQL.toPlainText()
            cur = conn.cursor()
            cur.execute(sql)

            rows = cur.fetchall()
            qTable.setRowCount(len(rows))
            colnames = [desc[0] for desc in cur.description]
            qTable.setColumnCount(len(colnames))
            qTable.setHorizontalHeaderLabels(colnames)

            for row in range(len(rows)):
                for col in range(len(colnames)):
                    item = QTableWidgetItem(str(rows[row][col]))
                    qTable.setItem(row,col,item)

            qTable.resizeColumnsToContents()

    ##https://stackoverflow.com/questions/8193920/print-a-text-through-a-printer-using-pyqt4
    ##https://stackoverflow.com/questions/22327635/how-can-i-print-data-from-my-database-while-in-qtablewidget
    ##https://bharatikunal.wordpress.com/2010/01/31/converting-html-to-pdf-with-python-and-qt/
        except psycopg2.DatabaseError, exception:
            QgsMessageLog.logMessage("RDS3", "RDS", 0)
            QMessageBox.information(self.iface.mainWindow(), "QGIS",exception)
            sys.exit(1)

        finally:
         if conn:
            conn.close()
            cur.close()
    ###https://stackoverflow.com/questions/22327635/how-can-i-print-data-from-my-database-while-in-qtablewidget
    def makeTableDocument(self):

        rows = self.dlg.tableWidget.rowCount()
        columns = self.dlg.tableWidget.columnCount()

        if rows<1 or columns<1:
            QMessageBox.information(self.iface.mainWindow(), "QGIS","You must first prepare/run the query")
            return

        document = QTextDocument()
        cursor = QTextCursor(document)
        QgsMessageLog.logMessage(str(rows), "RAMS", 0)

        table = cursor.insertTable(rows + 1, columns)
        format = table.format()
        format.setHeaderRowCount(1)
        table.setFormat(format)
        format = cursor.blockCharFormat()
        format.setFontWeight(QFont.Bold)

        for column in range(columns):
            cursor.setCharFormat(format)
            cursor.insertText("s")
            #self.dlg.tableWidget.horizontalHeaderItem(column).text())
            cursor.movePosition(QTextCursor.NextCell)
        for row in range(rows):
            for column in range(columns):
                cursor.insertText(self.dlg.tableWidget.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)

        if self.dlg.radioHTML.isChecked():
            fileName = QFileDialog.getSaveFileName(self.dlg.tableWidget, 'Save File', '', 'HTML Files (*.html)')
            if fileName == '': return
            htmText = document.toHtml()
            with open(fileName, 'w') as f:
                #f.setCodec( "utf-8" );
                f.write(htmText)

        if self.dlg.radioCSV.isChecked():
            fileName = QFileDialog.getSaveFileName(self.dlg.tableWidget, 'Save File', '', 'CSV Files (*.csv)')
            if fileName == '': return
##          csvText =  document.toPlainText()
##            with open(fileName, 'w') as f:
##                f.write(csvText)
            ###https://stackoverflow.com/questions/12608835/writing-a-qtablewidget-to-a-csv-or-xls
            with open(unicode(fileName), 'wb') as stream:
                writer = csv.writer(stream, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC )

                for row in range(self.dlg.tableWidget.rowCount()):
                    rowdata = []
                    for column in range(self.dlg.tableWidget.columnCount()):
                        item = self.dlg.tableWidget.item(row, column)
                        if item is not None:
                            rowdata.append(
                                unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)


##csv.QUOTE_ALL - Quote everything, regardless of type.
##csv.QUOTE_MINIMAL - Quote fields with special characters
##csv.QUOTE_NONNUMERIC - Quote all fields that are not integers or floats
##csv.QUOTE_NONE - Do not quote anything on output

##output_file = open(filename, 'w')
##
##selectedLayerIndex = self.dlg.comboBox.currentIndex()
##selectedLayer = layers[selectedLayerIndex]
##fields = selectedLayer.pendingFields()
##fieldnames = [field.name() for field in fields]
##
##for f in selectedLayer.getFeatures():
##    line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
##    unicode_line = line.encode('utf-8')
##    output_file.write(unicode_line)
##output_file.close()

        if self.dlg.radioPDF.isChecked():
            fileName = QFileDialog.getSaveFileName(self.dlg.tableWidget, 'Save File', '', 'PDF Files (*.pdf)')
            if fileName == '': return
            #if QFileInfo(fileName).suffix().isEmpty():
            #    fileName.append(".pdf");

            #set up the QPrinter
            p = QPrinter(QPrinter.HighResolution)
            p.setPaperSize(QPrinter.A4)
            p.setOutputFormat(QPrinter.PdfFormat)
            p.setOrientation(QPrinter.Landscape)
            p.setOutputFileName(fileName)
            document.print_(p)

#######----------------
##        docc = QTextDocument();
##        docc.setHtml( "<p>A QTextDocument can be used to present formatted text "
##                "in a nice way.</p>"
##                "<p align=center>It can be <b>formatted</b> "
##                "<font size=+2>in</font> <i>different</i> ways.</p>"
##                "<p>The text can be really long and contain many "
##                "paragraphs. It is properly wrapped and such...</p>" );
##        printer = QPrinter
##        printer.setOutputFileName(printer,"out.pdf")
##        printer.setOutputFormat(QPrinter.PdfFormat)
##
##        docc.print_(printer)
##        printer.newPage()

######-------------
        QgsMessageLog.logMessage("saved", "RAMS", 0)
        QMessageBox.information(self.iface.mainWindow(), "QGIS",'The file is saved successfully ('  + fileName + ')')
        return

    def highlightFeatures(self):

        QMessageBox.information(self.iface.mainWindow(), "START",'OK function')
        sql = self.dlg.textSQL.toPlainText()
        QMessageBox.information(self.iface.mainWindow(), sql,'OK function')
        layer = self.iface.activeLayer()
        ###selection=[]
        selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(sql))
        layer.setSelectedFeatures([k.objectid() for k in selection])
##        for feature in layer.getFeatures():
##            geom = feature.geometry()
##            roadNo = feature.attribute("Road_Type")
##            if roadNo == "Primary Road":
##                selection.append(feature.id())
##
##        layer.setSelectedFeatures(selection)

        QMessageBox.information(self.iface.mainWindow(), "QGIS",'OK function')
        return


