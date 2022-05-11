from PySide6 import QtQml
from .image import VideoImage
from .streamer import Streamer
import cv2
from pathlib import Path
import sys


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1] 
sys.path.append(ROOT)
print(ROOT)
sys.path.append(str(ROOT.joinpath('MvImport')))

def registerTypes(uri = "PyCVQML"):

    QtQml.qmlRegisterType(VideoImage, uri, 1, 0, "Image")
   
