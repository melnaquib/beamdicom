import QtQuick 2.6
import QtQuick.Controls 1.4 as C1
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Window 2.0

ApplicationWindow {


  visible: true

  title: qsTr("Name: " + patientName + " - Id : " + patientID)
  id : mainwindow

     visibility: Window.FullScreen

  property int currentIndex: 0

  function prev() {
    if(0 == currentIndex)
      currentIndex = files.length - 1;
    else
      --currentIndex;
  }

  function next() {
    if(files.length - 1 == currentIndex)
      currentIndex = 0;
    else
      ++currentIndex;
  }

  Item {
    anchors.fill: parent

    Image {
      id: image
      anchors.fill: parent
      fillMode: Image.PreserveAspectFit
      source: sourcePath(currentIndex)

      function sourcePath(idx) {
        console.log("IDX ", idx);
        var res = imagesFolder + '/' + files[currentIndex];
        if(res.toLowerCase().match('\\.pdf$'))
          res = 'image://imgpdf/' + res;
        else
          res = 'file:///' + res;

        console.log('IMG ', res)
        return res

      }
    }

    focus: true
    Keys.onRightPressed: next()
    Keys.onLeftPressed: prev()

    ViewerToolbar {

      anchors.bottom: parent.bottom
      anchors.margins: 5

      anchors.horizontalCenter: parent.horizontalCenter

      lbtn {
        icon: "images/icons/prev.svg"
        ma.onClicked: prev()
      }
      rbtn {
        icon: "images/icons/next.svg"
        ma.onClicked: next()
      }
    }

  }

  Component.onCompleted: {
    console.log("viewer loaded for ", imagesFolder);
    mainwindow.showMaximized();
  }
}
