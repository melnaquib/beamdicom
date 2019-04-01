from pydicom import read_file
from pynetdicom3 import AE
from pynetdicom3 import StorageSOPClassList
from PyQt5.QtCore import QSettings
from pynetdicom3 import sop_class
from pydicom.uid import ImplicitVRLittleEndian, ExplicitVRLittleEndian, DeflatedExplicitVRLittleEndian, \
    ExplicitVRBigEndian
from pynetdicom3 import StorageSOPClassList
from pydicom import read_file
import threading
import logging, os
logger = logging.getLogger('dicomrouter')

class StoreScu():

    def __init__(self):

        self.setup()

    def setup(self):
        # Set Transfer Syntax options
        transfer_syntax = [ExplicitVRLittleEndian,
                           ImplicitVRLittleEndian,
                           DeflatedExplicitVRLittleEndian,
                           ExplicitVRBigEndian]
        settings = QSettings()
        self._calling_aet = settings.value('storescu/aet')
        print(settings.value('targetStorescp/aet'))
        remotehost = 'localhost'
        remoteport = '12105'
        aec = ''
        # Bind to port 0, OS will pick an available port
        self._ae = AE(ae_title=self._calling_aet,
                port=0,
                scu_sop_class=StorageSOPClassList,
                scp_sop_class=[],
                transfer_syntax=transfer_syntax)

        self._ae.OnAssociateResponse = self.OnAssociateResponse
        self._remote_ae = dict(Address=remotehost, Port=remoteport, AET=aec)
        self._assoc = None

    def connect(self):
        print(self._remote_ae.get('Address'))
        print(self._remote_ae.get('Port'))
        self._assoc = self._ae.associate(self._remote_ae.get('Address'), int(self._remote_ae.get('Port')), self._calling_aet)
        if not self._assoc.is_established:
            print("Could not establish association")
            logger.warning("Could not establish association")
            return False
        # perform a DICOM ECHO, just to make sure remote AE is listening

        print('done"')
        return True

    # call back
    def OnAssociateResponse(association):
        print("Association response received")
        logger.info('Association response received')

    def send(self, dcm_files):
        for ii in dcm_files:
            print(ii)
            d = read_file(ii)
            print("DICOM StoreSCU ... ",)
            try:
                dataset = read_file(ii)
                status = self._assoc.send_c_store(dataset)
                print('done with status {}',status.status_type)
            except:
                print("problem", d.SOPClassUID)
        print("Release association")
        self._assoc.release()
        # done
        self._ae.quit()









def setup():
    logger.info('Starting StoreScu Setup')
    settings = QSettings()
    storage_foldername = settings.value('storage/folder')
    logger.info('Storage folder path: {}'.format(storage_foldername))
    if not os.path.exists(storage_foldername):
        os.makedirs(storage_foldername)
    logger.info('Finishing Storage Setup')






# assoc = AE.associate()
def connect():
    pass
def sendfile(file):
    transfer_syntax = [ImplicitVRLittleEndian,
                       ExplicitVRLittleEndian,
                       DeflatedExplicitVRLittleEndian,
                       ExplicitVRBigEndian]
    settings = QSettings()
    ae = AE(ae_title=settings.value('storescu/aet'),  # calling aet
            port=0,
            scu_sop_class=StorageSOPClassList,
            scp_sop_class=[],
            transfer_syntax=transfer_syntax)
    # Try and associate with the peer AE
    #   Returns the Association thread
    print('Requesting Association with the peer')
    print(settings.value('storescu/aet'))
    print(settings.value('targetStorescp/aet'))
    print(settings.value('targetStorescp/port'))
    assoc = ae.associate(settings.value('targetStorescp/aet'),
                         int(settings.value('targetStorescp/port')))
    if assoc.is_established:
        print('Association accepted by the peer')
        # Read the DICOM dataset from file 'dcmfile'
        dataset = read_file(file)
        # Send a DIMSE C-STORE request to the peer
        status = assoc.send_c_store(dataset)
        print('C-STORE status: %s' %status)
        # Release the association

        return status
    else:
        return sop_class.StorageServiceClass.OutOfResources


if __name__ == '__main__':
    from settings import settings
    settings.setup()
    s = StoreScu()
    dicom_path = '/media/abdelrahman/data1/mywork/melnaquib/dicom_converter/1.2.826.0.1.368043.2.206.20170330073520.725846087'
    dicomfiles = []

    for root, dirs, files in os.walk(dicom_path):
        for name in files:
            dicomfiles.append(os.path.join(root, name))
    if s.connect():
        s.send(dicomfiles)

