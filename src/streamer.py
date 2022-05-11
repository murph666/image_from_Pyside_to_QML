import numpy as np
from pathlib import Path
import cv2
from PySide6 import QtCore, QtGui, QtQuick, QtQml
import sys
from src.Singleton import Singleton
FILE = Path(__file__).resolve()

ROOT = FILE.parents[0] 
sys.path.append(str(ROOT.joinpath('MvImport')))

from MvCameraControl_class import *



class Streamer(QtCore.QObject, metaclass=Singleton):
    imageChangeSignal = QtCore.Signal()

    def __init__(self,listDevices, parent=None):
        super(Streamer, self).__init__(parent)
        self._image = QtGui.QImage()
        self.m_videoCapture = cv2.VideoCapture()
        self.deviceList = listDevices
        image = QtGui.QImage(3, 3, QtGui.QImage.Format_RGB32)
        value = QtGui.qRgb(189, 149, 39)  # 0xffbd9527
        image.setPixel(1, 1, value)
        value = QtGui.qRgb(122, 163, 39)  # 0xff7aa327
        image.setPixel(0, 1, value)
        image.setPixel(1, 0, value)
        value = QtGui.qRgb(237, 187, 51)  # 0xffedba31
        image.setPixel(2, 1, value)
        self._image = image

        

    def runStream(self):
        cam = MvCamera()

        # Select device and create handle
        stDeviceList = cast(self.deviceList.pDeviceInfo[0], POINTER(
            MV_CC_DEVICE_INFO)).contents
        print(stDeviceList)
        ret = cam.MV_CC_CreateHandle(stDeviceList)

        # Open device
        ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        # Set trigger mode as off
        ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)

        # Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
        ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
        nPayloadSize = stParam.nCurValue

        # Start grab image
        ret = cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            sys.exit()

        self.nPayLoadSize = nPayloadSize

        stDeviceList = MV_FRAME_OUT_INFO_EX()
        memset(byref(stDeviceList), 0, sizeof(stDeviceList))
        data_buf = (c_ubyte * nPayloadSize)()

        # set param to convert img
        nRGBSize = stDeviceList.nWidth * stDeviceList.nHeight*3
        stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
        memset(byref(stConvertParam), 0, sizeof(stConvertParam))
        stConvertParam.nWidth = stDeviceList.nWidth
        stConvertParam.nHeight = stDeviceList.nHeight
        stConvertParam.pSrcData = data_buf
        stConvertParam.nSrcDataLen = stDeviceList.nFrameLen
        stConvertParam.enSrcPixelType = stDeviceList.enPixelType
        stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
        stConvertParam.pDstBuffer = (c_ubyte * nRGBSize)()
        stConvertParam.nDstBufferSize = nRGBSize
        #
        self.frameDetected = np.zeros((2048, 2448), dtype=np.uint8)
        while True:
            
            ret = cam.MV_CC_GetOneFrameTimeout(
                byref(data_buf), nPayloadSize, stDeviceList, 10)
            ret = cam.MV_CC_ConvertPixelType(stConvertParam)

            if ret != 0:
                self.frame = np.array(
                        data_buf, dtype=np.uint8).reshape(2048, 2448)
                self.process_image(self.frame)                    
            else:
                print("get one frame fail, ret[0x%x]" % ret)


    def process_image(self, image):
        self._image = self.ToQImage(image)
        self.imageChangeSignal.emit()

    def ToQImage(self, im):
        if im is None:
            return QtGui.QImage()
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_Indexed8)
                qim.setColorTable([QtGui.qRgb(i, i, i) for i in range(256)])
                return qim.copy()

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    w, h, _ = im.shape
                    rgb_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    flip_image = cv2.flip(rgb_image, 1)
                    qim = QtGui.QImage(flip_image.data, h, w, QtGui.QImage.Format_RGB888)
                    return qim.copy()
        return QtGui.QImage()

    def image(self):
        return self._image
