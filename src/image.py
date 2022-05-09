from PySide6 import QtCore, QtGui, QtQuick


class VideoImage(QtQuick.QQuickPaintedItem):
    imageChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(VideoImage, self).__init__(parent)

        image = QtGui.QImage(3, 3, QtGui.QImage.Format_RGB32)

        value = QtGui.qRgb(189, 149, 39)  # 0xffbd9527
        image.setPixel(1, 1, value)

        value = QtGui.qRgb(122, 163, 39)  # 0xff7aa327
        image.setPixel(0, 1, value)
        image.setPixel(1, 0, value)

        value = QtGui.qRgb(237, 187, 51)  # 0xffedba31
        image.setPixel(2, 1, value)

        #self.m_image = QtGui.QImage()
        self.m_image = image

    def paint(self, painter):
        if self.m_image.isNull(): return
        image = self.m_image.scaled(self.size().toSize())
        painter.drawImage(QtCore.QPoint(), image)


    def setImage(self, image):
        #if self.m_image == image: return
        self.m_image = image
        self.imageChanged.emit()
        self.update()

    def image(self):
        return self.m_image

    image = QtCore.Property(QtGui.QImage, fget=image, fset=setImage, notify=imageChanged)
