from PyQt5.QtCore import QIdentityProxyModel, Qt, QDate, QSortFilterProxyModel, QSize, QRect, QPoint,  Qt
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor
from PyQt5.QtSql import  QSqlQueryModel


class StudiesProxyModel(QSortFilterProxyModel):

    _BRIEF_MODE_ROLES = Qt.UserRole + 0
    _BRIEF_MODE_ROLE_THUMBNAIL = _BRIEF_MODE_ROLES + 0
    _BRIEF_MODE_ROLE_BRIEF_TEXT = _BRIEF_MODE_ROLES + 1

    brief_cols = {'thumbnail': 2, 'brief': 7}

    def data(self, index, role=Qt.DisplayRole):
        value = super(StudiesProxyModel, self).data(index, role)
        record = self.getIndexRecord(index)

        if role == Qt.TextAlignmentRole:
            if StudiesProxyModel.brief_cols['brief'] == index.column():
                return Qt.AlignLeft
            return Qt.AlignCenter

        elif 0 == index.column():
            if role == Qt.DisplayRole:
                name = self.getPatientName(record)

                name = ' '.join(name)

                return name

        elif index.column() == 4 :
            if role == Qt.DisplayRole:
                studydate = str(value)
                year = studydate[:4]
                month = studydate[4:6]
                day = studydate[6:8]
                # studydate  = QDate(int(year),int(month), int(day)).toString("MM-dd-yyyy")
                # studydate = month + '-' + day + '-' + year
                return studydate

        elif StudiesProxyModel.brief_cols['brief'] == index.column() and Qt.DisplayRole == role:
            tmpl = """{fname}, {lname} {num_suffix}
            {studydate}
            {id}"""
            name = self.getPatientName(record)

            id = record.value(1)
            studydate = str(record.value(4))
            year = studydate[:4]
            month = studydate[4:6]
            day = studydate[6:8]
            studydate = QDate(int(year), int(month), int(day)).toString("MM-dd-yyyy")

            status = record.value(5)
            color = "green" if status else "yellow"
            if not status: status = "Processing..."

            text = tmpl.format(fname=name[0], lname=name[1], studydate = studydate, id=id, num_suffix=name[-1])
            return text

        elif StudiesProxyModel.brief_cols['thumbnail'] == index.column():
            preferred_size = QSize(256, 256)
            if Qt.DecorationRole == role:
                record = self.getIndexRecord(index)
                pixmap = QPixmap()
                img_count = record.value('Total Case Images')
                ba = record.value('thumbnail')
                if ba:
                    pixmap.loadFromData(ba, "PNG", Qt.AutoColor)
                    pixmap = pixmap.scaled(preferred_size, Qt.KeepAspectRatio)
                else:
                    pixmap = pixmap.scaled(preferred_size)

                painter = QPainter(pixmap)
                painter.setFont(QFont("FreeSans", 20))
                painter.setPen(QColor('green'))
                margin = 10
                rect = QRect(margin, margin, pixmap.width(), pixmap.height())
                painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, str(img_count))
                painter.end()

                return pixmap

            elif Qt.SizeHintRole == role:
                return preferred_size

        # return super(StudiesProxyModel, self).data(index, role)

        return value

    def getPatientName(self, record):
        name = record.value(0)
        name = [i for i in name.split('^') if i]
        if len(name) < 2:
            name.append('')

        seq = int(record.value('SEQ'))
        return name[0], name[-1], '({seq})'.format(seq=seq) if seq else ''

    def getIndexRecord(self, index):
        index = self.mapToSource(index)
        record = self.sourceModel().record(index.row())
        return record


    def headerData(self, row, orientation, role=None):
        if Qt.Vertical == orientation and Qt.DisplayRole == role:
            return row + 1
        return super(StudiesProxyModel, self).headerData(row, orientation, role)
