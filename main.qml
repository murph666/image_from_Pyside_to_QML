import QtQuick 2.15
import QtQuick 2.15
import QtQuick.Controls 2.15
import PyCVQML 1.0


ApplicationWindow {
    id: root
    visible: true
    width: 1200
    height: 1000
    color: "#122D42"
    

    Main{
        id: main
        
        Component.onCompleted: main.start()
    }

    Image {
        id: image
        width: 640
        height: 600
        anchors.fill: parent
        image: PY_manager.image
    }

}
