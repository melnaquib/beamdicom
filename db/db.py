import sqlite3

from PyQt5.QtCore import QSettings, QDir, QFile
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError

from . import cfg
import os, logging
_MIGRATION_FILENAME_TMPL = "db"+QDir.separator()+"migration"+QDir.separator()+"{}_{}.sql"

logger = logging.getLogger('dicomrouter')

def db_name():
    s = QSettings()
    if not os.path.exists(s.value("storage/folder")):
        os.makedirs(s.value("storage/folder"))
    r = s.value("storage/folder") + QDir.separator() + "db.sqlite"
    return r


def _qconnect():
    db = QSqlDatabase()
    db = QSqlDatabase.addDatabase("QSQLITE")
    if not QFile().exists(db_name()):
        logger.critical('Database file not exist')
        return
    db.setDatabaseName(db_name())
    return db.open()


def exists(conn):
    cursor = conn.execute("SELECT * FROM _META_INFO")
    return cursor.fetchone()


def ver(conn):
    try:
        cursor = conn.execute("SELECT * FROM _META_INFO WHERE key == 'VERSION'")
        row = cursor.fetchone()
        if row:
            return int(row[2])
    except sqlite3.OperationalError:
        pass

    return 0


def set_ver(conn, value):
    conn.execute("UPDATE _META_INFO SET VALUE = '{}' WHERE key == 'VERSION' ".format(value))


def _step(conn, num, forward=True):
    try:
        filename = _MIGRATION_FILENAME_TMPL.format(num, "up" if forward else "down")
        sql_str = open(filename, 'r').read()
        conn.executescript(sql_str)
        return True
    except Exception as e:
        print(e)
    return False


def _migrate():
    logger.info('Starting database migration')
    conn = sqlite3.connect(db_name())
    current_ver = ver(conn)
    res = current_ver
    logger.info('Target version: {}'.format(cfg.target_ver))
    for i in range(current_ver + 1, cfg.target_ver + 1):
        if not _step(conn, i):
            logger.critical('DB MIGRATION ERROR! STEP: {}'.format(i))
            print("DB MIGRATION ERROR! STEP: ", i)
            conn.rollback()
            res = i - 1
            break
        set_ver(conn, i)
        res = i
        logger.info('DB UPDATED: {}'.format(i))
        print("DB UPDATED ", i)
        conn.commit()

    conn.close()
    logger.info('current version: {}'.format(res))
    logger.info('Finishing database migration')
    return res


def setup():
    logger.info('Starting setup database')
    _migrate()
    if not _qconnect():
        logger.critical('Database not open ')
    logger.info('Finishing setup database')
