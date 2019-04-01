
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError
from pydicom.dataset import Dataset
from PyQt5.QtCore import QVariant, QDateTime

from enum import Enum
import logging, sys

logger = logging.getLogger('dicomrouter')

class CaseState(Enum):
    NEW = 0
    RECIEVED = 1
    FORWARDED = 2
    CONVERTED = 4

def patient_log(dataset):
    patient_log.query.finish()
    patient_log.query.bindValue(':patient_id', dataset.PatientID)
    patient_log.query.bindValue(':name', str(dataset.PatientName))
    patient_log.query.bindValue(':dob', str(dataset.PatientBirthDate))
    patient_log.query.bindValue(':gender', dataset.PatientSex)
    return patient_log.query.exec_()

def study_log(dataset,thumbnail):
    study_log.query.finish()
    study_log.query.bindValue(':study_iuid', str(dataset.StudyInstanceUID))
    study_log.query.bindValue(':patient_id', dataset.PatientID)
    study_log.query.bindValue(':datetime', str(dataset.StudyDate))
    study_log.query.bindValue(':accession_no', dataset.AccessionNumber)
    study_log.query.bindValue(':status', CaseState.NEW.value)
    study_log.query.bindValue(':thumbnail', thumbnail)
    study_log.query.bindValue(':update_timestamp', QDateTime.currentDateTime().toMSecsSinceEpoch() / 1000)
    _STUDY_UPDATE_QUERY_STR = "UPDATE OR IGNORE study set `update_timestamp` = {update_timestamp}  , to_image = 0 ,  workflow_phase = 0  WHERE study_iuid = '{study_iuid}'"
    _STUDY_UPDATE_QUERY_STR = _STUDY_UPDATE_QUERY_STR.format(study_iuid=str(dataset.StudyInstanceUID),update_timestamp=QDateTime.currentDateTime().toMSecsSinceEpoch() / 1000)
    query = QSqlQuery(_STUDY_UPDATE_QUERY_STR)
    if query.exec_():
        print("Update Case")
    return study_log.query.exec_()

def serie_log(dataset):
    serie_log.query.finish()
    serie_log.query.bindValue(':series_iuid', str(dataset.SeriesInstanceUID))
    serie_log.query.bindValue(':study_iuid', str(dataset.StudyInstanceUID))
    serie_log.query.bindValue(':series_no', str(dataset.SeriesNumber))
    serie_log.query.bindValue(':modality', dataset.Modality)
    return serie_log.query.exec_()


def sop_log(dataset):
    sop_log.query.finish()
    sop_log.query.bindValue(':sop_iuid', str(dataset.SOPInstanceUID))
    sop_log.query.bindValue(':series_iuid', str(dataset.SeriesInstanceUID))
    sop_log.query.bindValue(':instance_no', str(dataset.InstanceNumber))
    return sop_log.query.exec_()

def make_thumbnail(dataset):
    pass

def setup():
    logger.info('Dataset Setup Starting')
    # if not QSqlQuery().isValid():
    #     logger.critical('Dataset Setup Error : Database is not open')
    #     # sys.exit(0)
    patient_log.query = QSqlQuery()
    _PATIENT_INSERT_QUERY_STR = 'INSERT OR IGNORE INTO patient(`patient_id`, `name`, `dob`, `gender`) VALUES(:patient_id, :name, :dob, :gender)'
    patient_log.query.prepare(_PATIENT_INSERT_QUERY_STR)

    study_log.query = QSqlQuery()
    _STUDY_INSERT_QUERY_STR = 'INSERT OR IGNORE INTO study(`study_iuid`, `patient_id`, `datetime`, `accession_no` , `status` ,`thumbnail` ,`update_timestamp` ,`workflow_phase`) VALUES(:study_iuid, :patient_id, :datetime, :accession_no, :status, :thumbnail, :update_timestamp , 0)'
    study_log.query.prepare(_STUDY_INSERT_QUERY_STR)

    study_log.update_query = QSqlQuery()
    _STUDY_UPDATE_QUERY_STR = "UPDATE OR IGNORE study set `update_timestamp` = :update_timestamp WHERE study_iuid = :study_iuid"
    study_log.update_query.prepare(_STUDY_UPDATE_QUERY_STR)

    serie_log.query = QSqlQuery()
    _SERIE_INSERT_QUERY_STR = 'INSERT OR IGNORE INTO serie(`series_iuid`, `study_iuid`, `series_no`, `modality`) VALUES(:series_iuid, :study_iuid, :series_no, :modality)'
    serie_log.query.prepare(_SERIE_INSERT_QUERY_STR)

    sop_log.query = QSqlQuery()
    _SOP_INSERT_QUERY_STR = 'INSERT OR IGNORE INTO sop(`sop_iuid`, `series_iuid`, `instance_no`) VALUES(:sop_iuid, :series_iuid, :instance_no)'
    sop_log.query.prepare(_SOP_INSERT_QUERY_STR)
    logger.info('Dataset Setup Finishing')

def on_dataset(dataset):
    logger.info("Starting save Dataset")
    thumbnail = make_thumbnail(dataset)
    db = QSqlDatabase.database()
    db.transaction()
    if patient_log(dataset) and study_log(dataset,thumbnail) and serie_log(dataset) and sop_log(dataset):
        logger.info("DICOM DATASET LOGGED {}".format(dataset.SOPInstanceUID))
        # print("DICOM DATASET LOGGED ", dataset.SOPInstanceUID)
        db.commit()
    else:
        logger.warning("DICOM DATASET ERROR!: \n >>> IUID: {} \n \t>>> SERIES IUID: {}"
                       "\n \t >>> STUDY IUID: ", dataset.SOPInstanceUID, dataset.SeriesInstanceUID,
                        dataset.StudyInstanceUID)
        print("DICOM DATASET ERROR!: ", dataset)
        print(">>> IUID:", dataset.SOPInstanceUID)
        print(">>> SERIES IUID: ", dataset.SeriesInstanceUID)
        print(">>> STUDY IUID: ", dataset.StudyInstanceUID)
        db.rollback()
    logger.info("Finishing save Dataset")