from PySide6 import QtCore

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