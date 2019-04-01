from PyQt5.QtQuick import QQuickImageProvider
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QSize, QDir, QFileInfo, QUrl, QFile

import PyPDF2

import logging

logger = logging.getLogger(__name__)

class ConvertedPdfImageProvider(QQuickImageProvider):

    def __init__(self):
        super(ConvertedPdfImageProvider, self).__init__(QQuickImageProvider.Pixmap)

    def requestPixmap(self, id, _):
        pixmap = QPixmap()
        size = pixmap.size()
        try:
            print("IMG PDF ID ", id)
            url = QUrl(id)
            qfile = QFile(url.path())
            ok = qfile.open(QFile.ReadOnly)
            print(qfile)

            ba = qfile.readAll()
            import io
            bs = io.BytesIO(ba)
            pdffile = PyPDF2.PdfFileReader(bs)
            page0 = pdffile.getPage(0)
            xObject = page0['/Resources']['/XObject'].getObject()
            imgObjs = [xObject[obj] for obj in xObject if xObject[obj]['/Subtype'] == '/Image']

            if not imgObjs: return QPixmap(), QSize()

            imgObj = imgObjs[0]
            size = QSize(imgObj['/Width'], imgObj['/Height'])
            data = imgObj._data
            print(imgObj['/ColorSpace'])
            print(imgObj['/Filter'])
            if '/DeviceRGB' == imgObj['/ColorSpace'] and '/DCTDecode' ==  imgObj['/Filter']:
                pixmap.loadFromData(data)

                if pixmap.width() > 1024:
                    pixmap = pixmap.scaledToWidth(1024)
                    size = pixmap.size()

        except Exception as e:
            logger.exception("failed to create thumbnail for {filename}".format(filename=id))
            pixmap = pixmap.scaled(512, 512)

        return pixmap, pixmap.size()

if '__main__' == __name__:
    from PyQt5.QtWidgets import QApplication, QLabel

    app = QApplication([])
    provider = ConvertedPdfImageProvider()
    filename = '/home/melnaquib/work/freelancer.com/joshua/dicom_router/test/data/example_output_pdf/1.pdf'
    pixmap, _ = provider.requestPixmap(filename, None)
    w = QLabel()
    w.setPixmap(pixmap)
    w.show()
    app.exec_()

