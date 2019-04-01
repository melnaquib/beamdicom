from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from casesActions.dataset_actions import CaseState

import shutil
from storage import pathes
from storage.pathes import get_folder_mode, get_storage_folder, get_images_folder
from PyQt5.QtCore import QDir, QSettings
import logging
import os
logger = logging.getLogger(__name__)

WORKFLOW_PHASE_HIDE = 10

def study_db_delete(study_iuid):
    sql_delete_patient = " DELETE FROM patient WHERE patient_id  = ( SELECT patient_id FROM study WHERE study_iuid = '{study_iuid}')"
    sql_delete_serie = " DELETE FROM serie WHERE study_iuid =  '{study_iuid}'  "
    sql_delete_sop = " DELETE FROM sop WHERE series_iuid in (SELECT series_iuid from serie WHERE study_iuid = '{study_iuid}')  "
    sql_delete_study = "DELETE FROM study WHERE study_iuid =  '{study_iuid}' "
    sql_list = [sql_delete_sop, sql_delete_serie, sql_delete_patient, sql_delete_study]
    for sql_delete in sql_list:
        sql_str = sql_delete.format(study_iuid=study_iuid)
        query = QSqlQuery(sql_str)
        ok = query.exec_()
    return ok

def study_hide(study_iuid):
    print('study _hide')
    ok = study_db_hide(study_iuid)
    patient_id, patient_name = get_patient(study_iuid)
    if ok:
        settings = QSettings()
        remove_dicom = settings.value("conversion/dicom_remove")
        if remove_dicom == 'true' :
            study_files_del(study_iuid)
            delete_study_image_symbolic_link(study_iuid, patient_id, patient_name, True)

        study_images_files_del(study_iuid)
        delete_study_image_symbolic_link(study_iuid, patient_id, patient_name, False)



def study_db_hide(study_iuid):
    sql_str = "UPDATE study SET workflow_phase = {workflow_phase} WHERE study_iuid = '{study_iuid}'"
    sql_str = sql_str.format(study_iuid=study_iuid, workflow_phase=WORKFLOW_PHASE_HIDE)

    query = QSqlQuery(sql_str)
    ok = query.exec_()
    return ok

def study_files_del(study_iuid):
    dir_to_del = pathes.study_files_path(study_iuid)
    try:
        shutil.rmtree(dir_to_del)
    except Exception as e:
        logger.exception("Error on deleting study {study_iuid} files in path {dir_to_del}".
                         format(study_iuid=study_iuid, dir_to_del=dir_to_del))
        return False
    return True

def study_images_files_del(study_iuid):
    dir_to_del = pathes.study_images_path(study_iuid)
    try:
        shutil.rmtree(dir_to_del)
    except Exception as e:
        logger.exception("Error on deleting study {study_iuid} images in path {dir_to_del}".
                         format(study_iuid=study_iuid, dir_to_del=dir_to_del))
        return False
    return True

def study_del(study_iuid):
    ok = study_files_del(study_iuid)
    patient_id, patient_name = get_patient(study_iuid)
    delete_study_image_symbolic_link(study_iuid,patient_id,patient_name,True)
    # if not ok:
    #     return False
    ok = study_db_delete(study_iuid)
    # if not ok:
    #     return False
    study_images_files_del(study_iuid)
    delete_study_image_symbolic_link(study_iuid, patient_id, patient_name, False)

    return True

def delete_study_image_symbolic_link(study_iuid,patient_id,patient_name,delete_study):
    print(study_iuid)
    folder_mode = get_folder_mode()
    if delete_study:
        storage_folder = get_storage_folder()
    else:
        storage_folder = get_images_folder()


    if folder_mode == 'PatientID':
        target_folder = storage_folder + QDir.separator() + str(patient_id)
    elif folder_mode == 'PatientName':
        target_folder = storage_folder + QDir.separator() + str(patient_name)
    else:
        target_folder = storage_folder + QDir.separator() + str(study_iuid)
    try:
        os.remove(target_folder)
    except Exception as ex:
        print("can not remove Symbolic link")


def get_patient(study_iuid):
    sql_str = "SELECT patient_id, name from patient WHERE patient_id = (SELECT patient_id FROM study WHERE study_iuid = '{study_iuid}')"
    sql_str = sql_str.format(study_iuid=study_iuid)
    query = QSqlQuery(sql_str)
    query.first()

    if query.isValid():
        patient_id = query.value(0)
        print('patient id ', patient_id)
        patient_name = query.value(1)
        return (patient_id,patient_name)