# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/melnaquib/work/client/reportly/code/beamdicom/ui/SettingWidgetNewIp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(973, 744)
        Form.setMinimumSize(QtCore.QSize(900, 600))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setMinimumSize(QtCore.QSize(900, 600))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 953, 724))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.dicomservergroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.dicomservergroupBox.setObjectName("dicomservergroupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dicomservergroupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.dicomServerWidget = DicomNetworkSettingWidget(self.dicomservergroupBox)
        self.dicomServerWidget.setObjectName("dicomServerWidget")
        self.gridLayout_5.addWidget(self.dicomServerWidget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.dicomservergroupBox, 0, 0, 1, 1)
        self.dicomsendergroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.dicomsendergroupBox.setObjectName("dicomsendergroupBox")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dicomsendergroupBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.dicomSenderWidget = DicomNetworkSettingWidget(self.dicomsendergroupBox)
        self.dicomSenderWidget.setObjectName("dicomSenderWidget")
        self.gridLayout_6.addWidget(self.dicomSenderWidget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.dicomsendergroupBox, 0, 1, 1, 1)
        self.targetpacsgroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.targetpacsgroupBox.setObjectName("targetpacsgroupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.targetpacsgroupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.targetPacsWidget = DicomNetworkSettingWidget(self.targetpacsgroupBox)
        self.targetPacsWidget.setObjectName("targetPacsWidget")
        self.gridLayout_7.addWidget(self.targetPacsWidget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.targetpacsgroupBox, 1, 0, 1, 1)
        self.targerpacs2groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.targerpacs2groupBox.setObjectName("targerpacs2groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.targerpacs2groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.targetPacs1Widget = DicomNetworkSettingWidget(self.targerpacs2groupBox)
        self.targetPacs1Widget.setObjectName("targetPacs1Widget")
        self.gridLayout_4.addWidget(self.targetPacs1Widget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.targerpacs2groupBox, 1, 1, 1, 1)
        self.directoriesgroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.directoriesgroupBox.setObjectName("directoriesgroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.directoriesgroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.storageFldrBtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.storageFldrBtn.setObjectName("storageFldrBtn")
        self.gridLayout_2.addWidget(self.storageFldrBtn, 3, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.runFdrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.runFdrLineUnit.setObjectName("runFdrLineUnit")
        self.gridLayout_2.addWidget(self.runFdrLineUnit, 0, 1, 1, 1)
        self.logFldrBtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.logFldrBtn.setObjectName("logFldrBtn")
        self.gridLayout_2.addWidget(self.logFldrBtn, 1, 2, 1, 1)
        self.runFldrbtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.runFldrbtn.setObjectName("runFldrbtn")
        self.gridLayout_2.addWidget(self.runFldrbtn, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.tmpFldrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.tmpFldrLineUnit.setObjectName("tmpFldrLineUnit")
        self.gridLayout_2.addWidget(self.tmpFldrLineUnit, 2, 1, 1, 1)
        self.logFldrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.logFldrLineUnit.setObjectName("logFldrLineUnit")
        self.gridLayout_2.addWidget(self.logFldrLineUnit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.tmpFldrBtn = QtWidgets.QPushButton(self.directoriesgroupBox)
        self.tmpFldrBtn.setObjectName("tmpFldrBtn")
        self.gridLayout_2.addWidget(self.tmpFldrBtn, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.directoriesgroupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.storageFldrLineUnit = QtWidgets.QLineEdit(self.directoriesgroupBox)
        self.storageFldrLineUnit.setObjectName("storageFldrLineUnit")
        self.gridLayout_2.addWidget(self.storageFldrLineUnit, 3, 1, 1, 1)
        self.gridLayout_8.addWidget(self.directoriesgroupBox, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 0, 0, 1, 1)
        self.ipAddressFld = QtWidgets.QLineEdit(self.groupBox)
        self.ipAddressFld.setObjectName("ipAddressFld")
        self.gridLayout_9.addWidget(self.ipAddressFld, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.gridLayout_8.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dicomservergroupBox.setTitle(_translate("Form", "Dicom Server"))
        self.dicomsendergroupBox.setTitle(_translate("Form", "Dicom Sender"))
        self.targetpacsgroupBox.setTitle(_translate("Form", "Target Pacs"))
        self.targerpacs2groupBox.setTitle(_translate("Form", "Target Pacs 2"))
        self.directoriesgroupBox.setTitle(_translate("Form", "Directories"))
        self.storageFldrBtn.setText(_translate("Form", "......"))
        self.label_3.setText(_translate("Form", "Storage Folder"))
        self.logFldrBtn.setText(_translate("Form", "......."))
        self.runFldrbtn.setText(_translate("Form", "....."))
        self.label.setText(_translate("Form", "Run Folder"))
        self.label_2.setText(_translate("Form", "Log Folder"))
        self.tmpFldrBtn.setText(_translate("Form", "......."))
        self.label_4.setText(_translate("Form", "Temp Folder"))
        self.groupBox.setTitle(_translate("Form", "Network"))
        self.label_7.setText(_translate("Form", "Ip Address"))

from mtbm.ui.DicomNetworkSettingWidget import DicomNetworkSettingWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

