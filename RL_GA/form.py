# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(856, 651)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(300, 200, 181, 61))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 280, 89, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Miss Ji is beautiful"))
        self.pushButton.setText(_translate("Form", "PushButton"))

