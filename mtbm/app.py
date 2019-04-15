import sys
from PyQt5.QtCore import QSettings, QThread,  QDir, QSize
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QWidget
import psutil, subprocess, os, logging
from PyQt5.QtGui import QIcon
from mtbm.ipc.singletonApp import run_once
from mtbm.storage.Router import Router
from mtbm.ui import systray
import resources_rc
import images_rc

# import ipc
# # import sqlite3
# import requests
# import casesActions
# import db
# import image
# import settings
# import storage
# import ui
# ipc
# #sqlite3
# requests
# casesActions
# db
# image
# settings
# storage
# ui


basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, "..", ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)


def setup_router(app):
    router = Router(app)
    app.router = router
    app.setProperty("router", Router(router))


def main():
    # if check_activation() != True:
    #     return
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    def setup_app_data():
        print("SETUP APP DATA")
        settings = QSettings(".vendor.ini", QSettings.IniFormat)
        settings.setIniCodec("UTF-8")
        app.setOrganizationName(settings.value("org/name"))
        app.setOrganizationDomain(settings.value("org/domain"))
        app.setApplicationDisplayName((settings.value("app/displayName")))
        app.setApplicationName(settings.value("app/name"))
        app.setApplicationVersion(settings.value("app/version"))

    setup_app_data()


    from mtbm.settings import settings
    settings.setup()

    logger = setup_logging()
    setup_pynetdicom_logging()

    from mtbm.db import db
    db.setup()

    ok, server, port = run_once()
    if ok:
        logger.info("App started, IPC server on port {port}".format(port=port))
    else:
        logger.fatal("App already running, IPC server on port {port}".format(port=port))
        sys.exit(-10)

    proc = None
    if sys.platform.startswith('win'):
        if os.path.exists("dicom_converting_process.exe"):
            proc = subprocess.Popen("dicom_converting_process.exe")



    from mtbm.storage import storage
    storage.setup()
    st = storage.run_pythread()

    setup_router(app)


    from mtbm.ui import ui
    ui.setup()
    mainwindow = ui.run()
    app.setProperty("mainwindow", mainwindow)
    app.setWindowIcon(QIcon(":/images/app_icon.png"))

    tray = systray.setup(mainwindow.actionShow_DicomRouter, mainwindow.actionImport, mainwindow.action_Quit)
    app.setProperty("tray", tray)

    # from casesActions import StudyPostProcessor
    # studyPost = StudyPostProcessor.setup()

    from mtbm.casesActions import dataset_actions
    dataset_actions.setup()

    e = app.exec_()
    st.stop()
    try:
        if sys.platform.startswith('win'):
            if proc is not None:
                kill_proc_tree(proc.pid)
    except OSError as e:
        print("Conversion Process Error : error no.", e.errorno)
    sys.exit(0)

def kill_proc_tree(pid , including_parent = True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()

def setup_pynetdicom_logging():
    pynetdicom_logger = logging.getLogger("pynetdicom")
    # create file handler
    s = QSettings()
    if not os.path.exists(s.value("storage/folder")):
        os.makedirs(s.value("storage/folder"))
        # print(s.value("storage/folder") + QDir.separator() + "beamdicom.log")
    pynetdicom_logger_handler = logging.FileHandler(s.value("storage/folder") + QDir.separator() + "pynetdicom.log")
    pynetdicom_logger.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    pynetdicom_logger_handler.setFormatter(formatter)
    # add handler to logger
    pynetdicom_logger.addHandler(pynetdicom_logger_handler)
    # disable pynetdicom logging
    # pynetdicom_logger.disabled = False
    return pynetdicom_logger


def setup_logging():
    logger = logging.getLogger('beamdicom')
    s = QSettings()
    print(s.value("storage/folder"))
    if not os.path.exists(s.value("storage/folder")):
        os.makedirs(s.value("storage/folder"))
    # print(s.value("storage/folder") + QDir.separator() + "beamdicom.log")
    handler = logging.FileHandler(s.value("storage/folder") + QDir.separator() + "beamdicom.log")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s.%(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Set up Logging Complete')
    return logger




if __name__ == '__main__':
    main()