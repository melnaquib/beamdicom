import os

from PyQt5.QtCore import QSettings, QDir, Qt, QPoint, QRect, QByteArray
from PyQt5.QtGui import QImage, QPainter, QPen, QFont, QColor
from PyQt5.QtPrintSupport import QPrinter

import pydicom
import numpy as np
import PIL

#pixel_data, fmt, size, framenumber, sop_iuid, data
from storage import pathes
import logging
from storage.pathes import get_folder_mode,get_images_folder, study_files_path
from PyQt5.QtCore import QFileInfo
import subprocess
from PyQt5.QtSql import QSqlQuery
import images_rc
logger = logging.getLogger('dicomrouter')

def file_images(file):
    dataset = pydicom.read_file(file)
    cine = 'NumberOfFrames' in dataset and dataset.NumberOfFrames > 1

    logger.debug('Number of frames ',cine)
    ww = None
    if  'WindowWidth' in dataset:
        ww = dataset.WindowWidth
    wc = None
    if  'WindowCenter' in dataset:
        wc = dataset.WindowCenter
    if cine:
        for frame_number, pixel_data in enumerate(dataset.pixel_array):
            pixeldata, qfmt = qimage_ready_data(pixel_data, dataset.BitsAllocated,
                              dataset.SamplesPerPixel, ww, wc)
            yield pixeldata, qfmt, (dataset.Columns, dataset.Rows), frame_number, dataset.SOPInstanceUID, dataset
    else:
        pixeldata, qfmt = qimage_ready_data(dataset.pixel_array, dataset.BitsAllocated,
                                                            dataset.SamplesPerPixel, ww,
                                                            wc)
        yield pixeldata, qfmt, (dataset.Columns, dataset.Rows), 0, dataset.SOPInstanceUID, dataset

def study_dicom_files(study_uuid):
    path = pathes.study_files_path(study_uuid)
    for root, dirs, files in os.walk(path):
        for name in files:
            yield os.path.join(root, name)

def get_image_formate(samples_per_pixel):
    fmt = QImage.Format_RGB888
    if samples_per_pixel == 1:
        fmt = QImage.Format_Grayscale8
    return fmt

def study_dcm2img(study_iuid):
    for idx, file in enumerate(study_dicom_files(study_iuid)):
        # try:
        logger.info('Starting Conversion for sop iuid : {}'.format(file))
        file_dcm2img(idx + 1 , file, study_iuid)
        logger.info('Finish Conversion for sop iuid : {}'.format(file))
        # except Exception as err:
        #     print(err)
    # logger.info('No. of images for study iuid: {}  = {}'.format(study_iuid, idx + 1 ))
    return 1


from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


def aa():
    database = QFontDatabase()
    fontTree = QTreeWidget()
    fontTree.setColumnCount(2);
    fontTree.setHeaderLabels(["Font", "Smooth Sizes"]);

    for family in database.families():
        familyItem = QTreeWidgetItem(fontTree)
        familyItem.setText(0, family)
        for style in database.styles(family):
            styleItem = QTreeWidgetItem(familyItem)
            styleItem.setText(0, style)

            sizes = ""
            for points in database.smoothSizes(family, style):
                sizes += str(points) + " "
            styleItem.setText(1, sizes)

        fontTree.showMaximized()
        aa._ = fontTree


