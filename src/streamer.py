
import numpy as np
from pathlib import Path
import cv2
from PySide6 import QtCore, QtGui, QtQuick, QtQml


class Singleton(type(QtCore.Qt), type):
    """
    Singleton is a creational design pattern, which ensures that only one object 
    of its kind exists and provides a single point of access to it for any other code.
    """
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance


class Streamer(QtCore.QObject, metaclass=Singleton):
    imageChangeSignal = QtCore.Signal()

    def __init__(self, parent=None):
        super(Streamer, self).__init__(parent)
        self._image = QtGui.QImage()
        self.m_videoCapture = cv2.VideoCapture()

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
        self.m_videoCapture.release()
        self.m_videoCapture = cv2.VideoCapture(0)
        while True:
            _, self.f_image = self.m_videoCapture.read()
            self.process_image(self.f_image)

    def process_image(self, image):
        self._image = self.ToQImage(image)
        self.imageChangeSignal.emit()

    def ToQImage(self, im):
        if im is None:
            return QtGui.QImage()
        if im.dtype == np.uint8:
            w, h, _ = im.shape
            rgb_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            flip_image = cv2.flip(rgb_image, 1)
            qim = QtGui.QImage(flip_image.data, h, w,
                               QtGui.QImage.Format_RGB888)
            return qim.copy()
        return QtGui.QImage()

    def image(self):
        return self._image
