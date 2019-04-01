
from PyQt5.QtCore import QSettings, QThread, QUrl, QFileInfo, QProcess, QDir,qRegisterResourceData
from PyQt5.QtWidgets import QApplication, QWidget,QVBoxLayout, QScrollArea
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import  QQuickView
from PyQt5 import QtQuick ,QtQml, QtQuickWidgets

import sys
import os

from storage.pathes import get_folder_mode, get_storage_folder
from studyImageViewer.ConvertedPdfImageProvider import ConvertedPdfImageProvider

def viewImages(study_iuid):
  foldername = pathes.study_images_path(study_iuid)

  engine = QQmlApplicationEngine()
  engine.rootContext().setContextProperty("imagesFolder", foldername);
# //  engine.load(QUrl(QLatin1String("qrc:/main.qml")));
#   engine.load(QUrl(QLatin1String("../studyImageViewer/main.qml")));
  engine.load(QUrl("../studyImageViewer/main.qml"))
  viewImages.dump.append(engine)
  return engine

viewImages.dump = []

from storage import pathes

def open_study_images(study_iuid):
  # storage.
  foldername = pathes.study_images_path(study_iuid)
  if "win32" == sys.platform:
    process = QProcess.startDetached("explorer", [foldername])
    tmpList.append(process)
  else:
    QDesktopServices.openUrl(QUrl(foldername))

def open_study_files(study_iuid):
  mode = get_folder_mode()
  if mode == 'PatientID':
    foldername = get_storage_folder() + QDir.separator() + str(study_iuid)
  elif mode == 'PatientName':
    foldername = get_storage_folder() + QDir.separator() + str(study_iuid)
  else:
    foldername = pathes.study_files_path(study_iuid)
  if "win32" == sys.platform:
    process = QProcess.startDetached("explorer", [foldername])
    tmpList.append(process)
  else:
    QDesktopServices.openUrl(QUrl(foldername))

def viewImages(study_iuid, patient_id, patient_name):
  foldername = pathes.study_images_path(study_iuid)
  foldername = QFileInfo(foldername).absoluteFilePath()
  # QDesktopServices.openUrl(QUrl(foldername))

  # foldername = '/home/melnaquib/work/freelancer.com/joshua/dicom_router/run/images/1.2.826.0.1.368043.2.206.20170330073520.725846087/'
  # foldername = '/home/melnaquib/work/freelancer.com/joshua/dicom_router/test/data/example_output_pdf'

  imgdir = QDir(foldername)

  files = [finfo.fileName() for finfo in imgdir.entryInfoList(QDir.Files)]
  files = list(files)

  engine = QQmlApplicationEngine()

  provider = ConvertedPdfImageProvider()
  engine.addImageProvider('imgpdf', provider)

  engine.rootContext().setContextProperty("imagesFolder", imgdir.absolutePath())
  engine.rootContext().setContextProperty("patientID", patient_id)
  patient_name = str(patient_name).replace('^', ' ')
  # print("Id= ",patient_id , " , patient name = " , patient_name)
  engine.rootContext().setContextProperty("patientName", patient_name)

  engine.rootContext().setContextProperty("files", files)

  engine.load(QUrl("./studyImageViewer/main.qml"))

  viewImages.l.append(engine)
  return engine

viewImages.l = []

  #QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    # QString folderName = argc > 1 ? argv[1] : "/usr/share/backgrounds/gnome/";

    # app = QGuiApplication(argc, argv);


  # //  engine.load(QUrl(QLatin1String("qrc:/main.qml")));
  #   engine.load(QUrl(QLatin1String("../studyImageViewer/main.qml")));

    # return app.exec();


tmpList = []

def application_path(*paths):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *paths)

class MainWindow(QtQuick.QQuickWindow):
  def __init__(self):
    super(MainWindow, self).__init__()

    self._engine = QtQml.QQmlEngine(self)
    if not self._engine.incubationController():
      self._engine.setIncubationController(self.incubationController())



  def setSource(self, url):
    context = QtQml.QQmlContext(self._engine)

    component = QtQml.QQmlComponent(self._engine)

    component.loadUrl(url)

    if component.isError():
      print(component.errorString())
      return

    obj = component.create(context)

    if component.isError():
      print(component.errorString())
      return

    if isinstance(obj, QtQuick.QQuickItem):
      obj.setParentItem(self.contentItem())
      self._root = obj
