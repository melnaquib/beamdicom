import QtQuick 2.0

Rectangle {
  id: btn

  property alias icon: img.source
  property alias ma: ma

  opacity: 0.5
  border.color: 'white'
  color: 'white'
  width: 30
  height: width

  Image {
    id: img
    anchors.fill: parent
    fillMode: Image.PreserveAspectFit
  }
  MouseArea {
    id: ma
    anchors.fill: parent
    onClicked: if(btn.onClickedFn) btn.onClickedFn()
  }
}
