import QtQuick 2.15
import QtQuick 2.15
import QtQuick.Controls 2.15
import PyCVQML 1.0


ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 600

    Main{
        id: main
        Component.onCompleted: main.start()
    }

    Image {
        id: image
        width: 640
        height: 480
        
        image: PY_manager.image
    }

}
