from PyQt5 import QtCore,QtWidgets, QtGui

class Button(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Button, self).__init__(parent)
        self.setAcceptDrops(True)
        #self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(Button, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(Button, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.files_paths = []
            for url in event.mimeData().urls():
                file = url.toLocalFile()
                self.files_paths.append(QtCore.QFileInfo(file).absoluteFilePath())

            event.acceptProposedAction()
        else:
            super(Button,self).dropEvent(event)
    def accept(self):
        from storage import storage
        import pydicom
        from pydicom.errors import InvalidDicomError

        for f in self.files_paths:
            try:
                dataset = pydicom.read_file(f)
                storage._on_c_store()
            except InvalidDicomError :
                print('Not DICOM IMAGE')
            except PermissionError :
                print('Permission Error')
