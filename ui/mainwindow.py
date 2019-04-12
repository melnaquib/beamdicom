# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot,QModelIndex,QTimer,QPoint, Qt, QItemSelectionModel,QDate, QSortFilterProxyModel, QSize, QFileInfo, QDir
from PyQt5.QtWidgets import QMainWindow, QDialog, QGridLayout, qApp, QHeaderView, QMenu, QAction, QAbstractItemView, \
    QTableView, QWidget, QListView, QFileDialog, QLabel, QStyledItemDelegate, QApplication
from PyQt5.QtSql import QSqlQueryModel, QSqlRecord, QSqlQuery, QSqlTableModel
from PyQt5.QtGui import QPixmap, QIcon, QColor
import sys, os, shutil
import pydicom
from numpy.core.records import record

from storage import pathes
from casesActions.study_actions import on_study
from ui.SqlTableView import SqlTableView
from ui.StudiesProxyModel import StudiesProxyModel
from ui.Ui_mainwindow import Ui_MainWindow
from pydicom.dataset import Dataset, FileDataset
# from pynetdicom3 import pynetdicom_uid_prefix
from studyImageViewer import viewImages

import images_rc

from ui.StudyItemDelegate import StudyItemDelegate
from ui.HtmlContent import HtmlContent
_UPDATEUI_TIMEOUT = 15000
_BASIC_SQL_QUERY = """
SELECT 
patient.name AS 'Name',
patient.patient_id AS 'ID',
study.thumbnail,
(select count(sop.sop_iuid) from sop where sop.series_iuid in( select serie.series_iuid from serie  where serie.study_iuid = study.study_iuid) ) AS 'Total Case Images' ,
study.datetime AS 'Date',
CASE when study.to_image =1  and to_pacs = 1 THEN
            'Converted and Sent'
        WHEN to_image = 1 and to_pacs = 0 then
            'Converted'
		        WHEN to_image = 0 and to_pacs = 1 then
            'Sending'
			else 
			''
        END
'Status',
study.study_iuid AS study_iuid,
'A\nB\nC' AS BRIEF,
(SELECT COUNT(st2.id) FROM study st2 WHERE st2.id < study.id AND study.patient_id = st2.patient_id) AS SEQ

FROM 
study
JOIN patient on study.patient_id = patient.patient_id

 """
_BASIC_SQL_QUERY_GROUP = " GROUP BY study.study_iuid"
_BASIC_SQL_QUERY_WHERE = " WHERE workflow_phase = 0 "

