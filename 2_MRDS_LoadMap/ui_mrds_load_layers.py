# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mrds_load_layers.ui'
#
# Created: Wed Jul 11 12:43:05 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MRDS_LoadLayersDialog(object):
    def setupUi(self, MRDS_LoadLayersDialog):
        MRDS_LoadLayersDialog.setObjectName(_fromUtf8("MRDS_LoadLayersDialog"))
        MRDS_LoadLayersDialog.resize(461, 313)
        self.btnLoadLayers = QtGui.QPushButton(MRDS_LoadLayersDialog)
        self.btnLoadLayers.setGeometry(QtCore.QRect(360, 280, 91, 23))
        self.btnLoadLayers.setObjectName(_fromUtf8("btnLoadLayers"))
        self.label_2 = QtGui.QLabel(MRDS_LoadLayersDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 0, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox = QtGui.QGroupBox(MRDS_LoadLayersDialog)
        self.groupBox.setGeometry(QtCore.QRect(230, 30, 221, 121))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.chkStates = QtGui.QCheckBox(self.groupBox)
        self.chkStates.setGeometry(QtCore.QRect(10, 40, 101, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkStates.setFont(font)
        self.chkStates.setObjectName(_fromUtf8("chkStates"))
        self.chkDistrict = QtGui.QCheckBox(self.groupBox)
        self.chkDistrict.setGeometry(QtCore.QRect(10, 60, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkDistrict.setFont(font)
        self.chkDistrict.setObjectName(_fromUtf8("chkDistrict"))
        self.chkTownship = QtGui.QCheckBox(self.groupBox)
        self.chkTownship.setGeometry(QtCore.QRect(10, 80, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkTownship.setFont(font)
        self.chkTownship.setObjectName(_fromUtf8("chkTownship"))
        self.chkCities = QtGui.QCheckBox(self.groupBox)
        self.chkCities.setGeometry(QtCore.QRect(10, 100, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkCities.setFont(font)
        self.chkCities.setObjectName(_fromUtf8("chkCities"))
        self.chkNation = QtGui.QCheckBox(self.groupBox)
        self.chkNation.setGeometry(QtCore.QRect(10, 20, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkNation.setFont(font)
        self.chkNation.setObjectName(_fromUtf8("chkNation"))
        self.groupBox_2 = QtGui.QGroupBox(MRDS_LoadLayersDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(230, 210, 221, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.chkSRTM = QtGui.QCheckBox(self.groupBox_2)
        self.chkSRTM.setGeometry(QtCore.QRect(10, 20, 111, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkSRTM.setFont(font)
        self.chkSRTM.setObjectName(_fromUtf8("chkSRTM"))
        self.chkLanduse = QtGui.QCheckBox(self.groupBox_2)
        self.chkLanduse.setGeometry(QtCore.QRect(10, 40, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkLanduse.setFont(font)
        self.chkLanduse.setObjectName(_fromUtf8("chkLanduse"))
        self.groupBox_3 = QtGui.QGroupBox(MRDS_LoadLayersDialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 140, 211, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.chkOSM = QtGui.QCheckBox(self.groupBox_3)
        self.chkOSM.setGeometry(QtCore.QRect(10, 20, 231, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkOSM.setFont(font)
        self.chkOSM.setObjectName(_fromUtf8("chkOSM"))
        self.chkSROMP = QtGui.QCheckBox(self.groupBox_3)
        self.chkSROMP.setGeometry(QtCore.QRect(10, 40, 171, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkSROMP.setFont(font)
        self.chkSROMP.setObjectName(_fromUtf8("chkSROMP"))
        self.groupBox_4 = QtGui.QGroupBox(MRDS_LoadLayersDialog)
        self.groupBox_4.setGeometry(QtCore.QRect(230, 150, 221, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.chkRiver = QtGui.QCheckBox(self.groupBox_4)
        self.chkRiver.setGeometry(QtCore.QRect(10, 20, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRiver.setFont(font)
        self.chkRiver.setChecked(False)
        self.chkRiver.setObjectName(_fromUtf8("chkRiver"))
        self.chkRailway = QtGui.QCheckBox(self.groupBox_4)
        self.chkRailway.setGeometry(QtCore.QRect(10, 40, 70, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRailway.setFont(font)
        self.chkRailway.setObjectName(_fromUtf8("chkRailway"))
        self.chkFullExtent = QtGui.QCheckBox(MRDS_LoadLayersDialog)
        self.chkFullExtent.setGeometry(QtCore.QRect(20, 280, 131, 17))
        self.chkFullExtent.setChecked(True)
        self.chkFullExtent.setObjectName(_fromUtf8("chkFullExtent"))
        self.groupBox_5 = QtGui.QGroupBox(MRDS_LoadLayersDialog)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 30, 211, 101))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.chkRomdasSegments = QtGui.QCheckBox(self.groupBox_5)
        self.chkRomdasSegments.setGeometry(QtCore.QRect(10, 40, 201, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRomdasSegments.setFont(font)
        self.chkRomdasSegments.setObjectName(_fromUtf8("chkRomdasSegments"))
        self.chkRomdasNodes = QtGui.QCheckBox(self.groupBox_5)
        self.chkRomdasNodes.setGeometry(QtCore.QRect(10, 60, 171, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRomdasNodes.setFont(font)
        self.chkRomdasNodes.setObjectName(_fromUtf8("chkRomdasNodes"))
        self.chkRomdasNetwork = QtGui.QCheckBox(self.groupBox_5)
        self.chkRomdasNetwork.setGeometry(QtCore.QRect(10, 20, 201, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRomdasNetwork.setFont(font)
        self.chkRomdasNetwork.setObjectName(_fromUtf8("chkRomdasNetwork"))
        self.chkRomdasAssets = QtGui.QCheckBox(self.groupBox_5)
        self.chkRomdasAssets.setGeometry(QtCore.QRect(10, 80, 171, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkRomdasAssets.setFont(font)
        self.chkRomdasAssets.setObjectName(_fromUtf8("chkRomdasAssets"))

        self.retranslateUi(MRDS_LoadLayersDialog)
        QtCore.QMetaObject.connectSlotsByName(MRDS_LoadLayersDialog)

    def retranslateUi(self, MRDS_LoadLayersDialog):
        MRDS_LoadLayersDialog.setWindowTitle(_translate("MRDS_LoadLayersDialog", "M-RAMS", None))
        self.btnLoadLayers.setText(_translate("MRDS_LoadLayersDialog", "Load and Close", None))
        self.label_2.setText(_translate("MRDS_LoadLayersDialog", "<html><head/><body><p><span style=\" font-size:12pt;\">M-RAMS - Add Standard Layers</span></p></body></html>", None))
        self.groupBox.setTitle(_translate("MRDS_LoadLayersDialog", "Administrative Units", None))
        self.chkStates.setText(_translate("MRDS_LoadLayersDialog", "State/Region", None))
        self.chkDistrict.setText(_translate("MRDS_LoadLayersDialog", "District", None))
        self.chkTownship.setText(_translate("MRDS_LoadLayersDialog", "Township", None))
        self.chkCities.setText(_translate("MRDS_LoadLayersDialog", "City", None))
        self.chkNation.setText(_translate("MRDS_LoadLayersDialog", "Nation", None))
        self.groupBox_2.setTitle(_translate("MRDS_LoadLayersDialog", "Background", None))
        self.chkSRTM.setText(_translate("MRDS_LoadLayersDialog", "Elevation Model", None))
        self.chkLanduse.setText(_translate("MRDS_LoadLayersDialog", "Landuse", None))
        self.groupBox_3.setTitle(_translate("MRDS_LoadLayersDialog", "Other Road Features", None))
        self.chkOSM.setText(_translate("MRDS_LoadLayersDialog", "Open Streetmap (OSM)", None))
        self.chkSROMP.setText(_translate("MRDS_LoadLayersDialog", "RoadRoid (SROMP)", None))
        self.groupBox_4.setTitle(_translate("MRDS_LoadLayersDialog", "Other Layers", None))
        self.chkRiver.setText(_translate("MRDS_LoadLayersDialog", "Main River", None))
        self.chkRailway.setText(_translate("MRDS_LoadLayersDialog", "Railway", None))
        self.chkFullExtent.setText(_translate("MRDS_LoadLayersDialog", "Zoom to Full Extent", None))
        self.groupBox_5.setTitle(_translate("MRDS_LoadLayersDialog", "ROMDAS and MOC", None))
        self.chkRomdasSegments.setText(_translate("MRDS_LoadLayersDialog", "Road Segments", None))
        self.chkRomdasNodes.setText(_translate("MRDS_LoadLayersDialog", "Road Nodes", None))
        self.chkRomdasNetwork.setText(_translate("MRDS_LoadLayersDialog", "MOC Road Network", None))
        self.chkRomdasAssets.setText(_translate("MRDS_LoadLayersDialog", "Road Assets", None))

