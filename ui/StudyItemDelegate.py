from PyQt5.QtWidgets import QStyledItemDelegate, QItemDelegate, QAbstractItemDelegate, QWidget, QStyle, QApplication
from PyQt5.QtGui import QRegion, QPainter, QPalette, QColor
from PyQt5.QtCore import QPoint, QSize, Qt


from ui.StudyItemWidget import StudyItemWidget

class StudyItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(StudyItemDelegate, self).__init__(parent)

        self.studyItemWidget = StudyItemWidget()
        self.studyItemWidget.setAttribute(Qt.WA_DontShowOnScreen, True)
        # self.studyItemWidget.show()

    def sizeHint(self, option, index):
        # result = super(StudyItemDelegate, self).sizeHint(option, index)
        # result.setHeight(result.height() * 2)
        # result.setHeight(256)
        # print(self.studyItemWidget.normalGeometry().width())
        # print(self.studyItemWidget.normalGeometry().width())
        # result.setHeight(600)
        # print()
        result = QSize(option.rect.width(), self.studyItemWidget.minimumSizeHint().height())
        return result

    #     pass

    def paint3(self, painter, option, index):
        if(index.row()):
            print ("4")
        paintdevice = painter.device()
        painter.end()

        opt = option
        super(StudyItemDelegate, self).initStyleOption(opt, index)

        cg = QPalette.Normal if int(opt.state) & int(QStyle.State_Enabled) else QPalette.Disabled
        if QPalette.Normal == cg and not(int(opt.state) & int(QStyle.State_Active)):
            cg = QPalette.Inactive

        if (opt.state & QStyle.State_Selected):
            painter.setPen(opt.palette.color(cg, QPalette.HighlightedText))
        else:
            painter.setPen(opt.palette.color(cg, QPalette.Text))

        # style.drawControl(QStyle.CE_ItemViewItem, opt, painter, self.studyItemWidget)

        srcIndex = index.model().mapToSource(index)
        record = srcIndex.model().record(srcIndex.row())
        self.studyItemWidget.load(record)

        painter.translate(option.rect.topLeft())

        self.studyItemWidget.setGeometry(opt.rect)
        point = QPoint(opt.rect.x(), opt.rect.y())
        # point = QPoint(option.rect.y(), option.rect.x())
        region = QRegion(opt.rect)
        # painter = QPainter()
        # painter.setBrush(option.palette.foreground())
        self.studyItemWidget.render(painter.device(), QPoint(0, 0), region, QWidget.DrawChildren)
        self.studyItemWidget.render(painter.device(), QPoint(), QRegion(), QWidget.DrawChildren)

        print(option.rect.x(), " POINT ", option.rect.y())
        print(option.rect.width(), " ", option.rect.height())

        painter.begin(paintdevice)


    def paint2(self, painter, option, index):
        # paintdevice = painter.device()
        # painter.end()

        opt = option
        super(StudyItemDelegate, self).initStyleOption(opt, index)

        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)

        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, self.studyItemWidget)

        rect = option.rect
        cg = QPalette.Normal if int(opt.state) & int(QStyle.State_Enabled) else QPalette.Disabled
        if QPalette.Normal == cg and not(int(opt.state) & int(QStyle.State_Active)):
            cg = QPalette.Inactive

        if (opt.state & QStyle.State_Selected):
            painter.setPen(opt.palette.color(cg, QPalette.HighlightedText))
        else:
            painter.setPen(opt.palette.color(cg, QPalette.Text))

        # painter->drawText(QRect(rect.left(), rect.top(), rect.width(), rect.height()/2),
        #                   opt.displayAlignment, line0);
        # painter->drawText(QRect(rect.left(), rect.top()rect.height()/2, rect.width(), rect.height()/2),
        #                   opt.displayAlignment, line1);

        painter.translate(option.rect.topLeft())
        self.studyItemWidget.render(painter.device(), QPoint(),
                                    QRegion(), QWidget.DrawChildren)

        painter.begin(paintdevice)

    def paint(self, painter, option, index):
        rr = index.row()
        # painter.fillRect(300, 300, 300, 300, QColor(100, 0, 0, 100))

        opt = option
        super(StudyItemDelegate, self).initStyleOption(opt, index)
        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawPrimitive(QStyle.PE_PanelItemViewItem, opt, painter, None);
        self.studyItemWidget.setStyle(style)


        srcIndex = index.model().mapToSource(index)
        record = srcIndex.model().record(srcIndex.row())
        self.studyItemWidget.load(record)

        paintdevice = painter.device()
        painter.end()

        # style.drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)
        # style.drawControl(QStyle.CE_ItemViewItem, opt, painter, self.studyItemWidget)

        # cg = QPalette.Normal if int(opt.state) & int(QStyle.State_Enabled) else QPalette.Disabled
        # if QPalette.Normal == cg and not(int(opt.state) & int(QStyle.State_Active)):
        #     cg = QPalette.Inactive
        # if (opt.state & QStyle.State_Selected):
        #     painter.setPen(opt.palette.color(QPalette.Highlight))
        # else:
        #     painter.setPen(opt.palette.color(cg, QPalette.Background))

        # style.drawPrimitive(QStyle.PE_PanelItemViewItem, option, painter, None);

        # painter.translate(option.rect.topLeft())

        self.studyItemWidget.setGeometry(opt.rect)
        # painter.fillRect(10, 10, 100, 100, QColor(0, 0.5, .5, .5))


        # self.studyItemWidget.move(QPoint(option.rect.left(), option.rect.top()))
        # self.studyItemWidget.render(painter)

        # point = option.rect.topLeft()
        point = QPoint(option.rect.topLeft().x(), option.rect.topLeft().y() + 300)
        region = QRegion(0, 0, option.rect.width(), option.rect.height())

        self.studyItemWidget.render(painter.device(), point, region, QWidget.DrawChildren)

        # painter = QPainter()
        # painter.fillRect(opt.rect, QColor(0, 0, .5, .5))

        # painter.end()

        painter.begin(paintdevice)

    def paint4(self, painter, option, index):
        paintdevice = painter.device()
        painter.end()

        opt = option
        super(StudyItemDelegate, self).initStyleOption(opt, index)

        srcIndex = index.model().mapToSource(index)
        record = srcIndex.model().record(srcIndex.row())
        self.studyItemWidget.load(record)

        self.studyItemWidget.setGeometry(opt.rect)
        point = opt.rect.topLeft()
        # point = QRect(0, 0)option.rect.topLeft()
        region = QRegion(0, 0, option.rect.width(), option.rect.height())
        painter.translate(opt.rect.topLeft())
        self.studyItemWidget.render(painter.device(), point,
                                    region, QWidget.DrawChildren)

        # print(option.rect.x(), " POINT ", option.rect.y())
        # print(option.rect.width(), " ", option.rect.height())
        painter.begin(paintdevice)
