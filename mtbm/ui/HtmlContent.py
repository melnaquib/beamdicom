# -*- coding: utf-8 -*-

"""
Module implementing HtmlContent.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QUrl
from .Ui_HtmlContent import Ui_Dialog


class HtmlContent(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HtmlContent, self).__init__(parent)
        self.setupUi(self)

    def setContent(self, Content):
        self.textBrowser.setHtml(Content)

    def setContentFromFile(self, fileName):
        self.textBrowser.setSource(QUrl(fileName))

