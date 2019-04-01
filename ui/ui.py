
from .mainwindow import MainWindow

import sys
from PyQt5 import QtCore, QtWidgets
import logging
logger = logging.getLogger('dicomrouter')
def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    logger.info('QT Debug: line: {}, func: {}(), file: {}'.format(
          context.line, context.function, context.file))
    logger.info('  {}: {}\n'.format(mode, message))






def setup():
    QtCore.qDebug('Setup QDebug ')
    QtCore.qInstallMessageHandler(qt_message_handler)


def run():
    w = MainWindow()
    w.showMaximized()
    return w
