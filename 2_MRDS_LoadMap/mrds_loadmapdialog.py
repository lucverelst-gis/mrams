import os
from PyQt4 import QtCore, QtGui, uic

from ui_mrds_load_layers import Ui_MRDS_LoadLayersDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui_mrds_load_layers.ui'))


# create the dialog
class MRDS_LoadMapDialog(QtGui.QDialog, FORM_CLASS):
  def __init__(self, parent= None):
    super(MRDS_LoadMapDialog, self).__init__(parent)
    # Set up the user interface from Designer.
    ##self.ui = Ui_MRDS_Login ()
    self.setupUi(self)
