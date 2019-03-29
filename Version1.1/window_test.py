from PyQt5 import QtWidgets
import sys
import panel


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    m = panel.navigation_mainwindow()
    m.show()
    app.installEventFilter(m)
    sys.exit(app.exec_())