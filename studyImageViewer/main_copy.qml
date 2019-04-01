import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtQuick.Window 2.0
import Qt.labs.folderlistmodel 2.1

ApplicationWindow {

  Rectangle {
    width: 100
    height: 100
    color: "red"
  }
 visible: true
  width: Screen.desktopAvailableWidth
  height: Screen.desktopAvailableHeight
   FolderListModel {
id: folderModel
nameFilters: ["*.jpg, *.png"]

    //folder: "file:///C:/Documents and Settings/RUPESH/Desktop/mobile_image"
    folder: "file:///C:/Users/My Pictures/outing on 8-Jan2011/NewYearOuting"
          Component.onCompleted: {
        console.log("FOLDER " + imagesFolder);
        console.log("FOLDER " + files);
        console.log("FOLDER " + typeof(files));
//        folderModel.folder = imagesFolder;
      }


Component {
    id: fileDelegate
    Row {
        Image {
            width: 150; height: 150
            fillMode: Image.PreserveAspectFit
            smooth: true
            source: 'file:///' + imagesFolder + '/' + files[index]
        }
        Text { text: fileName }
    }
}
}
}