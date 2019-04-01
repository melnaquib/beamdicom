# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\work\code\dicom_router\ui\DicomNetworkSettingWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(464, 155)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.aeTitleFiled = QtWidgets.QLineEdit(Form)
        self.aeTitleFiled.setObjectName("aeTitleFiled")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.aeTitleFiled)
        self.portFiled = QtWidgets.QLineEdit(Form)
        self.portFiled.setObjectName("portFiled")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.portFiled)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.maxPduField = QtWidgets.QLineEdit(self.groupBox)
        self.maxPduField.setObjectName("maxPduField")
        self.gridLayout.addWidget(self.maxPduField, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.networkTimeoutField = QtWidgets.QLineEdit(self.groupBox)
        self.networkTimeoutField.setObjectName("networkTimeoutField")
        self.gridLayout.addWidget(self.networkTimeoutField, 0, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.ACSETimeoutField = QtWidgets.QLineEdit(self.groupBox)
        self.ACSETimeoutField.setObjectName("ACSETimeoutField")
        self.gridLayout.addWidget(self.ACSETimeoutField, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.DIMSETimeoutField = QtWidgets.QLineEdit(self.groupBox)
        self.DIMSETimeoutField.setObjectName("DIMSETimeoutField")
        self.gridLayout.addWidget(self.DIMSETimeoutField, 1, 3, 1, 1)
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_5.raise_()
        self.networkTimeoutField.raise_()
        self.maxPduField.raise_()
        self.DIMSETimeoutField.raise_()
        self.ACSETimeoutField.raise_()
        self.label_7.raise_()
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "AE Title"))
        self.groupBox.setTitle(_translate("Form", "Advanced"))
        self.label_5.setText(_translate("Form", "Max PDU"))
        self.label_7.setText(_translate("Form", "Timout Network"))
        self.label_8.setText(_translate("Form", "Timeout ACSE"))
        self.label_9.setText(_translate("Form", "Timout DIMSE"))
        self.label_2.setText(_translate("Form", "Port"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

