# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/melnaquib/work/client/reportly/code/beamdicom/ui/SettingWidgetIpR.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(624, 349)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.directoriesgroupBox = QtWidgets.QGroupBox(Form)
        self.directoriesgroupBox.setObjectName("directoriesgroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.directoriesgroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.runFldrbtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.runFldrbtn.setObjectName("runFldrbtn")
        self.gridLayout_2.addWidget(self.runFldrbtn, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.storageFldrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.storageFldrLineUnit.setObjectName("storageFldrLineUnit")
        self.gridLayout_2.addWidget(self.storageFldrLineUnit, 2, 1, 1, 1)
        self.storageFldrBtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.storageFldrBtn.setObjectName("storageFldrBtn")
        self.gridLayout_2.addWidget(self.storageFldrBtn, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.logFldrBtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.logFldrBtn.setObjectName("logFldrBtn")
        self.gridLayout_2.addWidget(self.logFldrBtn, 1, 2, 1, 1)
        self.runFdrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.runFdrLineUnit.setObjectName("runFdrLineUnit")
        self.gridLayout_2.addWidget(self.runFdrLineUnit, 0, 1, 1, 1)
        self.logFldrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.logFldrLineUnit.setObjectName("logFldrLineUnit")
        self.gridLayout_2.addWidget(self.logFldrLineUnit, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.directoriesgroupBox, 1, 0, 2, 2)
        self.dicomservergroupBox = QtWidgets.QGroupBox(Form)
        self.dicomservergroupBox.setObjectName("dicomservergroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dicomservergroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.dicomServerWidget = DicomNetworkSettingWidget(self.dicomservergroupBox)
        self.dicomServerWidget.setObjectName("dicomServerWidget")
        self.gridLayout_4.addWidget(self.dicomServerWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.dicomservergroupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.directoriesgroupBox.setTitle(_translate("Form", "Directories"))
        self.runFldrbtn.setText(_translate("Form", "....."))
        self.label_3.setText(_translate("Form", "Storage Folder"))
        self.storageFldrBtn.setText(_translate("Form", "......"))
        self.label.setText(_translate("Form", "Run Folder"))
        self.label_2.setText(_translate("Form", "Log Folder"))
        self.logFldrBtn.setText(_translate("Form", "......."))
        self.dicomservergroupBox.setTitle(_translate("Form", "Dicom Server"))

from DicomNetworkSettingWidget import DicomNetworkSettingWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

