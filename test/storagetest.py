from storage import storage
import threading

def sending(path):
    pass


if __name__ == '__main__':
    from settings import settings

    settings.setup()

    t1 = threading.Thread(target=sending(), args=('/media/abdelrahman/data1/mywork/melnaquib/dicom_converter/1.2.826.0.1.368043.2.206.20170330073520.725846087'))
    t2 = threading.Thread(target=sending, args=('/media/abdelrahman/data1/mywork/melnaquib/dicom_converter/1.2.826.0.1.368043.2.206.20170626210644.701357663'))
    t1.start()
    t2.start()

    print("Main complete")