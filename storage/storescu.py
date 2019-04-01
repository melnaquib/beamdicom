from pydicom import read_file
from pynetdicom3 import AE
from pynetdicom3 import StorageSOPClassList
from PyQt5.QtCore import QSettings
from pynetdicom3 import sop_class
from pydicom.uid import ImplicitVRLittleEndian, ExplicitVRLittleEndian, DeflatedExplicitVRLittleEndian, \
    ExplicitVRBigEndian
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

def release():
    print("Realease")
    assoc.release()

if __name__ == '__main__':
    from settings import settings
    settings.setup()
    sendfile("/media/abdelrahman/data1/mywork/code/PycharmProjects/dicomrouter/run/storage/1.3.46.670589.28.371150332999920121104133436088654/1")
