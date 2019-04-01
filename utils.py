from PyQt5.QtCore import QDir
import os

def storagefoldername(study_uuid):
    from PyQt5.QtCore import QSettings
    settings = QSettings()
    settings.beginGroup('storage')
    storage_foldername = settings.value('folder')
    foldername = storage_foldername + QDir.separator() + study_uuid
    return foldername

def dicomfiles(study_uuid):
    path = storagefoldername(study_uuid)
    fnames = []
    if not os.path.exists(path):
        return
    for root, dirs, files in os.walk(path):
        for name in files:
            fnames.append(os.path.join(root, name))
    return fnames

from storage.pathes import get_folder_mode, get_storage_folder
from PyQt5.QtCore import QFileInfo
import subprocess
import logging
logger = logging.getLogger('dicomrouter')
def create_patient_symbolic_link(study_folder, patient_id, patient_name):
    folder_mode = get_folder_mode()
    storage_folder = get_storage_folder()
    if os.path.exists(storage_folder):
        target_folder = ''
        if folder_mode =='PatientID':
            target_folder = storage_folder + QDir.separator() + str(patient_id)
        elif folder_mode =='PatientName':
            target_folder = storage_folder + QDir.separator() + str(patient_name)
        src_folder = QFileInfo(study_folder).absoluteFilePath()
        target_folder = QFileInfo(target_folder).absoluteFilePath()
        if not os.path.exists(target_folder):

            try:
                os.system('mklink /J "{}" "{}"'.format(target_folder, src_folder))
                # subprocess.call('mklink2 /J "{}" "{}"'.format(tar_folder, src_folder))
            except subprocess.CalledProcessError:
                logger.warning('Can not create symbolic link for study folder: ',study_folder)
            except OSError:
                logger.warning('Can not create symbolic link for study folder: ', study_folder)
            except :
                print('**********************************************')
                logger.warning('Can not create symbolic link for study folder: ', study_folder)


from storage.pathes import study_files_path

def study_dicom_files(study_uuid):
    path = study_files_path(study_uuid)
    for root, dirs, files in os.walk(path):
        for name in files:
            yield os.path.join(root, name)

def get_ip_address():
    from PyQt5.QtNetwork import QNetworkInterface, QAbstractSocket
    all_Interfaces = QNetworkInterface.allInterfaces()
    inter_list = list()
    for addr in all_Interfaces:
        if (addr.flags() & (QNetworkInterface.IsUp) and not (addr.flags() & (QNetworkInterface.IsLoopBack))):
            for entry in addr.addressEntries():
                if (entry.ip().protocol() == QAbstractSocket.IPv4Protocol):
                    inter_list.append(entry.ip().toString())
    return inter_list