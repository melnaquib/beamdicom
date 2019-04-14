# from celery import Celery
from numbers import Number
from pydicom import read_file
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QDir
import os
import numpy as np
# app = Celery("dicomTasks")
# import threading
# import celery.worker
# from dicomTasks import app
# from PyQt5.QtCore import QDir
#
# worker = celery.worker.WorkController(app=app, pool_cls='solo')
# threading.Thread(target=worker.start).start()
# Wait for Worker to be fully up and running
# import time
# time.sleep(1)
#how to send percentage file transfers to calling function
# @app.task
import logging

logger = logging.getLogger('beamdicom')

def processStudyuuid(study_uuid):
    """
    
    :param study_uuid: 
    :return: map of db flag column names, and whether they succeeded
    """
    res = {}
    from image.images import study_dcm2img
    logger.info('Starting Converion for study iuid :{}'.format(study_uuid))
    ok = study_dcm2img(study_uuid)
    res["to_image"] = ok
    logger.info('Finishing Conversion for study iuid :{}'.format(study_uuid))

    # ok = sendToTargetPacs(study_uuid)
    # res["to_pacs"] = ok

    return res


def sendToTargetPacs(study_uuid):
    from utils import dicomfiles
    from storage import storescu as neptunescu
    from pynetdicom3 import sop_class
    # neptunescu.connect()
    for file in dicomfiles(study_uuid):
        try:
            if sop_class.StorageServiceClass.Success == neptunescu.sendfile(file):
                updatestudystatus(study_uuid)
        except Exception as err:
            print(err)
    # neptunescu.release()


def updatestudystatus(study_uui):
    from PyQt5.QtSql import QSqlDatabase,QSqlQuery
    from casesActions.dataset_actions import CaseState
    QSqlDatabase.database().transaction()
    query = QSqlQuery()
    query.prepare("UPDATE study SET status = :status , to_pacs = :to_pacs WHERE study_iuid = :study_iuid")
    query.bindValue(":status", CaseState.FORWARDED.value)
    query.bindValue(":to_pacs", bool(True))
    query.bindValue(":study_iuid", str(study_uui))
    query.exec_()
    QSqlDatabase.database().commit()

def updatesopstatus(sop_uui, sop_status):
    from PyQt5.QtSql import QSqlDatabase,QSqlQuery
    from mtbm.casesActions.dataset_actions import CaseState
    QSqlDatabase.database().transaction()
    status = CaseState.RECIEVED.value
    query = QSqlQuery()
    query.prepare("UPDATE sop SET status = :status  WHERE sop_iuid = :sop_iuid")
    if sop_status:
        status = CaseState.FORWARDED.value
    logger.info('Update sop iuid :{} , status: {}'.format(sop_uui,status))
    query.bindValue(":status", status)
    # query.bindValue(":to_pacs", bool(True))
    query.bindValue(":sop_iuid", str(sop_uui))
    query.exec_()
    QSqlDatabase.database().commit()

def destinationpacs(referring_physician):
    from PyQt5.QtSql import QSqlDatabase,QSqlQuery
    from casesActions.dataset_actions import CaseState
    QSqlDatabase.database().transaction()
    query = QSqlQuery()
    # query.prepare("SELECT address,port,aet FROM routes WHERE referring_physician like '%' :referring_physician  '%'")


    # query.bindValue(":referring_physician", referring_physician)


    query.exec("SELECT address,port,aet FROM routes WHERE referring_physician like '%{}%'".format(referring_physician))
    QSqlDatabase.database().commit()

    address = query.value(0)
    port = query.value(1)
    aet = query.value(1)
    logger.info('Destination Pacs For Referring Physician:{} , address : {}, port : {}, aet : {}'.format(referring_physician,address,port,aet))
    return  (address, port, aet)