_TOTAL_CASES = " select count(study.study_iuid) from study "
_TOTAL_IMAGES = """select count(sop.sop_iuid) 
from  sop   where sop.series_iuid in ( select serie.series_iuid from serie ,  study where 
serie.study_iuid = study.study_iuid and study.to_image = 1  )"""

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.tableContextMenu = QMenu()
        self.tableContextMenu.addAction(self.actionView_Images)
        # self.tableContextMenu.addAction(self.actionOpen_Images_Folder)
        # self.tableContextMenu.addAction(self.actionOpen_Study_Folder)
        self.tableContextMenu.addSeparator()
        self.tableContextMenu.addAction(self.actionDelete_Study_Folder)

        self.studiesModel = QSqlQueryModel()
        sql_str = _BASIC_SQL_QUERY +  _BASIC_SQL_QUERY_WHERE + _BASIC_SQL_QUERY_GROUP
        self.studiesModel.setQuery(sql_str)
        s = self.studiesModel.query().lastError().text()

        self.proxyModel = StudiesProxyModel(self)
        self.proxyModel.setSourceModel(self.studiesModel)
        self.proxyModel.sort(0, Qt.AscendingOrder)

        self.studiesTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.studiesTableView.setModel(self.proxyModel)
        # self.studiesTableView.hideColumn(4)
        # self.studiesTableView.hideColumn(2)
        self.studiesTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.studiesTableView.horizontalHeader().setStretchLastSection(True)
        self.studiesTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.studiesTableView.horizontalHeader().resizeSection(0,300)
        self.studiesTableView.horizontalHeader().resizeSection(1, 300)
        self.studiesTableView.horizontalHeader().resizeSection(3, 200)
        self.studiesTableView.resizeEvent = self.resizeColumn

        self.studiesTableView.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
        self.studiesTableView.setSortingEnabled(True)
        self.studiesTableView.sortByColumn(3,1)
        self.studiesTableView.setSortingEnabled(True)
        self.studiesTableView.sortByColumn(0, Qt.AscendingOrder)

        # self.studiesListView.setModel(self.proxyModel)

        self.studiesBriefTableView.setModel(self.proxyModel)
        self.hidecols()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateui)
        self.timer.setSingleShot(False)
        self.timer.start(_UPDATEUI_TIMEOUT)

        # self.searchBtn.clicked.connect(self.search)
        # self.cancelBtn.clicked.connect(self.cancel_search)






        # self.patientIDSearchFld.returnPressed.connect(self.search)
        # self.patientNameSearchFld.returnPressed.connect(self.search)

        self.set_cases_images_count()

        self.menuBar.hide()
        self.setAcceptDrops(True)

        # for i in range(self.studyView.model().columnCount() - 1, 0, -1):
        #     self.studyView.hideColumn(i)
        self.studyItemDelegate = StudyItemDelegate()

        # self.studiesListView.setItemDelegate(self.studyItemDelegate)
        # self.studiesListView.setFlow(QListView.LeftToRight)
        # self.studiesTableView.setItemDelegateForColumn(2, ImageDelegate(self))
        # self.studiesListView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.studiesTableView.verticalHeader().hide()

        self.aboutDialog = HtmlContent(self)
        self.helpDialog = HtmlContent(self)
        self.licenseDialog = HtmlContent(self)


        self.routeTable = SqlTableView(self)
        self.studiesStackedWidget.addWidget(self.routeTable)
        self.routeTable.setModel(qApp.property("router").routesModel())


    def hidecols(self):
        col_count = self.studiesBriefTableView.model().columnCount()
        for i in range(col_count - 1, -1, -1):
            if i in StudiesProxyModel.brief_cols.values():
                self.studiesTableView.hideColumn(i)
            else:
                self.studiesBriefTableView.hideColumn(i)

        for i in [col_count - 1]:
            self.studiesTableView.hideColumn(i)
            self.studiesBriefTableView.hideColumn(i)

                        # self.studiesTableView.hideColumn(6)

    def activeViewTable(self):
        if self.studiesStackedWidget.currentIndex():
            return self.studiesTableView
        return self.studiesBriefTableView

    def updateui(self):
        scroll = self.activeViewTable().verticalScrollBar()
        if scroll.value():
            return

        queryStr = self.studiesModel.query().executedQuery()
        self.studiesModel.clear()
        self.studiesModel.query().clear()
        self.studiesModel.setQuery(queryStr)
        self.studiesTableView.hideColumn(2)
        self.set_cases_images_count()

        self.hidecols()

    def set_cases_images_count(self):
        return
        query = QSqlQuery()
        query.exec(_TOTAL_CASES)
        # while (query.next()):
        #     self.totalCasesLabel.setText('Total Cases : ' + str(query.value(0)))
        query.exec(_TOTAL_IMAGES)
        # while (query.next()):
        #     self.totalImagesLabel.setText('Total Images : ' + str(query.value(0)))

    @pyqtSlot()
    def on_action_Settings_triggered(self):
        from ui.SettingsWidget import SettingsWidget
        from ui.WrapperDialog import WrapperDialog
        dlg = WrapperDialog()
        dlg.setWidget(SettingsWidget())
        dlg.exec_()

    @pyqtSlot(QModelIndex)
    def on_studiesTableView_doubleClicked(self,index):
        # study_iuid = self.get_study_iuid(index)
        # viewImages.open_study_images(study_iuid)
        study_iuid = self.get_study_iuid_new(index)
        patient_id = self.get_patient_id(index)
        patient_name = self.get_patient_name(index)
        # if StudiesProxyModel.brief_cols['thumbnail'] == index.column():
        #     print("Thumbnail")
        viewImages.viewImages(study_iuid,patient_id,patient_name)

    @pyqtSlot(QPoint)
    def on_studiesTableView_customContextMenuRequested(self, point):
        self.tableContextMenu.exec_(self.studiesTableView.mapToGlobal(point))

    # @pyqtSlot(QPoint)
    # def on_studiesListView_customContextMenuRequested(self, point):
    #     self.tableContextMenu.exec_(self.studiesListView.mapToGlobal(point))

    def get_study_iuid(self, index):
        if not index:
            return ""
        proxy_index = self.proxyModel.mapToSource(index)
        row = proxy_index.row()
        record = self.studiesModel.record(row)
        from storage.pathes import get_folder_mode
        mode = get_folder_mode()
        if mode =='PatientID':
            column_name = 'ID'
        elif mode == 'PatientName':
            column_name = 'NAME'
        else:
            column_name = 'study_iuid'
        print('row : ',row)
        # record = QSqlRecord()
        # for i in range(record.count()):
        #     print(record.fieldName(i))
        # study_iuid = record.value(record.count() - 1)
        study_iuid = record.value(column_name)
        return study_iuid

    def get_study_iuid_new(self, index):
        if not index:
            return ""
        proxy_index = self.proxyModel.mapToSource(index)
        row = proxy_index.row()
        record = self.studiesModel.record(row)
        column_name = 'study_iuid'
        print('row : ',row)
        study_iuid = record.value(column_name)
        return study_iuid

    @pyqtSlot()
    def on_action_Exit_triggered(self):
        self.close()

    @pyqtSlot()
    def on_action_Quit_triggered(self):
        qApp.quit()

    @pyqtSlot()
    def on_actionView_Images_triggered(self):
        study_iuid = self.get_selected_study_iuid_new()
        patient_id = self.get_selected_patient_id()
        patient_name = self.get_selected_patient_name()
        print('View Images, patient id : {} , patient name : {}'.format(patient_id , patient_name))
        if study_iuid == '':
            return
        viewImages.viewImages(study_iuid,patient_id, patient_name)

    @pyqtSlot()
    def on_actionOpen_Images_Folder_triggered(self):
        study_iuid = self.get_selected_study_iuid()
        viewImages.open_study_images(study_iuid)

    @pyqtSlot()
    def on_actionOpen_Study_Folder_triggered(self):
        study_iuid = self.get_selected_study_iuid()
        viewImages.open_study_files(study_iuid)

    @pyqtSlot()
    def on_actionDelete_Study_Folder_triggered(self):
        indexes = self.studiesTableView.selectedIndexes()
        index = indexes[0] if indexes else None
        if not index:
            return ""
        proxy_index = self.proxyModel.mapToSource(index)
        row = proxy_index.row()
        record = self.studiesModel.record(row)
        study_iuid = record.value('study_iuid')
        print("Delete Study iuid : ".format(study_iuid))
        from storage import workflow
        workflow.study_hide(study_iuid)


    def get_selected_study_iuid(self):
        indexes = self.studiesTableView.selectedIndexes()
        index = indexes[0] if indexes else None
        study_iuid = self.get_study_iuid(index)
        return study_iuid

    def get_selected_study_iuid_new(self):
        indexes = self.studiesTableView.selectedIndexes()
        index = indexes[0] if indexes else None
        study_iuid = self.get_study_iuid_new(index)
        return study_iuid

    def get_selected_patient_id(self):
        indexes = self.studiesTableView.selectedIndexes()
        index = indexes[0] if indexes else None
        patient_id = self.get_patient_id(index)
        return patient_id

    def get_patient_id(self, index):
        if not index:
            return ""
        proxy_index = self.proxyModel.mapToSource(index)
        row = proxy_index.row()
        record = self.studiesModel.record(row)
        column_name = 'ID'
        patient_id = record.value(column_name)
        return patient_id

    def get_selected_patient_name(self):
        indexes = self.studiesTableView.selectedIndexes()
        index = indexes[0] if indexes else None
        patient_name = self.get_patient_name(index)
        return patient_name

    def get_patient_name(self, index):
        if not index:
            return ""
        proxy_index = self.proxyModel.mapToSource(index)
        row = proxy_index.row()
        record = self.studiesModel.record(row)
        column_name = 'Name'
        patient_name = record.value(column_name)
        return patient_name

    # findButton.clicked.connect(lambda: self.find(findField.text()))
    def find(self, text, column = 1):
        model = self.studiesTableView.model()
        start = model.index(0, column)
        matches = model.match(
            start, Qt.DisplayRole,
            text, 1, Qt.MatchContains)
        if matches:
            index = matches[0]
            # index.row(), index.column()
            self.table.selectionModel().select(
                index, QItemSelectionModel.Select)
            indexes = self.table.selectionModel().selectedIndexes()

    def search(self):
        queryStr = _BASIC_SQL_QUERY + _BASIC_SQL_QUERY_WHERE
        if self.patientIDSearchFld.text() != '':
            queryStr = _BASIC_SQL_QUERY + " and study.patient_id = '" + self.patientIDSearchFld.text() + "'"
        if self.patientNameSearchFld.text() != '':
            queryStr = queryStr + " and patient.name like '%"+self.patientNameSearchFld.text()+"%'"

        queryStr = queryStr + " GROUP BY study.study_iuid"
        self.proxyModel.sourceModel().query().clear()
        self.proxyModel.sourceModel().setQuery(queryStr)

    def cancel_search(self):
        self.patientNameSearchFld.setText('')
        self.patientIDSearchFld.setText('')

        queryStr = _BASIC_SQL_QUERY + _BASIC_SQL_QUERY_WHERE + _BASIC_SQL_QUERY_GROUP
        print(queryStr)
        self.proxyModel.sourceModel().query().clear()
        self.proxyModel.sourceModel().setQuery(queryStr)

    # @pyqtSlot()
    # def on_actionSwitch_View_toggled(self, checked):
    #     print('on_actionSwitch_View_toggled')
    #     tabIndex = 1 if checked else 0
    #     self.studiesStackedWidget.setCurrentIndex(tabIndex)

    @pyqtSlot(bool)
    def on_actionSwitch_View_triggered(self, checked):
        tabIndex = 1 if checked else 0
        self.studiesStackedWidget.setCurrentIndex(tabIndex)


    @pyqtSlot()
    def on_action_DragDrop_triggered(self):
        from ui.dragdropbtn import Button
        from ui.WrapperDialog import WrapperDialog
        dlg = WrapperDialog()
        btn = Button(self)
        btn.setIcon(QIcon(":/resources/drag.png"))
        btn.setIconSize(QSize(100, 100))
        dlg.setWidget(btn)
        dlg.exec_()

    @pyqtSlot()
    def on_action_About_triggered(self):
        self.aboutDialog.setContentFromFile("qrc:/res/about.html")
        self.aboutDialog.textBrowser.setOpenExternalLinks(True)
        self.aboutDialog.setWindowTitle("About Us")
        self.aboutDialog.show()

    @pyqtSlot()
    def on_action_License_triggered(self):
        self.licenseDialog.setContentFromFile("qrc:/res/license.html")
        self.licenseDialog.setWindowTitle("License")
        self.licenseDialog.show()

    @pyqtSlot()
    def on_action_Help_triggered(self):
        self.helpDialog.setContentFromFile("qrc:/res/help.html")
        self.helpDialog.textBrowser.setOpenExternalLinks(True)
        self.helpDialog.setWindowTitle("Help")
        self.helpDialog.show()

    @pyqtSlot()
    def on_actionImport_triggered(self):
        from PyQt5.QtWidgets import QFileDialog
        import os
        my_dir = QFileDialog.getExistingDirectory(
            self,
            "Select DICOM Folder",
            os.getcwd(),
            QFileDialog.ShowDirsOnly
        )
        if my_dir:
            print("dir selected : ",my_dir)
            folder = my_dir.replace("/", QDir.separator())
            folder = folder.replace("\\",QDir.separator())
            self.process_dcm_file([folder])



    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(MainWindow, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(MainWindow, self).dragMoveEvent(event)


    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files_paths = []
            for url in event.mimeData().urls():
                file = url.toLocalFile()
                files_paths.append(QFileInfo(file).absoluteFilePath())
            self.process_dcm_file(files_paths)
            event.acceptProposedAction()
        else:
            super(MainWindow,self).dropEvent(event)

    def process_dcm_file(self,files_paths):
        tmp_files = list()
        for file in files_paths:
            if QFileInfo(file).isDir():
                for root, dirs, files in os.walk(file):
                    for name in files:
                        self.save_dcm_file(os.path.join(root, name))
                        tmp_files.append(os.path.join(root, name))
            else:
                self.save_dcm_file(file)
                tmp_files.append(file)
        self.delete_tmp_files(tmp_files)

    def delete_tmp_files(self,tmp_files):
        from PyQt5.QtCore import QSettings
        settings = QSettings()
        tmp_folder = settings.value('storage/tmp')
        if tmp_folder:
            for tmp_file in tmp_files:
                try:
                    print(tmp_folder + QDir.separator() + os.path.basename(tmp_file))
                    os.remove(tmp_folder + QDir.separator() + os.path.basename(tmp_file))
                except Exception :
                    print("Error In Remove Tmp Files")

    def save_dcm_file(self, file):
        from PyQt5.QtCore import QSettings
        settings = QSettings()
        tmp_folder = settings.value('storage/tmp')
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        try:
            shutil.copy(file,tmp_folder)
        except FileNotFoundError as e:
            print("Can not import File ",e.filename )
            return
        except PermissionError as pr:
            print("Permission Error")
            return
        except OSError as ose :
            print("Os Error")
        print(file , tmp_folder)
        print(os.path.basename(file))
        try:
            dataset = pydicom.read_file(tmp_folder + QDir.separator() + os.path.basename(file))
        except pydicom.errors.InvalidDicomError:
            print('Not DICOM IMAGE')
            return
        except PermissionError:
            print('Permission Error')
            return
        except OSError :
            print(" OS Error")
            return
        study_iuid = dataset.StudyInstanceUID
        foldername = pathes.study_files_path(study_iuid)
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        #
        filename = foldername + QDir.separator() + str(dataset.SOPInstanceUID)
        if sys.platform.startswith('win'):
            from utils import create_patient_symbolic_link
            create_patient_symbolic_link(foldername, dataset.PatientID, dataset.PatientName)

        meta = Dataset()
        meta.MediaStorageSOPClassUID = dataset.SOPClassUID
        meta.MediaStorageSOPInstanceUID = dataset.SOPInstanceUID
        vendor_settings = QSettings(".vendor.ini", QSettings.IniFormat)
        vendor_settings.setIniCodec("UTF-8")
        impl_class_uid_root = vendor_settings.value("dicom/OID")
        ver = vendor_settings.value("app/version")
        app_number = '3'  # meaniniglessly chosen
        meta.impl_class_uid = impl_class_uid_root + app_number + '.' + ver
        meta.ImplementationClassUID = impl_class_uid_root + app_number + '.' + ver



        ds = FileDataset(filename, {}, file_meta=meta, preamble=b"\0" * 128)
        ds.update(dataset)

        ds.is_little_endian = True
        ds.is_implicit_VR = True

        try:
            ds.save_as(filename)
            print("File %s written", filename)
        except IOError:
            print('SAVE FAILED! FILE: ', filename)
            print('SAVE FAILED! FILE: ', filename)
            return 0xA700  # Failed - Out of Resources
        except:
            return 0xA700  # Failed - Out of Resources
        # print(filename)
        from casesActions import dataset_actions
        dataset_actions.on_dataset(pydicom.read_file(filename))

    def resizeColumn(self, event):
        """ Resize all sections to content and user interactive """
        self.studiesTableView.horizontalHeader().setStretchLastSection(True)
        self.studiesTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.studiesTableView.horizontalHeader().resizeSection(0, 300)
        self.studiesTableView.horizontalHeader().resizeSection(1, 300)
        self.studiesTableView.horizontalHeader().resizeSection(3, 150)
        self.studiesTableView.horizontalHeader().resizeSection(4, 200)


    @pyqtSlot(QModelIndex)
    def on_studiesBriefTableView_doubleClicked(self,index):
        study_iuid = self.get_study_iuid_new(index)
        patient_id = self.get_patient_id(index)
        patient_name = self.get_patient_name(index)
        # if StudiesProxyModel.brief_cols['thumbnail'] == index.column():
        #     print("Thumbnail")
        viewImages.viewImages(study_iuid,patient_id,patient_name)
        # else:
        #     viewImages.open_study_images(study_iuid)


    @pyqtSlot(bool)
    def on_rou_tes_ViewAction_toggled(self, value):
        idx = 2 if value else 0
        self.studiesStackedWidget.setCurrentIndex(idx)


class FileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)

    def accept(self):
        super(FileDialog, self).accept()

class ImageDelegate(QStyledItemDelegate):

    def __init__(self, parent):

        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        painter.fillRect(option.rect, QColor(191,222,185))
        srcIndex = index.model().mapToSource(index)
        record = srcIndex.model().record(srcIndex.row())
        if isinstance(record, QSqlRecord):
            byte_array = record.value("thumbnail")
            if byte_array:
                pixmap = QPixmap()
                print(pixmap.loadFromData(byte_array, "PNG", Qt.AutoColor))

                pixmap.scaled(500, 500, Qt.KeepAspectRatio)
                painter.drawPixmap(option.rect, pixmap)

    def sizeHint(self, option, index):
        result = QSize(option.rect.width(), 1000)
        return result