def write_patient_data(idx, qimg, dataset):
    #scale up enough to draw text on
    scale = int(1000 / qimg.width()) + 1
    w = qimg.width()
    h = qimg.height()
    qimg = qimg.smoothScaled(w * scale, h * scale)

    TEXT_TMPL_LEFT = """{Laterality}
{patientName}
{patientId}
{date}
{Manufacturer}
"""
    #### {dose}   {accumulateddose}
    TEXT_TMPL_RIGHT ="""{facility}
    {images}
{institionname}
{company}
{website}"""

    #  {totaltimeoffluoroscopy} {exposurecontrolmode}
    values = {}
    values_right = {}
    name = [i for i in  str(dataset.PatientName).split('^') if i]
    patient_name =[i for i in  str(dataset.PatientName).split('^') if i]
    patient_first_name = patient_name[0]
    patient_last_name = patient_name[-1]
    converted_patient_name =  patient_first_name + '\n' +patient_last_name
    values["Laterality"] = str(dataset.Laterality) if 'Laterality' in dataset else ''
    print(values["Laterality"])
    values["patientName"] = converted_patient_name
    values["patientId"] = 'ID:' + str(dataset.PatientID)
    values["date"] = dataset.StudyDate
    # try:
    #     values["dose"] = dataset.EntranceDose  if dataset.EntranceDose in dataset else "" # X-Ray Output
    # except AttributeError as e:
    #     logger.info("EntranceDose Error ".format(e.args))
    #     values["dose"] = ""
    # values["dap"] = 'DAP:' + str(dataset.ImageAndFluoroscopyAreaDoseProduct) + '  mGy.cm\u00b2'  # Image Area Dose Product (ImageAndFluoroscopyAreaDoseProduct) dataset[0x0018, 0x115e].value
    # try:
    #     values["accumulateddose"] = dataset.EntranceDoseInmGy # Entrance Dose in mGy
    # except AttributeError as e:
    #     logger.info(e.args)
    #     values["accumulateddose"] = ''
    # values["kvp"] = str(dataset.KVP) +'  kVp'  # Peak kilo voltage output of the X-Ray generator used. dataset[0x0018, 0x0060].value
    # values["tubecurrent"] = str(int(dataset.XRayTubeCurrentInuA)) + '  uA'  # X-Ray Tube Current in µA.dataset[0x0018, 0x8151].value
    # try:
    #     values_right["totaltimeoffluoroscopy"] = dataset.TotalTimeOfFluoroscopy  # Total Time of Fluoroscopy
    # except AttributeError as e:
    #     values_right["totaltimeoffluoroscopy"] = ''
    #     logger.info(e.args)
    # try:
    #     values_right["exposurecontrolmode"] = dataset["ExposureControlMode"].value  #Exposure Control Mode
    # except ValueError as ve:
    #     values_right["exposurecontrolmode"] = ''
    #     logger.info(ve.args)
    no_images = get_no_images(dataset.StudyInstanceUID)
    # no_images = get_total_images(dataset.StudyInstanceUID)
    values_right["images"] = 'Image  ' + str(idx) + "/" + str(no_images)
    values["Manufacturer"] = str(dataset.Manufacturer)
    values_right["institionname"] = get_instition_name() + ' by:'
    values_right['company'] =  get_company_name()

    values_right["website"] = get_website()
    values_right["facility"] = get_facility_name()

    try:
        text = TEXT_TMPL_LEFT.format(**values)
    except KeyError as e:
        print("Key Error")

    try:
        text_right = TEXT_TMPL_RIGHT.format(**values_right)
    except KeyError as e:
        print("Key Error")

    painter = QPainter(qimg)
    # painter.setFont(QFont("Arial", 12));
    painter.setFont(QFont("FreeSans", 12))
    painter.setPen(QColor(255, 255, 255, 255))
    margin = 10
    r = QRect(margin, 0, qimg.width() , qimg.height() - margin)

    painter.drawText(r, Qt.AlignLeft | Qt.AlignBottom, text)
    painter.end()

    painterright = QPainter(qimg)
    # painter.setFont(QFont("Arial", 12));
    painterright.setFont(QFont("FreeSans", 12))
    painterright.setPen(QColor(255, 255, 255, 255))
    margin = 10
    r = QRect(margin, 0, qimg.width() - 20 , qimg.height() - margin)

    painterright.drawText(r, Qt.AlignRight | Qt.AlignBottom, text_right)

    logo_img = QImage(":/images/app_icon.png")
    logo_img = logo_img.scaledToWidth(qimg.width() / 8)
    painterright.drawImage(QPoint(qimg.width() * 7 / 8, 20), logo_img)

    facility_logo_path = QSettings().value("facility/logo")
    print(facility_logo_path)
    if facility_logo_path:
        facility_img = QImage(facility_logo_path)
        facility_img = facility_img.scaledToWidth(qimg.width() / 8)
        painterright.drawImage(QPoint(1, 20), facility_img)

    painterright.end()

    return qimg


