from PyQt5.QtWidgets import QItemDelegate

class CenterItemDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(CenterItemDelegate, self).__init__(parent)

    