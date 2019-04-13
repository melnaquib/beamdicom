import sys

from pydicom import read_file
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, \
    ExplicitVRBigEndian, DeflatedExplicitVRLittleEndian,RLELossless,JPEGBaseline

from pynetdicom import AE, StoragePresentationContexts
# from pynetdicom import StorageSOPClassList

from PyQt5.QtCore import QSettings, QStandardPaths, QDir
import logging
import os



transfer_syntax = [ExplicitVRLittleEndian,
                   ImplicitVRLittleEndian,
                   DeflatedExplicitVRLittleEndian,
                   ExplicitVRBigEndian,
                   ]
transfer_syntax_rle = [
                   RLELossless]
transfer_syntax_jpeg = [
    JPEGBaseline]

def setup_logging():
    logger = logging.getLogger('beamdicom')
    addin_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    # iconnect_log_file = addin_path + QDir.separator() + "beamdicom.log"
    # handler_path = os.getenv('LOG_PATH', iconnect_log_file)
    # handler = logging.FileHandler(handler_path)
    s = QSettings()
    if not os.path.exists(s.value("storage/folder")):
        os.makedirs(s.value("storage/folder"))
    handler = logging.FileHandler(s.value("storage/folder") + QDir.separator() + "beamdicom.log")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(module)s.%(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Set up Logging Complete')
    return logger


logger = setup_logging()

def send(pacs_param,dcmfile_in,calling_aet):
    # check_dcm_file
    # Bind to port 0, OS will pick an available port
    # , peer = 'localhost', port = 11112, called_aet = 'ANYSCP'
    if len(pacs_param) > 0 :
        peer = str(pacs_param[0])
        port = int(pacs_param[1])
        called_aet = str(pacs_param[2])
    if not called_aet:
        called_aet = 'ANYSCP'

    transfer_syntax = [ImplicitVRLittleEndian,
                       ExplicitVRLittleEndian,
                       DeflatedExplicitVRLittleEndian,
                       ExplicitVRBigEndian]
    ae = AE(ae_title=calling_aet)

    for context in StoragePresentationContexts:
        ae.add_requested_context(context.abstract_syntax, transfer_syntax)

    try:
        f = open(dcmfile_in, 'rb')
        dataset = read_file(f, force=True)
        f.close()
    except IOError:
        print('Cannot read input file {0!s}'.format(dcmfile_in))
        sys.exit()

    # Request association with remote
    assoc = ae.associate(peer, port,  ae_title=called_aet)
    sending_status = False
    if assoc.is_established:
        print('Sending file: {0!s}'.format(dcmfile_in))
        logger.info('Sending file: {0!s}'.format(dcmfile_in))
        try:
            # if dataset.data_element("PixelData").VR != "OB":
            # dataset.data_element("PixelData").VR = "OB"
            status = assoc.send_c_store(dataset)
        except ValueError as ve:
            print (ve)
            sending_status = False
        if 0 == status.Status:
            print("send file successfully file: {0!s}".format(dcmfile_in))
            logger.info("send file successfully file: {0!s}".format(dcmfile_in))
            sending_status = True
        else:
            logger.error("Can Not Send File: {0!s}".format(dcmfile_in))
            print("Can Not Send File: {0!s}".format(dcmfile_in))

        assoc.release()
    else:
        logger.error("Can not Establish association ")

    return sending_status




if __name__ == '__main__':

    send(('localhost',4242, 'ANYSCP'), "/media/abdelrahman/data1/mywork/upwork/dcm4chee_aws/s3/3A98D8F9.dcm",'localhost')