def file_dcm2img(idx, file, study_iuid):
    for pixel_data, fmt, size, framenumber, sop_iuid, dataset in file_images(file):
        qimg = QImage(pixel_data, size[0], size[1], fmt)
        # save
        settings = QSettings()
        save_fmt = settings.value("conversion/format")
        from storage.pathes import study_images_path
        images_path = study_images_path(study_iuid)
        if not os.path.exists(images_path):
            os.makedirs(images_path)
            create_patient_symbolic_link(images_path, dataset.PatientID, dataset.PatientName)
        # frame_filename = images_path + QDir.separator() + sop_iuid + "_" + str(framenumber) + "." + save_fmt
        frame_filename = images_path + QDir.separator() + str(dataset.PatientName).replace('^', ' ') + "_" + str(idx) + "_" + str(framenumber) + "." + save_fmt
        logger.debug('Image is converted :{}'.format(frame_filename))
        qimg = write_patient_data(idx, qimg, dataset)
        logger.debug('finish writing patient data')
        create_thumbnail(qimg, study_iuid)
        save_img(qimg, frame_filename, save_fmt)
        logger.debug('finish saving image')


def qimage_ready_data(pixel_array, bits, samples_per_pixel, ww, wl):
    fmt = get_image_formate(samples_per_pixel)
    logger.debug('Image Formate = ',fmt)
    logger.debug('Samples Per Pixel : ', samples_per_pixel)
    if samples_per_pixel == 1:
        if bits > 8:
            logger.debug('bits is greater than 8 , make rescalling')
            # make rescalling
            if ww is None or wl is None:
                logger.debug('Window Width Or Window Level Is none, so get max and min ')
                max_val = np.max(pixel_array)
                min_val = np.min(pixel_array)
                logger.debug('max val = {} , min_val = {} '.format(max_val, min_val))
                ww = max_val - min_val
                wl = min_val + ww / 2
                logger.debug('After Rescalling: window width : {} , window level : {}'.format(ww, wl))

            w, l = ww, wl
            c = l - (w/2)
            # logger.debug(' y = {} * (x - {} ',format(str(255/w), str(c)))

            pixel_array = (255/w) * (pixel_array - c)
            # PIL.Image.fromarray(pixel_array).convert('L').show()
            pixel_array[pixel_array > 255] = 255
            pixel_array[pixel_array < 0] = 0
            pixel_array = pixel_array.astype(np.uint8)
    return pixel_array, fmt



if __name__ == '__main__':
    from settings import settings
    settings.setup()
    study_dcm2img("1.2.826.0.1.368043.2.206.20170424082631.1263486011.1")


def save_img(qimg, filename, fmt):
    if fmt in ["png", "bmp", "jpg"]:
        qimg.save(filename)
    elif "pdf" == fmt:
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.Letter)
        paperPixels = printer.pageRect(QPrinter.DevicePixel)
        paperPixels = paperPixels.getRect()  # get tuple of the "pixels on the paper"
        paperWidth = paperPixels[2]
        paperHeight = paperPixels[3]
        print('paper height : ', paperHeight, ', paper width : ', paperWidth)
        orientation = QPrinter.Landscape if qimg.width() > qimg.height() else QPrinter.Portrait
        # printer.setPageOrientation(orientation)
        # printerPdf.setPageMargins(20, 10, 20, 20, QPrinter::Millimeter);
        printer.setOutputFormat(QPrinter.PdfFormat)
        # printer.setFullPage(True)
        printer.setOutputFileName(filename)

        painter = QPainter(printer)

        qimg2 = qimg.scaled(printer.width(), printer.height()
                            , Qt.KeepAspectRatio, Qt.SmoothTransformation)
        printer_rect = QRect(0, 0, printer.width(), printer.height())
        img_rect = QRect(QPoint(0, 0), qimg2.size())
        img_rect.moveCenter(printer_rect.center())
        painter.drawImage(img_rect, qimg2)
        painter.end()

