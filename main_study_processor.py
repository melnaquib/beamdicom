import sys

from PyQt5.QtCore import QCoreApplication, QSettings, QThread
from PyQt5.QtWidgets import QWidget, QApplication

def main():
    # app = QCoreApplication(sys.argv)
    app = QApplication(sys.argv)
    def vendorData():
        settings = QSettings(".vendor.ini", QSettings.IniFormat)
        app.setOrganizationName(settings.value("org/name"))
        app.setOrganizationDomain(settings.value("org/domain"))
        # app.setApplicationDisplayName(settings.value("app/displayName"))
        app.setApplicationName(settings.value("app/name"))
        app.setApplicationVersion(settings.value("app/version"))
    vendorData()

    from settings import settings
    settings.setup()

    from casesActions import StudyPostProcessor
    studyThread = StudyPostProcessor.setup()

    sys.exit(app.exec_())


if __name__ == '__main__':
    # import dicomTasks
    main()
