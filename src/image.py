from PySide6 import QtCore, QtGui, QtQuick


class VideoImage(QtQuick.QQuickPaintedItem):
    """
    Объект-изображение, который отображается в окне
    """
    imageChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(VideoImage, self).__init__(parent)
        self.m_image = QtGui.QImage()

    def paint(self, painter):
        if self.m_image.isNull():
            return
        image = self.m_image.scaled(self.size().toSize())
        painter.drawImage(QtCore.QPoint(), image)

    def image(self):
        return self.m_image

    def setImage(self, image):
        if self.m_image == image:
            return
        self.m_image = image
        self.imageChanged.emit()
        self.update()

    image = QtCore.Property(QtGui.QImage, fget=image,
                            fset=setImage, notify=imageChanged)
