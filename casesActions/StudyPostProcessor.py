from functools import reduce

from PyQt5.QtCore import QThread, pyqtSignal, QSettings
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError
import logging
from storage import workflow

logger = logging.getLogger('dicomrouter')

class StudyPostProcessor(QThread):
    processstudyuid = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self)

    def _db_open(self):
        db = QSqlDatabase.database()
        if not db.isOpen():
            from db import db
            db._qconnect()

    def _db_close(self):
        db = QSqlDatabase.database()
        if db.isOpen():
            QSqlDatabase.database().close()

    def _studies(self):
        """
        caches all list so as not to keep db open,, avoid multiple connections as much as possible
        :return: 
        """
        self._db_open()

        sql_str = """SELECT study_iuid FROM study WHERE  datetime(update_timestamp, 'unixepoch') < datetime('now', '-1 minute')
                          AND to_image=0 AND to_pacs=0"""
        query = QSqlQuery()
        query.exec_(sql_str)
        res = []
        while(query.next()):
            study_iuid = query.value(0)
            res.append(study_iuid)
        # self._db_close()

        return res

    def _mark_done(self, study_iuid, success_list):
        self._db_open()
        query = QSqlQuery()
        sql_str = "UPDATE study SET {} = 1 where study_iuid = '" + str(study_iuid) +"'"
        for process, success in success_list.items():
            if success:
                query.exec(sql_str.format(process))

        # self._db_close()

    def _del_study_files(self,study_iuid):

        # FIXME Check Settings Remove After Conversion or Not
        settings = QSettings()
        remove = settings.value("conversion/dicom_remove")
        if remove == 'true':
            workflow.study_files_del(study_iuid)
            patient_id, patient_name = self.get_patient(study_iuid)
            workflow.delete_study_image_symbolic_link(study_iuid, patient_id, patient_name, delete_study=True)

    def _process(self, study_iuid):
        # self.processstudyuid.emit(study_iuid)

        import dicomTasks
        success = dicomTasks.processStudyuuid(study_iuid)
        self._mark_done(study_iuid, success)

        res = reduce(lambda a, b: a and b, success)
        if(res):
            self._del_study_files(study_iuid)


    def run(self):
        while True:
            l = self._studies()
            if len(l) > 0:
                logger.info('Starting Converion Process')
            for study_iuid in l:
                self._process(study_iuid)
            self.sleep(30)

    def get_patient(self, study_iuid):
        sql_str = "SELECT patient_id, name from patient WHERE patient_id = (SELECT patient_id FROM study WHERE study_iuid = '{study_iuid}')"
        sql_str = sql_str.format(study_iuid=study_iuid)
        query = QSqlQuery(sql_str)
        query.first()

        if query.isValid():
            patient_id = query.value(0)
            print('patient id ', patient_id)
            patient_name = query.value(1)
            return (patient_id, patient_name)


def setup():
    studyProcess = StudyPostProcessor()
    # import dicomTasks
    # studyProcess.processstudyuid.connect(dicomTasks.processStudyuuid)
    studyProcess.start()
    return studyProcess




