import sys
import cv2
from PySide6 import QtGui, QtCore, QtQuick

from src import *
from MvCameraControl_class import *
from src.Singleton import Singleton

CURRENT_DIRECTORY = Path(__file__).resolve().parent


class MainWindow(QtCore.QObject, metaclass = Singleton):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)


        # for HikCamera
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        self.convertedDeviceList = []
        print(self)


    def launchThread(self, worker, threader):
        worker.moveToThread(threader)

        threader.started.connect(worker.runStream)
        

        threader.finished.connect(threader.quit)
        threader.finished.connect(lambda: QtCore.QThread.msleep(10))
        threader.finished.connect(threader.deleteLater)
        threader.finished.connect(lambda: QtCore.QThread.msleep(10))
        threader.finished.connect(worker.deleteLater)

        threader.start()

    def getListOfUSBDevices(self, listDevices):
        ret = MvCamera.MV_CC_EnumDevices(self.tlayerType, self.deviceList)
        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(
                MV_CC_DEVICE_INFO)).contents

            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                #print("\ngige device: [%d]" % i)
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    strModeName = strModeName + chr(per)
                #print("device model name: %s" % strModeName)
                nip1 = (
                    (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = (
                    (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = (
                    (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                #print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                list = []
                #print("\nu3v device: [%d]" % i)
                list.append("MV_USB_DEVICE")
                strModeName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    strModeName = strModeName + chr(per)
                #print("device model name: %s" % strModeName)
                list.append(strModeName)
                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                #print("user serial number: %s" % strSerialNumber)
                list.append(strSerialNumber)
                listDevices.append(strModeName)
        #print(listDevices)

    @QtCore.Signal
    def imageChanged(self):
        pass

    @QtCore.Slot()
    def start(self):
        self.getListOfUSBDevices(self.convertedDeviceList)
        self.videoThread = QtCore.QThread()
        self.streamer = Streamer(self.deviceList)
        self.streamer.imageChangeSignal.connect(self.imageChanged)
        self.launchThread(self.streamer, self.videoThread)

    @QtCore.Property(QtGui.QImage, notify=imageChanged)
    def image(self):
        return self.streamer.image()


if __name__ == '__main__':

    registerTypes()
    app = QtGui.QGuiApplication(sys.argv)

    engine = QtQml.QQmlApplicationEngine()
    
    QtQml.qmlRegisterType(MainWindow, "PyCVQML", 1, 0, "Main")
    engine.load(QtCore.QUrl.fromLocalFile(CURRENT_DIRECTORY / "main.qml"))

    manager = MainWindow()
    engine.rootContext().setContextProperty("PY_manager", manager)
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
