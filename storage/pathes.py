from PyQt5.QtCore import QSettings, QDir
from PyQt5.QtSql import QSqlQuery


def _study__patient_last_name(record):
    return record.value("name")

# _study_id();

def _study_folder_name(study_iuid):
    return study_iuid


def convention_name():
    settings = QSettings()
    mode = settings.value("storage/foldername_mode")
    modes = {"", ""}
    modes[mode];
    query = QSqlQuery()
    query.prepare("SELECT * FROM "\
                  "study JOIN patient ON study.patient_id = patient.patient_id "\
                  "WHERE study_iuid=:study_iuid")
    query.bindValue("study_iuid")
    query.exec()
    ok = query.next()
    # modes = {"Last Name": "", "Patient ID", "Date"}
    # return study_iuid

def study_files_path(study_iuid):
    settings = QSettings()
    folder = settings.value('storage/folder')
    folder = folder.replace("/", QDir.separator())
    folder = folder.replace("\\", QDir.separator())
    foldername = folder + QDir.separator() + _study_folder_name(study_iuid)
    return foldername

def study_images_path(study_iuid):
    settings = QSettings()
    folder = settings.value('conversion/folder')
    folder = folder.replace("/", QDir.separator())
    folder = folder.replace("\\", QDir.separator())
    foldername = folder + QDir.separator() + _study_folder_name(study_iuid)
    return foldername

def get_folder_mode():
    s = QSettings()
    return s.value('storage/foldername_mode')

def get_storage_folder():
    settings = QSettings()
    folder = settings.value('storage/folder')
    folder = folder.replace("/", QDir.separator())
    folder = folder.replace("\\", QDir.separator())
    return folder

def get_images_folder():
    settings = QSettings()
    folder = settings.value('conversion/folder')
    folder = folder.replace("/", QDir.separator())
    folder = folder.replace("\\", QDir.separator())
    return folder