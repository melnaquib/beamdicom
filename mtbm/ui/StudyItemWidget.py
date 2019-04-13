# -*- coding: utf-8 -*-

"""
Module implementing StudyItemWidget.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QDateTime
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlRecord

from .Ui_StudyItemWidget import Ui_Form

class StudyItemWidget(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(StudyItemWidget, self).__init__(parent)
        self.setupUi(self)

    def load(self, data):
        tmpl = """<H3>{fname}, {lname}</H3>
<H6 style="color: 'gray';">{studyDate}<H6>

<H6 style="color: 'gray';">{id}<H6> 
<H5 align="right" style="color: '{color}';">{status}<H5>
"""
        if isinstance(data, QSqlRecord):
            name = data.value(0)
            name = [i for i in name.split('^') if i]

            id = data.value(1)

            studydate = str( data.value(4))
            year = studydate[:4]
            month = studydate[4:6]
            day = studydate[6:8]
            studydate = QDate(int(year), int(month), int(day)).toString("MM-dd-yyyy")

            status = data.value(5)
            color = "green" if status else "yellow"
            if not status: status = "Processing..."

            txt = tmpl.format(lname=name[0], fname=name[-1], studyDate=studydate, id=id,
                              color=color, status=status)
            self.detailsLabel.setText(txt)

            # imgFile = "/home/melnaquib/work/freelancer.com/joshua/dicom_router/run/images/1.2.826.0.1.368043.2.206.20170330073520.725846087/1.2.826.0.1.368043.2.206.20170330073520.1842955774.1_0.png"
            byte_array = data.value(2)

            if byte_array:
                pixmap = QPixmap()
                pixmap.loadFromData(byte_array, "PNG")
                # pixmap = QPixmap(data.value(2))
                # pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                self.thumbnailLabel.setPixmap(pixmap)
