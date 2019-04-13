from PyQt5.QtNetwork import QTcpServer, QTcpSocket,  QHostAddress, QNetworkAccessManager
from PyQt5.QtWidgets import qApp

import requests


def run_once():
    def on_newconn():
        if "mainwindow" in qApp.dynamicPropertyNames():
            qApp.property("mainwindow").show()

    port = 12300
    server = QTcpServer()
    server.newConnection.connect(on_newconn)
    ok = server.listen( QHostAddress.Any, port)
    if not ok:
        try:
            req = requests.get('http://localhost:{}'.format(port), timeout=0)
        except:
            pass

    return ok, server, port
