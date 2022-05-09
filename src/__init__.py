from PySide6 import QtQml
from .image import VideoImage
from .streamer import Streamer
import cv2
from pathlib import Path
import sys
FILE = Path(__file__).resolve()

ROOT = FILE.parents[1] 
sys.path.append(ROOT)
from main import MainWindow

def registerTypes(uri = "PyCVQML"):
    QtQml.qmlRegisterType(VideoImage, uri, 1, 0, "Image")
    QtQml.qmlRegisterType(MainWindow, uri, 1, 0, "Main")
