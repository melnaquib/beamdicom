# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/melnaquib/work/freelancer.com/joshua/dicom_router/ui/StudyItemWidget.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
  def setupUi(self, Form):
    Form.setObjectName("Form")
    Form.resize(1224, 272)
    self.gridLayout_3 = QtWidgets.QGridLayout(Form)
    self.gridLayout_3.setObjectName("gridLayout_3")
    self.gridLayout_2 = QtWidgets.QGridLayout()
    self.gridLayout_2.setObjectName("gridLayout_2")
    self.detailsLabel = QtWidgets.QLabel(Form)
    self.detailsLabel.setObjectName("detailsLabel")
    self.gridLayout_2.addWidget(self.detailsLabel, 0, 1, 1, 1)
    self.thumbnailLabel = QtWidgets.QLabel(Form)
    self.thumbnailLabel.setMinimumSize(QtCore.QSize(32, 32))
    self.thumbnailLabel.setMaximumSize(QtCore.QSize(256, 256))
    self.thumbnailLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    self.thumbnailLabel.setText("")
    self.thumbnailLabel.setScaledContents(True)
    self.thumbnailLabel.setObjectName("thumbnailLabel")
    self.gridLayout_2.addWidget(self.thumbnailLabel, 0, 0, 1, 1)
    self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)

    self.retranslateUi(Form)
    QtCore.QMetaObject.connectSlotsByName(Form)

  def retranslateUi(self, Form):
    _translate = QtCore.QCoreApplication.translate
    Form.setWindowTitle(_translate("Form", "Form"))
    self.detailsLabel.setText(_translate("Form", "<H3>{lname}, {fname}</H3>\n"
"<H6 style=\"color: \'gray\';\">{date}<H6>\n"
"<BR/>\n"
"<H6 style=\"color: \'gray\';\">{id}<H6> \n"
"<H5 align=\"right\" style=\"color: \'{color}\';\">{status}<H5>\n"
""))


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  Form = QtWidgets.QWidget()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())

