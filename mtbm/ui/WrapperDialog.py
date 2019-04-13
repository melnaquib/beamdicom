# -*- coding: utf-8 -*-

"""
Module implementing WrapperDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QWidget,QLayout

from .Ui_WrapperDialog import Ui_Dialog


class WrapperDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(WrapperDialog, self).__init__(parent)
        self.setupUi(self)

    def setWidget(self, widget):
        widget.setParent(self)
        self.layout().addWidget(widget, 0,0)
        self.adjustSize()
        self._widget = widget

    def accept(self):
        self._widget.accept()
        super().accept()