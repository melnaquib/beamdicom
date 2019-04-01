# -*- coding: utf-8 -*-

"""
Module implementing DicomNetworkSettingWidget.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from ui.Ui_DicomNetworkSettingWidget import Ui_Form


class DicomNetworkSettingWidget(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DicomNetworkSettingWidget, self).__init__(parent)
        self.setupUi(self)



if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    app = QApplication(sys.argv)
    w = DicomNetworkSettingWidget()
    w.show()
    sys.exit(app.exec_())