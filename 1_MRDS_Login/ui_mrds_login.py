# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mrds_login.ui'
#
# Created: Wed Jul 11 12:42:54 2018
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

class Ui_MRDS_Login(object):
    def setupUi(self, MRDS_Login):
        MRDS_Login.setObjectName(_fromUtf8("MRDS_Login"))
        MRDS_Login.resize(299, 338)
        MRDS_Login.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        self.label_2 = QtGui.QLabel(MRDS_Login)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.line = QtGui.QFrame(MRDS_Login)
        self.line.setGeometry(QtCore.QRect(20, 70, 271, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_3 = QtGui.QLabel(MRDS_Login)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 131, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(MRDS_Login)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 131, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.btnAbout = QtGui.QPushButton(MRDS_Login)
        self.btnAbout.setGeometry(QtCore.QRect(20, 290, 75, 23))
        self.btnAbout.setObjectName(_fromUtf8("btnAbout"))
        self.label_8 = QtGui.QLabel(MRDS_Login)
        self.label_8.setGeometry(QtCore.QRect(90, 60, 191, 16))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.btnConnect = QtGui.QPushButton(MRDS_Login)
        self.btnConnect.setGeometry(QtCore.QRect(200, 290, 91, 26))
        self.btnConnect.setObjectName(_fromUtf8("btnConnect"))
        self.btnCancel = QtGui.QPushButton(MRDS_Login)
        self.btnCancel.setGeometry(QtCore.QRect(120, 290, 75, 26))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.editUser = QtGui.QLineEdit(MRDS_Login)
        self.editUser.setGeometry(QtCore.QRect(20, 110, 251, 20))
        self.editUser.setText(_fromUtf8(""))
        self.editUser.setObjectName(_fromUtf8("editUser"))
        self.editPassword = QtGui.QLineEdit(MRDS_Login)
        self.editPassword.setGeometry(QtCore.QRect(20, 160, 251, 20))
        self.editPassword.setInputMask(_fromUtf8(""))
        self.editPassword.setText(_fromUtf8(""))
        self.editPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.editPassword.setObjectName(_fromUtf8("editPassword"))
        self.chkAddLayer = QtGui.QCheckBox(MRDS_Login)
        self.chkAddLayer.setGeometry(QtCore.QRect(20, 260, 201, 17))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.chkAddLayer.setFont(font)
        self.chkAddLayer.setChecked(False)
        self.chkAddLayer.setObjectName(_fromUtf8("chkAddLayer"))
        self.label_5 = QtGui.QLabel(MRDS_Login)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 131, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.editServer = QtGui.QLineEdit(MRDS_Login)
        self.editServer.setGeometry(QtCore.QRect(20, 210, 251, 20))
        self.editServer.setInputMask(_fromUtf8(""))
        self.editServer.setText(_fromUtf8(""))
        self.editServer.setEchoMode(QtGui.QLineEdit.Normal)
        self.editServer.setCursorPosition(0)
        self.editServer.setObjectName(_fromUtf8("editServer"))
        self.chkRemoveLayers = QtGui.QCheckBox(MRDS_Login)
        self.chkRemoveLayers.setGeometry(QtCore.QRect(20, 240, 191, 17))
        self.chkRemoveLayers.setObjectName(_fromUtf8("chkRemoveLayers"))

        self.retranslateUi(MRDS_Login)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("pressed()")), MRDS_Login.reject)
        QtCore.QMetaObject.connectSlotsByName(MRDS_Login)

    def retranslateUi(self, MRDS_Login):
        MRDS_Login.setWindowTitle(_translate("MRDS_Login", "M-RAMS", None))
        self.label_2.setText(_translate("MRDS_Login", "<html><head/><body><p><span style=\" font-size:12pt;\">Myanmar <br/>Road Asset Management System</span></p></body></html>", None))
        self.label_3.setText(_translate("MRDS_Login", "User name", None))
        self.label_4.setText(_translate("MRDS_Login", "Password", None))
        self.btnAbout.setText(_translate("MRDS_Login", "About", None))
        self.label_8.setText(_translate("MRDS_Login", "ADB TA-8987 Myanmar", None))
        self.btnConnect.setText(_translate("MRDS_Login", "Connect && Close", None))
        self.btnCancel.setText(_translate("MRDS_Login", "Cancel", None))
        self.chkAddLayer.setText(_translate("MRDS_Login", "Add Myanmar Background Layer", None))
        self.label_5.setText(_translate("MRDS_Login", "Server", None))
        self.chkRemoveLayers.setText(_translate("MRDS_Login", "Remove all loaded layers", None))

