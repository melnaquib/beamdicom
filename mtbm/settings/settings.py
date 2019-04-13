from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QDir
import resources_rc
import logging

logger = logging.getLogger('dicomrouter')

def setup():
    logger.info('Starting Setup Settings')
    settings = QSettings()
    defaultSettings = QSettings("defaultSettings.ini", QSettings.IniFormat)
    print(defaultSettings.status())
    print(defaultSettings.allKeys())
    logger.info('Default setting path: {}'.format(defaultSettings.fileName()))
    logger.info('Default setting Keys and values')
    for k in defaultSettings.allKeys():
        logger.info('{} : {}'.format(k, defaultSettings.value(k)))
    pathkeys = list(defaultSettings.value("pathskey/keys")) if defaultSettings.value("pathskey/keys") is not None else list()
    logger.info('*********************************************')

    # if pathkeys is not None:
    #     pathkeys = list(pathkeys)
    # for k in pathkeys:
    #     defaultSettings.setValue(k,defaultSettings.value(k).replace('/', QDir.separator()))

    for k in defaultSettings.allKeys():
        if not settings.contains(k):
            v = defaultSettings.value(k)
            settings.setValue(k, v)
    # settings.setValue("db/name", settings.value("storage/folder") + QDir.separator() + "db.sqlite")
    setupSettings = QSettings("setupSettings.ini", QSettings.IniFormat)
    logger.info('Setup Setting File: {}'.format(setupSettings.fileName()))
    logger.info('Setup Setting keys and values')
    ############## set values always as setup
    # for k in setupSettings.allKeys():
    #     logger.info('{} : {}'.format(k, setupSettings.value(k)))
    #     settings.setValue(k, setupSettings.value(k))
    ############################################
    for k in setupSettings.allKeys():
        if not settings.contains(k):
            v = setupSettings.value(k)
            settings.setValue(k, v)
    logger.info('*********************************************')
    settings.sync()
    logger.info('Saving Setting File: {}'.format(settings.fileName()))
    logger.info('Saving Setting Keys and values')
    for k in settings.allKeys():
        logger.info('{} : {}'.format(k , settings.value(k)))
    logger.info('*********************************************')
    logger.info('Finishing Setup Settings')

