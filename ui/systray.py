
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, qApp
from PyQt5.QtGui import QIcon
import images_rc


def setup(action_show_window, action_import, action_exit):
    cxt_menu = QMenu()
    cxt_menu.addAction(action_show_window)
    cxt_menu.addSeparator()
    cxt_menu.addAction(action_import)
    cxt_menu.addSeparator()
    cxt_menu.addAction(action_exit)

    tray = QSystemTrayIcon()

    tray.setIcon(QIcon(":/images/app_icon.png"))
    tray.setContextMenu(cxt_menu)
    tray.show()
    tray.setToolTip(qApp.applicationName())
    # tray.showMessage("hoge", "moge")
    # self.tray.showMessage("fuga", "moge")

    return tray

