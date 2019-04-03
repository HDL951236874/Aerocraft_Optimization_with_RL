
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import RL_GA.navigation_mainwindow
import RL_GA.main
import math

class navigation_mainwindow(RL_GA.navigation_mainwindow.Ui_navigation_mainwindow):
    def __init__(self):
        super(navigation_mainwindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.pushButton.clicked.connect(self.start_simulation)
        self.m1 = PlotCanvas(self, width=10, height=3)
        self.m1.move(350,50)
        self.m2 = PlotCanvas(self, width=5, height=3)
        self.m2.move(300,400)
        self.m3 = PlotCanvas(self, width=5, height=3)
        self.m3.move(900,400)

    def start_simulation(self):
        if self.comboBox.currentText() == 'classic':
            self.x,self.y,self.xt,self.yt,self.l1,self.V,self.l2,self.ny = RL_GA.main.main(
                float(self.lineEdit.text()),
                float(self.lineEdit_2.text()),
                float(self.lineEdit_3.text()),
                float(self.lineEdit_4.text())/float(self.lineEdit_18.text())*math.pi,
                float(self.lineEdit_5.text()),
                float(self.lineEdit_6.text()),
                float(self.lineEdit_7.text()),
                float(self.lineEdit_8.text()),
                float(self.lineEdit_9.text()),
                float(self.lineEdit_10.text()),
                float(self.lineEdit_11.text()),
                float(self.lineEdit_12.text()),
                float(self.lineEdit_13.text()),
                float(self.lineEdit_14.text()),
                float(self.lineEdit_15.text()),
                float(self.lineEdit_16.text()),
                float(self.lineEdit_17.text()),
                2
            )
        if self.comboBox.currentText() == 'GA':
            S = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 2, 4, 2, 2]
            S_new = []
            for i in range(len(S)):
                S_new += [float(S[i])] * 50
            self.x, self.y, self.xt, self.yt, self.l1, self.V, self.l2, self.ny = RL_GA.main.main(
                float(self.lineEdit.text()),
                float(self.lineEdit_2.text()),
                float(self.lineEdit_3.text()),
                float(self.lineEdit_4.text()) / float(self.lineEdit_18.text())*math.pi,
                float(self.lineEdit_5.text()),
                float(self.lineEdit_6.text()),
                float(self.lineEdit_7.text()),
                float(self.lineEdit_8.text()),
                float(self.lineEdit_9.text()),
                float(self.lineEdit_10.text()),
                float(self.lineEdit_11.text()),
                float(self.lineEdit_12.text()),
                float(self.lineEdit_13.text()),
                float(self.lineEdit_14.text()),
                float(self.lineEdit_15.text()),
                float(self.lineEdit_16.text()),
                float(self.lineEdit_17.text()),
                S_new
            )

        if self.comboBox.currentText() == 'RL':
            S = [2,2,3,2,3,2,3,2,3,3,4,4,3,2,4,2,2,3,3,3,3,3,3,3,3]
            S_new = []
            for i in range(len(S)):
                S_new += [float(S[i])] * 50
            self.x, self.y, self.xt, self.yt, self.l1, self.V, self.l2, self.ny = RL_GA.main.main(
                float(self.lineEdit.text()),
                float(self.lineEdit_2.text()),
                float(self.lineEdit_3.text()),
                float(self.lineEdit_4.text()) / float(self.lineEdit_18.text())*math.pi,
                float(self.lineEdit_5.text()),
                float(self.lineEdit_6.text()),
                float(self.lineEdit_7.text()),
                float(self.lineEdit_8.text()),
                float(self.lineEdit_9.text()),
                float(self.lineEdit_10.text()),
                float(self.lineEdit_11.text()),
                float(self.lineEdit_12.text()),
                float(self.lineEdit_13.text()),
                float(self.lineEdit_14.text()),
                float(self.lineEdit_15.text()),
                float(self.lineEdit_16.text()),
                float(self.lineEdit_17.text()),
                S_new
            )
        self.m1.axes.cla()
        self.m1.axes.plot(self.x, self.y)
        self.m1.axes.plot(self.xt,self.yt)
        self.m1.draw()
        self.m2.axes.cla()
        self.m2.axes.plot(self.l1,self.V)
        self.m2.draw()
        self.m3.axes.cla()
        self.m3.axes.plot(self.l2,self.ny)
        self.m3.draw()

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