def get_no_images(StudyInstanceUID):
    from PyQt5.QtSql import QSqlQuery
    sql_str = "select count(sop_iuid)  from sop where sop.series_iuid in (select serie.series_iuid from serie where serie.study_iuid =  '" + str(StudyInstanceUID) + "' ) "

    query = QSqlQuery()
    # query.bindValue(':series_iuid', str(SeriesInstanceUID))
    query.exec_(sql_str)
    no_images = 0
    while (query.next()):
        no_images = query.value(0)
    return no_images

def get_instition_name():
    settings = QSettings()
    client = settings.value('client/name')
    newclient = str(client).replace('I', "\u2191")
    newclient = newclient.replace(' ','\n')
    return (newclient)

def get_company_name():
    settings = QSettings(".vendor.ini", QSettings.IniFormat)
    return settings.value("org/name")

def get_website():
    settings = QSettings(".vendor.ini", QSettings.IniFormat)
    return settings.value("org/domain")



def create_patient_symbolic_link(study_folder, patient_id, patient_name):
    folder_mode = get_folder_mode()
    storage_folder = get_images_folder()
    target_folder = ''
    if os.path.exists(storage_folder):
        if folder_mode =='PatientID':
            target_folder = storage_folder + QDir.separator() + str(patient_id)
        elif folder_mode =='PatientName':
            target_folder = storage_folder + QDir.separator() + str(patient_name)
        src_folder = QFileInfo(study_folder).absoluteFilePath()
        target_folder = QFileInfo(target_folder).absoluteFilePath()
        if not os.path.exists(target_folder):

            try:
                os.system('mklink /J "{}" "{}"'.format(target_folder, src_folder))
                # subprocess.call('mklink2 /J "{}" "{}"'.format(tar_folder, src_folder))
            except subprocess.CalledProcessError:
                logger.warning('Can not create symbolic link for image folder: ',study_folder)
            except OSError:
                logger.warning('Can not create symbolic link for image folder: ', study_folder)
            except :
                print('**********************************************')
                logger.warning('Can not create symbolic link for image folder: ', study_folder)



def get_total_images(study_iuid):
    query = QSql
    foldername = study_files_path(study_iuid)
    if os.path.exists(foldername):
        files = os.listdir(foldername)
        files = list(files)
    return len(files)

def get_facility_name():
    s = QSettings()
    return s.value("facility/name")


def create_thumbnail(qimg, study_iuid):
    from PyQt5.QtCore import QFile, QIODevice, QBuffer
    from PyQt5.QtSql import QSqlQuery, QSqlDatabase
    # f = QFile(filename)
    # if f.open(QIODevice.ReadOnly):
    #     ba = f.readAll()
    #     f.close()
    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.WriteOnly)
    qimg.save(buffer, 'PNG')

    if ba :
        print("byte array is not none")
        query = QSqlQuery()
        query.prepare("UPDATE study set thumbnail =  :IMAGE  WHERE study.study_iuid = '"+study_iuid+"' ")
        query.bindValue(":IMAGE", ba)
        # query.bindValue(":study_iuid", study_iuid)
        query.exec_()
        if query.lastError().isValid():
            print(query.lastError().text())
            QSqlDatabase.database().rollback()
        else:
            print("Commit")
            QSqlDatabase.database().commit()
