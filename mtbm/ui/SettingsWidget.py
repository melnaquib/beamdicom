# -*- coding: utf-8 -*-

"""
Module implementing SettingsWidget.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import QSettings
from .DicomNetworkSettingWidget import DicomNetworkSettingWidget

from mtbm.ui.Ui_SettingWidgetIpR import Ui_Form
import utils

class SettingsWidget(QWidget, Ui_Form):

    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SettingsWidget, self).__init__(parent)
        self.setupUi(self)
        # self.ipAddressFld.setText(" ".join(str(item) for item in utils.get_ip_address()))
        self.loadSettings()
        self.runFldrbtn.clicked.connect(lambda: self.openRunFolder(self.runFdrLineUnit))
        self.logFldrBtn.clicked.connect(lambda: self.openRunFolder(self.logFldrLineUnit))
        self.storageFldrBtn.clicked.connect(lambda: self.openRunFolder(self.storageFldrLineUnit))
        # self.tmpFldrBtn.clicked.connect(lambda: self.openRunFolder(self.tmpFldrLineUnit))

    def openRunFolder(self, widget):
        from PyQt5.QtWidgets import QFileDialog
        import os
        my_dir = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            os.getcwd(),
            QFileDialog.ShowDirsOnly
        )
        print(my_dir)
        widget.setText(my_dir)

    def loadSettings(self):
        settings = QSettings()

        self.runFdrLineUnit.setText(settings.value("storage/run"))
        self.logFldrLineUnit.setText(settings.value("storage/log"))
        self.storageFldrLineUnit.setText(settings.value("storage/folder"))
        # self.tmpFldrLineUnit.setText(settings.value("storage/tmp"))
        foldermode = 'Study IUID'
        if settings.value("storage/foldername_mode") == 'PatientName':
            foldermode = 'Patient Name'
        elif settings.value("storage/foldername_mode") == 'PatientID':
            foldermode = 'Patient ID'
        # self.foldernamemodFld.setCurrentText(foldermode)

        # self.dicomSenderWidget.aeTitleFiled.setText(settings.value("storescu/aet"))
        # self.dicomSenderWidget.maxPduField.setText(settings.value("storescu/max_pdu"))
        # self.dicomSenderWidget.networkTimeoutField.setText(settings.value("storescu/network_timeout"))
        # self.dicomSenderWidget.ACSETimeoutField.setText(settings.value("storescu/acse_timeout"))
        # self.dicomSenderWidget.DIMSETimeoutField.setText(settings.value("storescu/dimse_timeout"))
        #
        # self.dicomSenderWidget.portFiled.setVisible(False)
        # self.dicomSenderWidget.label_2.setVisible(False)
        #
        self.dicomServerWidget.aeTitleFiled.setText(settings.value("storescp/aet"))
        self.dicomServerWidget.portFiled.setText(settings.value("storescp/port"))
        self.dicomServerWidget.maxPduField.setText(settings.value("storescp/max_pdu"))
        self.dicomServerWidget.networkTimeoutField.setText(settings.value("storescp/network_timeout"))
        self.dicomServerWidget.ACSETimeoutField.setText(settings.value("storescp/acse_timeout"))
        self.dicomServerWidget.DIMSETimeoutField.setText(settings.value("storescp/dimse_timeout"))
        #
        # self.targetPacsWidget.aeTitleFiled.setText(settings.value("targetStorescp/aet"))
        # self.targetPacsWidget.portFiled.setText(settings.value("targetStorescp/port"))
        # self.targetPacsWidget.maxPduField.setText(settings.value("targetStorescp/max_pdu"))
        # self.targetPacsWidget.networkTimeoutField.setText(settings.value("targetStorescp/network_timeout"))
        # self.targetPacsWidget.ACSETimeoutField.setText(settings.value("targetStorescp/acse_timeout"))
        # self.targetPacsWidget.DIMSETimeoutField.setText(settings.value("targetStorescp/dimse_timeout"))
        #
        # self.targetPacs1Widget.aeTitleFiled.setText(settings.value("targetStorescp1/aet"))
        # self.targetPacs1Widget.portFiled.setText(settings.value("targetStorescp1/port"))
        # self.targetPacs1Widget.maxPduField.setText(settings.value("targetStorescp1/max_pdu"))
        # self.targetPacs1Widget.networkTimeoutField.setText(settings.value("targetStorescp1/network_timeout"))
        # self.targetPacs1Widget.ACSETimeoutField.setText(settings.value("targetStorescp1/acse_timeout"))
        # self.targetPacs1Widget.DIMSETimeoutField.setText(settings.value("targetStorescp1/dimse_timeout"))

        # self.cnvDirLineEdit.setText(settings.value("conversion/folder"))
        # self.cnvFmtComboBox.setCurrentText(settings.value("conversion/format"))
        # print(True if settings.value("conversion/dicom_remove") == 'true' else False)
        # self.removeDicomCheckBox.setChecked(True if settings.value("conversion/dicom_remove") == 'true' else False)

    def accept(self):
        self.saveSettings()

    def saveSettings(self):
        settings = QSettings()

        settings.setValue('storescp/aet', self.dicomServerWidget.aeTitleFiled.text())
        settings.setValue('storescp/port', self.dicomServerWidget.portFiled.text())
        settings.setValue('storescp/max_pdu', self.dicomServerWidget.maxPduField.text())
        settings.setValue('storescp/network_timeout', self.dicomServerWidget.networkTimeoutField.text())
        settings.setValue('storescp/acse_timeout', self.dicomServerWidget.ACSETimeoutField.text())
        settings.setValue('storescp/dimse_timeout', self.dicomServerWidget.DIMSETimeoutField.text())

        # settings.setValue('targetStorescp/aet', self.targetPacsWidget.aeTitleFiled.text())
        # settings.setValue('targetStorescp/port', self.targetPacsWidget.portFiled.text())
        # settings.setValue('targetStorescp/max_pdu', self.targetPacsWidget.maxPduField.text())
        # settings.setValue('targetStorescp/network_timeout', self.targetPacsWidget.networkTimeoutField.text())
        # settings.setValue('targetStorescp/acse_timeout', self.targetPacsWidget.ACSETimeoutField.text())
        # settings.setValue('targetStorescp/dimse_timeout', self.targetPacsWidget.DIMSETimeoutField.text())

        # settings.setValue('targetStorescp1/aet', self.targetPacs1Widget.aeTitleFiled.text())
        # settings.setValue('targetStorescp1/port', self.targetPacs1Widget.portFiled.text())
        # settings.setValue('targetStorescp1/max_pdu', self.targetPacs1Widget.maxPduField.text())
        # settings.setValue('targetStorescp1/network_timeout', self.targetPacs1Widget.networkTimeoutField.text())
        # settings.setValue('targetStorescp1/acse_timeout', self.targetPacs1Widget.ACSETimeoutField.text())
        # settings.setValue('targetStorescp1/dimse_timeout', self.targetPacs1Widget.DIMSETimeoutField.text())

        # settings.setValue('storescu/aet', self.dicomSenderWidget.aeTitleFiled.text())
        # settings.setValue('storescu/max_pdu', self.dicomSenderWidget.maxPduField.text())
        # settings.setValue('storescu/network_timeout', self.dicomSenderWidget.networkTimeoutField.text())
        # settings.setValue('storescu/acse_timeout', self.dicomSenderWidget.ACSETimeoutField.text())
        # settings.setValue('storescu/dimse_timeout', self.dicomSenderWidget.DIMSETimeoutField.text())

        settings.setValue('storage/run', self.runFdrLineUnit.text())
        settings.setValue('storage/log', self.logFldrLineUnit.text())
        settings.setValue('storage/folder', self.storageFldrLineUnit.text())
        # settings.setValue('storage/tmp', self.tmpFldrLineUnit.text())

        # settings.setValue("conversion/folder", self.cnvDirLineEdit.text())
        # settings.setValue("conversion/format", self.cnvFmtComboBox.currentText())
        # settings.setValue("conversion/dicom_remove",self.removeDicomCheckBox.isChecked())
        foldermode = 'Study Instance UID'
        # if self.foldernamemodFld.currentIndex() == 0:
        #     foldermode = 'PatientName'
        # elif  self.foldernamemodFld.currentIndex() == 1:
        #     foldermode = 'PatientID'
        settings.setValue("storage/foldername_mode",foldermode)

        settings.sync()

    # @pyqtSlot()
    # def on_cnvDirBrowsePushButton_clicked(self):
    #     dirname = QFileDialog.getExistingDirectory()
    #     if dirname:
    #         self.cnvDirLineEdit.setText(dirname)
