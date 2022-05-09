
import os

import sys
import cv2
from PySide6 import QtGui, QtCore, QtQuick
from src import *
import shiboken6


CURRENT_DIRECTORY = Path(__file__).resolve().parent



class MainWindow(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.videoThread = QtCore.QThread()
        self.streamer = Streamer()
        self.streamer.imageChangeSignal.connect(self.imageChanged)

    def launchThread(self, worker, threader):
        worker.moveToThread(threader)
        
        threader.started.connect(worker.runStream)
        threader.started.connect(print("STARDED"))

        threader.finished.connect(threader.quit)
        threader.finished.connect(lambda: QtCore.QThread.msleep(10))
        threader.finished.connect(threader.deleteLater)
        threader.finished.connect(lambda: QtCore.QThread.msleep(10))
        threader.finished.connect(worker.deleteLater)

        threader.start()
    
    @QtCore.Signal
    def imageChanged(self):
        pass
        
    @QtCore.Slot()
    def start(self):
        self.launchThread(self.streamer, self.videoThread)

    @QtCore.Property(QtGui.QImage, notify=imageChanged)
    def image(self):
        return self.streamer.image()


if __name__ == '__main__':
    registerTypes()
    app = QtGui.QGuiApplication(sys.argv)

    engine = QtQml.QQmlApplicationEngine()
    manager = MainWindow()
    
    engine.rootContext().setContextProperty("PY_manager", manager)
    engine.load(QtCore.QUrl.fromLocalFile(CURRENT_DIRECTORY / "main.qml"))
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
