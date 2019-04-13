import fnmatch

from PyQt5.QtCore import QObject, QModelIndex
from PyQt5.QtSql import QSqlTableModel


class Router(QObject):

    def __init__(self, parent=None):
        super(Router, self).__init__(parent)

        self._routesModel = QSqlTableModel(self)
        self._routesModel.setTable("routes")
        self._routesModel.select()


    def routesModel(self):
        return self._routesModel

    def match_name(self, pat, name):
        if 0 == len(name):
            return False
        r = fnmatch.fnmatchcase(name, pat)
        return r

    def match(self, referring_physician):
        n = self.routesModel().rowCount(QModelIndex())
        for i in range(n):
            ir = self.routesModel().record(i)
            # ir.value()
            ireferring_physician = ir.value("referring_physician")
            if self.match_name(ireferring_physician, referring_physician):
                return ir.value("id"), ir.value("referring_physician"), ir.value("address"), ir.value("port"), ir.value("aet")

        return None, None, None, None, None