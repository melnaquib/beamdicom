
from pydicom.dataset import Dataset, FileDataset
from pydicom.filewriter import write_file
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian, \
    ExplicitVRBigEndian, DeflatedExplicitVRLittleEndian, UID

# from pynetdicom import AE, StorageSOPClassList
from pynetdicom import AE, evt
# from pynetdicom import pynetdicom_uid_prefix
from pydicom.uid import ImplicitVRLittleEndian, ExplicitVRLittleEndian, DeflatedExplicitVRLittleEndian, \
    ExplicitVRBigEndian
from pynetdicom import sop_class

import logging
import sys
import pydicom

import os
from casesActions.study_actions import on_study
from storage import pathes
import subprocess

pynetdicom_logger = logging.getLogger('pynetdicom')
pynetdicom_logger.setLevel(logging.DEBUG)
# pynetdicom_logger.setLevel(logging.DEBUG)

from PyQt5.QtCore import QThread, QSettings, QTimer,QDir,QFileInfo
from storage.pathes import get_storage_folder, get_folder_mode

import os

from pynetdicom import (
    AE,
    StoragePresentationContexts,
    VerificationPresentationContexts)

_STUDY_TIMEOUT = 60000

def OnAssociateRequest(association):
    logger.info("Store SCP: association requested")

def OnReceiveEcho():
    logger.info("Store SCP: Echo received")

def OnAssociateResponse(association):
    logger.info("Store SCP: Association response received")

