import os
from PyQt4 import QtCore, QtGui, uic
##from ui_mrds_login import Ui_MRDS_Login




FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui_mrds_login.ui'))


# create the dialog
class MRDS_LoginDialog(QtGui.QDialog, FORM_CLASS):
  def __init__(self, parent= None):
    super(MRDS_LoginDialog, self).__init__(parent)
    # Set up the user interface from Designer.
    ##self.ui = Ui_MRDS_Login ()
    self.setupUi(self)


##class SaveAttributesDialog(QtGui.QDialog, FORM_CLASS):
##    def __init__(self, parent=None):
##        """Constructor."""
##        super(SaveAttributesDialog, self).__init__(parent)
##        # Set up the user interface from Designer.
##        # After setupUI you can access any designer object by doing
##        # self.<objectname>, and you can use autoconnect slots - see
##        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
##        # #widgets-and-dialogs-with-auto-connect
##        self.setupUi(self)