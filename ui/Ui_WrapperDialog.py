# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/melnaquib/work/freelancer.com/joshua/dicom_router/ui/WrapperDialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
  def setupUi(self, Dialog):
    Dialog.setObjectName("Dialog")
    Dialog.resize(400, 300)
    Dialog.setSizeGripEnabled(True)
    self.gridLayout = QtWidgets.QGridLayout(Dialog)
    self.gridLayout.setObjectName("gridLayout")
    self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
    self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
    self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
    self.buttonBox.setObjectName("buttonBox")
    self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

    self.retranslateUi(Dialog)
    self.buttonBox.accepted.connect(Dialog.accept)
    self.buttonBox.rejected.connect(Dialog.reject)
    QtCore.QMetaObject.connectSlotsByName(Dialog)

  def retranslateUi(self, Dialog):
    _translate = QtCore.QCoreApplication.translate
    Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  Dialog = QtWidgets.QDialog()
  ui = Ui_Dialog()
  ui.setupUi(Dialog)
  Dialog.show()
  sys.exit(app.exec_())