def setup_logging():
    logger = logging.getLogger('pynetdicom')
    s = QSettings()
    if not os.path.exists(s.value("storage/folder")):
        os.makedirs(s.value("storage/folder"))
    handler = logging.FileHandler(s.value("storage/folder") + QDir.separator() + "beamdicom.log")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s -  %(module)s.%(funcName)s - %(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Set up Logging Complete')
    return logger

logger = setup_logging()

mode_prefixes = {'CT Image Storage': 'CT',
                 'Enhanced CT Image Storage': 'CTE',
                 'MR Image Storage': 'MR',
                 'Enhanced MR Image Storage': 'MRE',
                 'Positron Emission Tomography Image Storage': 'PT',
                 'Enhanced PET Image Storage': 'PTE',
                 'RT Image Storage': 'RI',
                 'RT Dose Storage': 'RD',
                 'RT Plan Storage': 'RP',
                 'RT Structure Set Storage': 'RS',
                 'Computed Radiography Image Storage': 'CR',
                 'Ultrasound Image Storage': 'US',
                 'Enhanced Ultrasound Image Storage': 'USE',
                 'X-Ray Angiographic Image Storage': 'XA',
                 'Enhanced XA Image Storage': 'XAE',
                 'Nuclear Medicine Image Storage': 'NM',
                 'Secondary Capture Image Storage': 'SC'}


class StoreAE(AE):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def router(self, req, rsp, sopClass):
        sop_uid = sopClass.UID
        sop_uid = sop_uid.name.replace(' ', '')
        delegate = sys.modules['scp_' + sop_uid]
        callback = "on_" + req.__class__.__name__.lower()
        callback = getattr(delegate, callback, self)
        return callback(req, rsp, sopClass)


def get_pacs_parameter(referring_physician):
    from PyQt5 import QtWidgets
    app = QtWidgets.qApp
    r = app.property("router")
    # from storage.Router import Router
    # r = Router()
    id,referring_physician,address,port,aet =  r.match(referring_physician)
    logger.info('Destination Pacs For Referring Physician:{} , address : {}, port : {}, aet : {}'.format(referring_physician,
                                                                                                 address, port, aet))
    return (address, port, aet)

def get_calling_aet():
    setting = QSettings()
    return setting.value("storescp/aet")




def handle_store(event):
    dataset = event.dataset
    try:
        logger.info('Received C-Store. Stn name %s, Modality %s, SOPClassUID %s, Study UID %s and Instance UID %s',
                dataset.StationName , dataset.Modality, dataset.SOPClassUID, dataset.StudyInstanceUID, dataset.SOPInstanceUID)
    except:
        try:
            logger.warning(
                "Received C-Store - station name missing. Modality %s, SOPClassUID %s, Study UID %s and Instance UID %s",
                dataset.Modality, dataset.SOPClassUID, dataset.StudyInstanceUID, dataset.SOPInstanceUID)
        except:
            logger.warning("Received C-Store - error in logging details")
    try:
        sop_class = dataset.SOPClassUID
        sop_instance = dataset.SOPInstanceUID
    except Exception as exc:
        # Unable to decode dataset
        return 0xC210

    try:
        # Get the elements we need
        mode_prefix = mode_prefixes[sop_class.name]
    except KeyError:
        mode_prefix = 'UN'

    study_iuid = dataset.StudyInstanceUID
    foldername = pathes.study_files_path(study_iuid)
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    filename = foldername + QDir.separator() + str(dataset.SOPInstanceUID)
    if sys.platform.startswith('win'):
        create_patient_symbolic_link(foldername,dataset.PatientID,dataset.PatientName)
        pass
        # os.symlink(filename , target)
        # win32file.CreateSymbolicLink(filename, target, 1)

        # winshell.CreateShortcut(
        #     Path=str(foldername + QDir.separator() + dataset.PatientName)+".lnk",
        #     Target=filename
        # )
    cx = event.context

    meta = Dataset()
    meta.MediaStorageSOPClassUID = dataset.SOPClassUID
    meta.MediaStorageSOPInstanceUID = dataset.SOPInstanceUID
    # TODO YOUR_ORGROOT.Year.Month.Day.Hour.Minute.Second.Milliseconds.StaticCounter
    # suffix_uid = [str(),str(),str()]
    vendor_settings =  QSettings(".vendor.ini", QSettings.IniFormat)
    vendor_settings.setIniCodec("UTF-8")
    impl_class_uid_root = vendor_settings.value("dicom/OID")
    ver = vendor_settings.value("app/version")
    app_number = '3' # meaniniglessly chosen
    meta.impl_class_uid = impl_class_uid_root + app_number + '.' + ver
    meta.ImplementationClassUID = impl_class_uid_root + app_number + '.' + ver
    meta.TransferSyntaxUID = cx.transfer_syntax


    # ds = FileDataset(filename, {}, file_meta=meta, preamble=b"\0" * 128)
    # ds.update(dataset)

    dataset.file_meta = meta
    dataset.is_little_endian = cx.transfer_syntax.is_little_endian
    dataset.is_implicit_VR = cx.transfer_syntax.is_implicit_VR



    status_ds = Dataset()
    status_ds.Status = 0x0000

    try:
        dataset.save_as(filename, write_like_original=False)
        logger.info("File %s written", filename)
        status_ds.Status = 0x0000
    except IOError:
        logger.warning('SAVE FAILED! FILE: ', filename)
        print('SAVE FAILED! FILE: ', filename)
        status_ds.Status = 0xA700
        return status_ds # Failed - Out of Resources
    except:
        status_ds.Status = 0xA701
        return status_ds # Failed - Out of Resources
    # print(filename)
    from casesActions import dataset_actions
    dataset_actions.on_dataset(pydicom.read_file(filename))
    ref_ph_name = ''
    try:
        ref_ph_name = dataset.ReferringPhysicianName
        ref_ph_name = str(ref_ph_name)
        logger.info("Received ReferringPhysicianName {}".format(ref_ph_name))
    except:
        logger.error("Dataset not have Referring Physician's Name")
    try:
        pacs_param = get_pacs_parameter(ref_ph_name)
        calling_aet = get_calling_aet()
        from storage import sending
        sending_status = sending.send(pacs_param,filename,calling_aet)

        import dicomTasks
        dicomTasks.updatesopstatus(dataset.SOPInstanceUID, sending_status)
    except:
        logger.error('Error in sending or update status for sop iuid')
    return status_ds # Success

def ae_run():
    transfer_syntax = [ImplicitVRLittleEndian,
                       ExplicitVRLittleEndian,
                       DeflatedExplicitVRLittleEndian,
                       ExplicitVRBigEndian]
    scu_sop_classes = []
    scp_sop_classes = [sop_class.VerificationSOPClass]
    # scp_sop_classes.extend(sop_class.STORAGE_CLASS_LIST)

    settings = QSettings()
    settings.beginGroup('storescp')
    ae_title = settings.value('aet')
    ae_port = int(settings.value('port'))
    max_conn = int(settings.value('max_conn'))

    # FIXEME check Port
    ae = StoreAE(ae_title=ae_title,
            # port=ae_port,
            # scu_sop_class = scu_sop_classes,
            # scp_sop_class = scp_sop_classes,
            # transfer_syntax = transfer_syntax
                 )

    for context in StoragePresentationContexts:
        ae.add_supported_context(context.abstract_syntax, transfer_syntax)
    for context in VerificationPresentationContexts:
        ae.add_supported_context(context.abstract_syntax, transfer_syntax)

    vendor_settings =  QSettings(".vendor.ini", QSettings.IniFormat)
    vendor_settings.setIniCodec("UTF-8")
    impl_class_uid_root = vendor_settings.value("dicom/OID")
    ver = vendor_settings.value("app/version")
    app_number = '3' # meaniniglessly chosen
    ae.impl_class_uid = impl_class_uid_root + app_number + '.' + ver
    ae.impl_ver_name = vendor_settings.value("dicom/OID_NAME") + '_' + ver

    ae_run.ae = ae
    ae.maximum_pdu_size = int(settings.value('max_pdu'))
    ae.network_timeout = int(settings.value('network_timeout'))
    ae.acse_timeout = int(settings.value('acse_timeout'))
    ae.dimse_timeout = int(settings.value('dimse_timeout'))

    ae.maximum_associations = 70

    logger.info('AE properties: ae={}, port={}'.format(ae_title,ae_port))
    # ae.on_c_store = _on_c_store
    handlers = [(evt.EVT_C_STORE, handle_store)]
    try:
        ae.start_server((ae_title,ae_port), evt_handlers=handlers)
        logger.info(' "Started AE... AET:{0}, port:{1}".format(aet, port)')
    except PermissionError as pe:
        logger.critical('AE cannot start (PermissionError)', exc_info=True)
        sys.exit(0)
    except OSError as oe:
        logger.critical('AE cannot start', exc_info=True)
        sys.exit(0)


def setup():
    logger.info('Starting Storage Setup')
    settings = QSettings()
    storage_foldername = settings.value('storage/folder')
    logger.info('Storage folder path: {}'.format(storage_foldername))
    if not os.path.exists(storage_foldername):
        os.makedirs(storage_foldername)
    logger.info('Finishing Storage Setup')


def run():
    ae_thread = QThread()
    ae_thread.run = ae_run
    ae_thread.start()
    logger.info('Storage Started')
    return ae_thread

def run_pythread():
    import threading
    ae_thread = threading.Thread()
    ae_thread.run = ae_run
    # ae_thread.stop = lambda : ae_run.ae.stop()
    ae_thread.start()
    logger.info('Storage Started')
    return ae_thread



# import winshell
import os

def validate_port(port):
    import socket
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        test_socket.bind((os.popen('hostname').read()[:-1],port))
    except socket.error:
        logger.error("Cannot listen on port {0:d}, insufficient priveleges".format(port))
        sys.exit()

# def create_shortcuts(self, tool_name, exe_path, startin, icon_path):
#     from win32com.client import Dispatch
#     import win32file
#
#     shell = Dispatch('WScript.Shell')
#     shortcut_file = os.path.join(winshell.desktop(), tool_name + '.lnk')
#     shortcut = shell.CreateShortCut(shortcut_file)
#     shortcut.Targetpath = exe_path
#     shortcut.WorkingDirectory = startin
#     shortcut.IconLocation = icon_path
#     shortcut.save()

def create_patient_symbolic_link(study_folder, patient_id, patient_name):
    folder_mode = get_folder_mode()
    storage_folder = get_storage_folder()
    if os.path.exists(storage_folder):
        if folder_mode =='PatientID':
            target_folder = storage_folder + QDir.separator() + str(patient_id)
        elif folder_mode =='PatientName':
            target_folder = storage_folder + QDir.separator() + str(patient_name)
        else:
            return
        src_folder = QFileInfo(study_folder).absoluteFilePath()
        tar_folder = QFileInfo(target_folder).absoluteFilePath()
        if not os.path.exists(target_folder):

            try:
                os.system('mklink /J "{}" "{}"'.format(tar_folder, src_folder))
                # subprocess.call('mklink2 /J "{}" "{}"'.format(tar_folder, src_folder))
            except subprocess.CalledProcessError:
                logger.warning('Can not create symbolic link for study folder: ',study_folder)
            except OSError:
                logger.warning('Can not create symbolic link for study folder: ', study_folder)
            except :
                print('**********************************************')
                logger.warning('Can not create symbolic link for study folder: ', study_folder)





