import QtQuick 2.6
import QtQuick.Controls 1.4 as C1

import QtQuick.Layouts 1.1
import QtQuick.Window 2.0

RowLayout {
  opacity: 0.5
  property alias lbtn: lbtn
  property alias rbtn: rbtn
  ViewerButton {
    id: lbtn
  }
  ViewerButton {
    id: rbtn
  }
}
