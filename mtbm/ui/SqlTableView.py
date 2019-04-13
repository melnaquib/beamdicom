# -*- coding: utf-8 -*-

"""
Module implementing SqlTableView.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QWidget, QMessageBox

from .Ui_SqlTableView import Ui_Form


class SqlTableView(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SqlTableView, self).__init__(parent)
        self.setupUi(self)
        self.setModel(QSqlTableModel(self))

    def setModel(self, model):
        self.tableView.setModel(model)

        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.tableView.hideColumn(0)


    def model(self):
        return self.tableView.model()

    @pyqtSlot()
    def on_resetBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        if QMessageBox.Yes == QMessageBox.warning(self, self.tr("Reload Routes"), self.tr("Are you sure you want to revert routes changes?")
                            , QMessageBox.Yes | QMessageBox.No):
            self.model().revertAll()

    @pyqtSlot()
    def on_saveBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.model().submitAll()

    @pyqtSlot()
    def on_addBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        record = self.model().record()
        self.model().insertRecord(-1, record)


    @pyqtSlot()
    def on_remBtn_clicked(self):
        """
        Slot documentation goes here.
        """
        ixs = self.tableView.selectedIndexes()
        if ixs.isEmpty():
            return

        if QMessageBox.Yes == QMessageBox.warning(self, self.tr("Delete Routes"), self.tr("Are you sure you want to delete selected routes?")
                            , QMessageBox.Yes | QMessageBox.No):
            self.model().deleteLater()





