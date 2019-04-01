from PyQt5.QtSql import QSqlQuery
def on_study(study_uuid):
    from dicomTasks import processStudyuuid
    processStudyuuid(study_uuid)



def update_study(study_iuid):
    sql_update = "UPDATE OR IGNORE study set to_image = 0 where study.study_iuid ='{study_iuid}'"
    sql_update = sql_update.format(study_iuid=study_iuid)
    update_query = QSqlQuery()
    update_query.exec(sql_update)