from sys import exit, argv
from collections import Counter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QGuiApplication, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QWidget, QMessageBox
from numpy import array, min, max, where, zeros, any
from os import path
from PIL import Image

from molpub.layouts import HighlightStructureImage, Figure


root_path = path.dirname(path.abspath(__file__)).replace("\\", "/")


class ImageWindow1(object):

    def __init__(self):
        self.graphicsView = None

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 90, 491, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(570, 110, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(650, 110, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(580, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(root_path + "/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_7.setIcon(icon1)
        # self.pushButton_7.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_7.setText("refresh")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(570, 30, 40, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(root_path + "/icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon2)
        self.pushButton_8.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_8.setObjectName("pushButton_8")

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(90, 30, 481, 41))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label_3.setText(_translate("Form", "remove"))
        self.pushButton_4.setText(_translate("Form", "redo"))
        self.pushButton_3.setText(_translate("Form", "undo"))
        self.pushButton_5.setText(_translate("Form", "back"))
        self.pushButton_6.setText(_translate("Form", "next"))
        self.label.setText(_translate("Form", "path"))


class ImageWindow2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 90, 491, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(580, 200, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(650, 200, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(650, 100, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(580, 100, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(650, 150, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(580, 150, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(580, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(root_path + "/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_7.setIcon(icon1)
        # self.pushButton_7.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_7.setText("refresh")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label_3.setText(_translate("Form", "range"))
        self.pushButton_4.setText(_translate("Form", "redo"))
        self.pushButton_3.setText(_translate("Form", "undo"))
        self.pushButton_5.setText(_translate("Form", "back"))
        self.pushButton_6.setText(_translate("Form", "next"))
        self.comboBox_2.setItemText(0, _translate("Form", "cartoon"))
        self.comboBox_2.setItemText(1, _translate("Form", "cell"))
        self.comboBox_2.setItemText(2, _translate("Form", "dots"))
        self.comboBox_2.setItemText(3, _translate("Form", "label"))
        self.comboBox_2.setItemText(4, _translate("Form", "lines"))
        self.comboBox_2.setItemText(5, _translate("Form", "mesh"))
        self.comboBox_2.setItemText(6, _translate("Form", "nb_spheres"))
        self.comboBox_2.setItemText(7, _translate("Form", "ribbon"))
        self.comboBox_2.setItemText(8, _translate("Form", "slice"))
        self.comboBox_2.setItemText(9, _translate("Form", "spheres"))
        self.comboBox_2.setItemText(10, _translate("Form", "sticks"))
        self.comboBox_2.setItemText(11, _translate("Form", "surface"))
        self.label_4.setText(_translate("Form", "style"))
        self.comboBox_3.setItemText(0, _translate("Form", "chain"))
        self.comboBox_3.setItemText(1, _translate("Form", "model"))
        self.comboBox_3.setItemText(2, _translate("Form", "position"))
        self.comboBox_3.setItemText(3, _translate("Form", "range"))
        self.comboBox_3.setItemText(4, _translate("Form", "residue"))
        self.comboBox_3.setItemText(5, _translate("Form", "segment"))
        self.label_5.setText(_translate("Form", "class"))


class ImageWindow3(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".././icons/logo.pnsvgg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 90, 491, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(580, 180, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(650, 180, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(580, 135, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textEdit_1 = QtWidgets.QTextEdit(Form)
        self.textEdit_1.setGeometry(QtCore.QRect(650, 135, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit_1")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(580, 90, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(650, 90, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(580, 240, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textEdit_3 = QtWidgets.QTextEdit(Form)
        self.textEdit_3.setGeometry(QtCore.QRect(650, 240, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_3")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(580, 285, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.textEdit_4 = QtWidgets.QTextEdit(Form)
        self.textEdit_4.setGeometry(QtCore.QRect(650, 285, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_4.setFont(font)
        self.textEdit_4.setObjectName("textEdit_4")

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(580, 330, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.textEdit_5 = QtWidgets.QTextEdit(Form)
        self.textEdit_5.setGeometry(QtCore.QRect(650, 330, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_5.setFont(font)
        self.textEdit_5.setObjectName("textEdit_5")

        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(580, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(root_path + "/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_7.setIcon(icon1)
        # self.pushButton_7.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_7.setText("refresh")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label_3.setText(_translate("Form", "rotate z"))
        self.pushButton_4.setText(_translate("Form", "redo"))
        self.pushButton_3.setText(_translate("Form", "undo"))
        self.pushButton_5.setText(_translate("Form", "back"))
        self.pushButton_6.setText(_translate("Form", "next"))
        self.label_4.setText(_translate("Form", "rotate y"))
        self.label_5.setText(_translate("Form", "rotate x"))
        self.label_6.setText(_translate("Form", "move x"))
        self.label_7.setText(_translate("Form", "move y"))
        self.label_8.setText(_translate("Form", "move z"))


class ImageWindow4(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 90, 491, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(580, 200, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(650, 200, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(650, 150, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(580, 150, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.textEdit_1 = QtWidgets.QTextEdit(Form)
        self.textEdit_1.setGeometry(QtCore.QRect(650, 100, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit_1")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(580, 100, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(580, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(root_path + "/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_7.setIcon(icon1)
        # self.pushButton_7.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_7.setText("refresh")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label_3.setText(_translate("Form", "range"))
        self.pushButton_4.setText(_translate("Form", "redo"))
        self.pushButton_3.setText(_translate("Form", "undo"))
        self.pushButton_5.setText(_translate("Form", "back"))
        self.pushButton_6.setText(_translate("Form", "next"))
        self.comboBox_3.setItemText(0, _translate("Form", "chain"))
        self.comboBox_3.setItemText(1, _translate("Form", "model"))
        self.comboBox_3.setItemText(2, _translate("Form", "position"))
        self.comboBox_3.setItemText(3, _translate("Form", "range"))
        self.comboBox_3.setItemText(4, _translate("Form", "residue"))
        self.comboBox_3.setItemText(5, _translate("Form", "segment"))
        self.label_5.setText(_translate("Form", "class"))
        self.label_4.setText(_translate("Form", "color"))


class StructureImage1(QMainWindow, ImageWindow1):

    # noinspection PyGlobalUndefined
    def __init__(self):
        super(StructureImage1, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        image_list = []
        structure = None
        self.draw_number = 0
        self.folder_text = []
        self.remove_text = []

        # noinspection PyUnresolvedReferences
        self.pushButton_8.clicked.connect(self.load_structures)
        # noinspection PyUnresolvedReferences
        self.pushButton_7.clicked.connect(self.draw_structure)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.pushButton_4.clicked.connect(self.set_redo)

    def load_structures(self):
        structure_names, _ = QFileDialog.getOpenFileNames(self, 'Open file', '.', "Structure (*.pdb *.cif)")
        for structure_name in structure_names:
            self.textBrowser.append(structure_name)

    def draw_structure(self):
        global image_list
        global structure

        structure_paths = [file for file in self.textBrowser.toPlainText().split("\n")]
        if self.draw_number == 0:
            structure = HighlightStructureImage(structure_paths=structure_paths)

        if self.textEdit.toPlainText() != "":
            structure.set_cache(cache_contents=[self.textEdit.toPlainText()])

        structure.save(save_path="./temp/image" + str(self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.draw_number) + ".pse")

        if self.draw_number < len(image_list):
            image_list = image_list[:self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.draw_number) + ".png")

        if self.draw_number < len(self.folder_text):
            self.folder_text = self.folder_text[:self.draw_number + 1]
            self.folder_text[self.draw_number] = self.textBrowser.toPlainText()
        else:
            self.folder_text.append(self.textBrowser.toPlainText())

        if self.draw_number < len(self.remove_text):
            self.remove_text = self.remove_text[:self.draw_number + 1]
            self.remove_text[self.draw_number] = self.textEdit.toPlainText()
        else:
            self.remove_text.append(self.textEdit.toPlainText())

        figure = QPixmap("./temp/image" + str(self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number - 2])
            self.textEdit.setText(self.remove_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            structure.clear()
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText("")
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number])
            self.textEdit.setText(self.remove_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[-1])
            self.textEdit.setText(self.remove_text[-1])

    def window_clear(self):
        global image_list
        global structure

        image_list = []
        if structure is not None:
            structure.close()
        self.draw_number = 0
        self.folder_text = []
        self.remove_text = []

        self.textBrowser.clear()
        self.textEdit.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)


class StructureImage2(QMainWindow, ImageWindow2):

    # noinspection PyGlobalUndefined
    def __init__(self):
        super(StructureImage2, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.style_text = []
        self.class_text = []
        self.range_text = []

        # noinspection PyUnresolvedReferences
        self.pushButton_7.clicked.connect(self.draw_structure)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    # noinspection PyGlobalUndefined
    def draw_structure(self):
        global structure
        global image_list

        representation = self.comboBox_2.currentText()
        shading_type = self.comboBox_3.currentText()
        content = self.textEdit.toPlainText()

        structure.set_shape(representation_plan=[(shading_type + ":" + content, representation)],
                            initial_representation=None, independent_color=True, closed_surface=True)
        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.style_text):
            self.style_text = self.style_text[:self.draw_number + 1]
            self.style_text[self.draw_number] = representation
        else:
            self.style_text.append(representation)

        if self.draw_number < len(self.class_text):
            self.class_text = self.class_text[:self.draw_number + 1]
            self.class_text[self.draw_number] = shading_type
        else:
            self.class_text.append(shading_type)

        if self.draw_number < len(self.range_text):
            self.range_text = self.range_text[:self.draw_number + 1]
            self.range_text[self.draw_number] = content
        else:
            self.range_text.append(content)

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentText(self.style_text[self.draw_number - 2])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number - 2])
            self.textEdit.setText(self.range_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentIndex(0)
            self.comboBox_3.setCurrentIndex(0)
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)
            self.comboBox_2.setCurrentText(self.style_text[self.draw_number])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number])
            self.textEdit.setText(self.range_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")
            self.comboBox_2.setCurrentText(self.style_text[-1])
            self.comboBox_3.setCurrentText(self.class_text[-1])
            self.textEdit.setText(self.range_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.style_text = []
        self.class_text = []
        self.range_text = []

        self.textEdit.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    # noinspection PyGlobalUndefined
    def window_initialization(self):
        global structure
        global image_list

        if len(image_list) > 0:
            self.draw_number = 0
            self.style_text = []
            self.class_text = []
            self.range_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


class StructureImage3(QMainWindow, ImageWindow3):

    # noinspection PyGlobalUndefined
    def __init__(self):
        super(StructureImage3, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.rotatex_text = []
        self.rotatey_text = []
        self.rotatez_text = []
        self.movex_text = []
        self.movey_text = []
        self.movez_text = []

        # noinspection PyUnresolvedReferences
        self.pushButton_7.clicked.connect(self.draw_structure)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    # noinspection PyGlobalUndefined
    def draw_structure(self):
        global structure
        global image_list

        rotate_x = int(self.textEdit_2.toPlainText()) if self.textEdit_2.toPlainText() != "" else 0
        rotate_y = int(self.textEdit_1.toPlainText()) if self.textEdit_1.toPlainText() != "" else 0
        rotate_z = int(self.textEdit.toPlainText()) if self.textEdit.toPlainText() != "" else 0
        move_x = int(self.textEdit_3.toPlainText()) if self.textEdit_3.toPlainText() != "" else 0
        move_y = int(self.textEdit_4.toPlainText()) if self.textEdit_4.toPlainText() != "" else 0
        move_z = int(self.textEdit_5.toPlainText()) if self.textEdit_5.toPlainText() != "" else 0
        rotate = [rotate_x, rotate_y, rotate_z]

        if move_x == 0 and move_y == 0 and move_z == 0:
            if self.draw_number > 0:
                structure.set_state(rotate=rotate, only_rotate=True)
            else:
                structure.set_state(rotate=rotate)
        else:
            translate = [move_x, move_y, move_z]
            structure.set_state(rotate=rotate, translate=translate)

        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.rotatex_text):
            self.rotatex_text = self.rotatex_text[:self.draw_number + 1]
            self.rotatex_text[self.draw_number] = self.textEdit_2.toPlainText()
        else:
            self.rotatex_text.append(self.textEdit_2.toPlainText())

        if self.draw_number < len(self.rotatey_text):
            self.rotatey_text = self.rotatey_text[:self.draw_number + 1]
            self.rotatey_text[self.draw_number] = self.textEdit_1.toPlainText()
        else:
            self.rotatey_text.append(self.textEdit_1.toPlainText())

        if self.draw_number < len(self.rotatez_text):
            self.rotatez_text = self.rotatez_text[:self.draw_number + 1]
            self.rotatez_text[self.draw_number] = self.textEdit.toPlainText()
        else:
            self.rotatez_text.append(self.textEdit.toPlainText())

        if self.draw_number < len(self.movex_text):
            self.movex_text = self.movex_text[:self.draw_number + 1]
            self.movex_text[self.draw_number] = self.textEdit_3.toPlainText()
        else:
            self.movex_text.append(self.textEdit_3.toPlainText())

        if self.draw_number < len(self.movey_text):
            self.movey_text = self.movey_text[:self.draw_number + 1]
            self.movey_text[self.draw_number] = self.textEdit_4.toPlainText()
        else:
            self.movey_text.append(self.textEdit_4.toPlainText())

        if self.draw_number < len(self.movez_text):
            self.movez_text = self.movez_text[:self.draw_number + 1]
            self.movez_text[self.draw_number] = self.textEdit_5.toPlainText()
        else:
            self.movez_text.append(self.textEdit_5.toPlainText())

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_2.setText(self.rotatex_text[self.draw_number - 2])
            self.textEdit_1.setText(self.rotatey_text[self.draw_number - 2])
            self.textEdit.setText(self.rotatez_text[self.draw_number - 2])
            self.textEdit_3.setText(self.movex_text[self.draw_number - 2])
            self.textEdit_4.setText(self.movey_text[self.draw_number - 2])
            self.textEdit_5.setText(self.movez_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit.setText("")
            self.textEdit_1.setText("")
            self.textEdit_2.setText("")
            self.textEdit_3.setText("")
            self.textEdit_4.setText("")
            self.textEdit_5.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_2.setText(self.rotatex_text[self.draw_number])
            self.textEdit_1.setText(self.rotatey_text[self.draw_number])
            self.textEdit.setText(self.rotatez_text[self.draw_number])
            self.textEdit_3.setText(self.movex_text[self.draw_number])
            self.textEdit_4.setText(self.movey_text[self.draw_number])
            self.textEdit_5.setText(self.movez_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")

            self.textEdit_2.setText(self.rotatex_text[-1])
            self.textEdit_1.setText(self.rotatey_text[-1])
            self.textEdit.setText(self.rotatez_text[-1])
            self.textEdit_3.setText(self.movex_text[-1])
            self.textEdit_4.setText(self.movey_text[-1])
            self.textEdit_5.setText(self.movez_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.rotatex_text = []
        self.rotatey_text = []
        self.rotatez_text = []
        self.movex_text = []
        self.movey_text = []
        self.movez_text = []

        self.textEdit.clear()
        self.textEdit_1.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    def window_initialization(self):
        global structure
        global image_list
        if len(image_list) > 0:
            self.draw_number = 0
            self.rotatex_text = []
            self.rotatey_text = []
            self.rotatez_text = []
            self.movex_text = []
            self.movey_text = []
            self.movez_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.textEdit_1.clear()
            self.textEdit_2.clear()
            self.textEdit_3.clear()
            self.textEdit_4.clear()
            self.textEdit_5.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


class StructureImage4(QMainWindow, ImageWindow4):

    # noinspection PyGlobalUndefined
    def __init__(self):
        super(StructureImage4, self).__init__()
        self.setupUi(self)
        global image_list
        global structure
        self.draw_number = 0
        self.start_number = 0
        self.color_text = []
        self.class_text = []
        self.range_text = []

        # noinspection PyUnresolvedReferences
        self.pushButton_7.clicked.connect(self.draw_structure)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.pushButton_4.clicked.connect(self.set_redo)

    def start_image(self):
        if len(image_list) > 0:
            self.scene.addPixmap(QPixmap(image_list[-1]))
            self.graphicsView.setScene(self.scene)
            self.start_number = len(image_list)

    def draw_structure(self):
        global structure
        global image_list

        color = self.textEdit_1.toPlainText()
        shading_type = self.comboBox_3.currentText()
        range = self.textEdit.toPlainText()

        structure.set_color(coloring_plan=[(shading_type + ":" + range, color)], initial_color=None)
        structure.save(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".png")
        structure.save_pymol(save_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")

        if self.start_number + self.draw_number < len(image_list):
            image_list = image_list[:self.start_number + self.draw_number + 1]
        else:
            image_list.append("./temp/image" + str(self.start_number + self.draw_number) + ".png")

        if self.draw_number < len(self.color_text):
            self.color_text = self.color_text[:self.draw_number + 1]
            self.color_text[self.draw_number] = color
        else:
            self.color_text.append(color)

        if self.draw_number < len(self.class_text):
            self.class_text = self.class_text[:self.draw_number + 1]
            self.class_text[self.draw_number] = shading_type
        else:
            self.class_text.append(shading_type)

        if self.draw_number < len(self.range_text):
            self.range_text = self.range_text[:self.draw_number + 1]
            self.range_text[self.draw_number] = range
        else:
            self.range_text.append(range)

        figure = QPixmap("./temp/image" + str(self.start_number + self.draw_number) + ".png")
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def save_image(self, label_text, ratio):
        global structure
        global image_list
        if len(image_list) > 0:
            structure.save(save_path="./temp/panel_" + label_text + ".png", ratio=ratio)

    def set_undo(self):
        global image_list
        global structure

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number - 2])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 2) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText(self.color_text[self.draw_number - 2])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number - 2])
            self.textEdit.setText(self.range_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number - 1])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText("")
            self.comboBox_3.setCurrentIndex(0)
            self.textEdit.setText("")
            self.draw_number = 0

    def set_redo(self):
        global image_list
        global structure

        if self.start_number + self.draw_number < len(image_list):
            self.scene.clear()
            figure = QPixmap(image_list[self.start_number + self.draw_number])
            self.scene.addPixmap(figure)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number) + ".pse")
            self.graphicsView.setScene(self.scene)

            self.textEdit_1.setText(self.color_text[self.draw_number])
            self.comboBox_3.setCurrentText(self.class_text[self.draw_number])
            self.textEdit.setText(self.range_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(image_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number + self.draw_number - 1) + ".pse")

            self.textEdit_1.setText(self.color_text[-1])
            self.comboBox_3.setCurrentText(self.class_text[-1])
            self.textEdit.setText(self.range_text[-1])

    def window_clear(self):
        self.draw_number = 0
        self.start_number = 0
        self.color_text = []
        self.class_text = []
        self.range_text = []

        self.textEdit.clear()
        self.textEdit_1.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)

    def window_initialization(self):
        global structure
        global image_list

        if len(image_list) > 0:
            self.draw_number = 0
            self.color_text = []
            self.class_text = []
            self.range_text = []
            image_list = image_list[:self.start_number]

            self.textEdit.clear()
            self.textEdit_1.clear()
            self.scene.clear()
            self.scene.addPixmap(QPixmap(image_list[self.start_number - 1]))
            self.graphicsView.setScene(self.scene)
            structure.load_pymol(load_path="./temp/image" + str(self.start_number - 1) + ".pse")


class ClickSurface(object):

    # noinspection PyPep8Naming
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        # noinspection PyUnresolvedReferences
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(80, 25, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(260, 20, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(10, 80, 381, 201))
        self.graphicsView.setObjectName("graphicsView")

        self.button_group = QtWidgets.QButtonGroup()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # noinspection PyPep8Naming
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label_3.setText(_translate("Form", "label"))
        self.pushButton.setText(_translate("Form", "complete"))


class ContentWindow(object):

    # noinspection PyPep8Naming
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(90, 30, 481, 41))
        self.textBrowser.setObjectName("textBrowser")

        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(40, 90, 491, 481))
        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene()

        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 460, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(580, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(680, 520, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(570, 30, 41, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(root_path + "/icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon1)
        self.pushButton_7.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_7.setObjectName("pushButton_7")

        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(580, 400, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(root_path + "/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.pushButton_8.setIcon(icon2)
        # self.pushButton_8.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_8.setText("refresh")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.label.setText(_translate("Form", "path"))
        self.pushButton_4.setText(_translate("Form", "redo"))
        self.pushButton_3.setText(_translate("Form", "undo"))
        self.pushButton_5.setText(_translate("Form", "back"))
        self.pushButton_6.setText(_translate("Form", "next"))


class SelectionWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 80, 300, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 80, 300, 300))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 490, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PyMOL-PUB surface"))
        self.pushButton.setText(_translate("Form", "structure\n""image"))
        self.pushButton_2.setText(_translate("Form", "statistical\n""content"))
        self.pushButton_3.setText(_translate("Form", "back"))


class DetailWindow(QWidget, ClickSurface):
    def __init__(self, layout, order):
        super(DetailWindow, self).__init__()
        self.detail_button_list = None
        self.setupUi(self)
        self.draw_layout(layout, order)

    def draw_layout(self, layout, order):
        width = 370 / layout[1]
        height = 190 / layout[0]
        self.detail_button_list = []

        for i in range(layout[0] * layout[1]):
            button = QPushButton(self)
            self.detail_button_list.append(button)
            self.detail_button_list[i].resize(int(width), int(height))
            self.detail_button_list[i].move(int(12 + i % layout[1] * (375.0 / layout[1])),
                                            int(82 + i // layout[1] * (195.0 / layout[0])))
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(16)
            self.detail_button_list[i].setFont(font)
            self.detail_button_list[i].setObjectName("push_button" + str(i))
            if i == order:
                self.detail_button_list[i].setStyleSheet("border: 3px dashed black; background: #FFE699;")
                self.detail_button_list[i].setText("select")
            else:
                self.detail_button_list[i].setStyleSheet("border: 3px dashed black;")
            self.button_group.addButton(self.detail_button_list[i], i)
            self.detail_button_list[i].show()


class SelectWindow(QMainWindow, SelectionWindow):
    def __init__(self):
        super(SelectWindow, self).__init__()
        self.setupUi(self)


class StatisticalWindow(QMainWindow, ContentWindow):

    # noinspection PyGlobalUndefined
    def __init__(self):
        global statistical_list
        super(StatisticalWindow, self).__init__()
        self.setupUi(self)
        statistical_list = []
        self.draw_number = 0
        self.folder_text = []

        # noinspection PyUnresolvedReferences
        self.pushButton_7.clicked.connect(self.add_statistical)
        # noinspection PyUnresolvedReferences
        self.pushButton_8.clicked.connect(self.show_statistical)
        # noinspection PyUnresolvedReferences
        self.pushButton_3.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.pushButton_4.clicked.connect(self.set_redo)

    def add_statistical(self):
        figure_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "Figure (*.png *.jpg *.bmp)")
        self.textBrowser.append(figure_name)

    def show_statistical(self):
        global statistical_list

        statistical_path = self.textBrowser.toPlainText().strip("\n")

        if self.draw_number < len(statistical_list):
            statistical_list = statistical_list[:self.draw_number + 1]
            statistical_list[self.draw_number] = statistical_path
        else:
            statistical_list.append(statistical_path)

        if self.draw_number < len(self.folder_text):
            self.folder_text = self.folder_text[:self.draw_number + 1]
            self.folder_text[self.draw_number] = self.textBrowser.toPlainText()
        else:
            self.folder_text.append(self.textBrowser.toPlainText())

        figure = QPixmap(statistical_path)
        self.scene.clear()
        self.scene.addPixmap(figure)
        self.graphicsView.setScene(self.scene)

        self.draw_number += 1

    def save_image(self, label_text, manuscript_format):
        global statistical_list
        if len(statistical_list) > 0:
            image_data = Image.open(fp=statistical_list[-1])

            if manuscript_format == "PNAS" or manuscript_format == "ACS":
                minimum_dpi = 600
            elif manuscript_format == "Oxford":
                minimum_dpi = 350
            else:
                minimum_dpi = 300

            if image_data.info["dpi"][0] < minimum_dpi:
                reply = QMessageBox.question(self, "Ask",
                                             "The image you selected does not meet the minimum dpi requirement of the "
                                             "current journal.\nDo you agree to increase the dpi of this image?\n(If "
                                             "you select \"no\" or \"cancel\", the image will not be exported "
                                             "successfully.)",
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    image_data.info["dpi"] = (minimum_dpi + 50, minimum_dpi + 50)

            if image_data.info["dpi"][0] < minimum_dpi:
                statistical_list = []
            else:
                newfile_path = "./temp/panel_" + label_text + ".png"
                image_data.save(fp=newfile_path, quality=95, dpi=(minimum_dpi + 50, minimum_dpi + 50))

    def set_undo(self):
        global statistical_list

        if self.draw_number > 1:
            self.scene.clear()
            figure = QPixmap(statistical_list[self.draw_number - 2])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.scene.clear()
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText("")
            self.draw_number = 0

    def set_redo(self):
        global statistical_list

        if self.draw_number < len(statistical_list):
            self.scene.clear()
            figure = QPixmap(statistical_list[self.draw_number])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[self.draw_number])
            self.draw_number += 1
        else:
            self.scene.clear()
            figure = QPixmap(statistical_list[-1])
            self.scene.addPixmap(figure)
            self.graphicsView.setScene(self.scene)
            self.textBrowser.setText(self.folder_text[-1])

    def window_clear(self):
        global statistical_list

        statistical_list = []
        self.draw_number = 0
        self.folder_text = []

        self.textBrowser.clear()
        self.scene.clear()
        self.graphicsView.setScene(self.scene)


class MainWindow(object):

    def __init__(self):
        self.central_widget = None
        self.history_label, self.history_browser, self.history_button = None, None, None
        self.targets_label, self.targets_combo_box = None, None
        self.occupied_label, self.occupied_text_edit = None, None
        self.radio_label, self.radio_text_edit = None, None
        self.total_column_label, self.total_column_combo_box = None, None
        self.graphics_view, self.button_group, self.push_button_1 = None, None, None
        self.layout_label, self.layout_combo_box = None, None
        self.implement_label, self.implement_combo_box = None, None
        self.undo_button, self.redo_button = None, None
        self.output_button = None
        self.progress_label, self.progress_bar = None, None
        self.molpub = None

    # noinspection PyPep8Naming
    def setupUi(self, PyMOL):
        PyMOL.setObjectName("PyMOL")
        PyMOL.setWindowModality(QtCore.Qt.ApplicationModal)
        PyMOL.setFixedSize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PyMOL.setWindowIcon(icon)

        self.central_widget = QtWidgets.QWidget(PyMOL)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.history_label = QtWidgets.QLabel(self.central_widget)
        self.history_label.setGeometry(QtCore.QRect(20, 20, 60, 40))
        self.history_label.setFont(font)
        self.history_label.setAlignment(QtCore.Qt.AlignVCenter)

        self.history_browser = QtWidgets.QTextBrowser(self.central_widget)
        self.history_browser.setGeometry(QtCore.QRect(80, 20, 650, 40))
        self.history_browser.setFont(font)
        self.history_browser.setObjectName("textBrowser")

        self.history_button = QtWidgets.QPushButton(self.central_widget)
        self.history_button.setGeometry(QtCore.QRect(740, 20, 40, 40))
        self.history_button.setFont(font)
        self.history_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(root_path + "/icons/folder.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.history_button.setIcon(icon)
        self.history_button.setIconSize(QtCore.QSize(30, 30))
        self.history_button.setObjectName("pushButton")

        self.targets_label = QtWidgets.QLabel(self.central_widget)
        self.targets_label.setGeometry(QtCore.QRect(20, 70, 60, 40))
        self.targets_label.setFont(font)
        self.targets_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.targets_combo_box = QtWidgets.QComboBox(self.central_widget)
        self.targets_combo_box.setGeometry(QtCore.QRect(80, 70, 120, 40))
        new_font = QtGui.QFont()
        new_font.setFamily("Arial")
        new_font.setPointSize(12)
        new_font.setBold(False)
        new_font.setItalic(True)
        new_font.setWeight(50)
        self.targets_combo_box.setFont(new_font)
        self.targets_combo_box.setObjectName("comboBox")
        self.targets_combo_box.addItems(["" for _ in range(8)])

        self.radio_label = QtWidgets.QLabel(self.central_widget)
        self.radio_label.setGeometry(QtCore.QRect(240, 70, 100, 40))
        self.radio_label.setFont(font)
        self.radio_label.setAlignment(QtCore.Qt.AlignVCenter)

        self.radio_text_edit = QtWidgets.QTextEdit(self.central_widget)
        self.radio_text_edit.setGeometry(QtCore.QRect(350, 70, 50, 40))
        self.radio_text_edit.setFont(font)
        self.radio_text_edit.setObjectName("textEdit_1")
        PyMOL.setCentralWidget(self.central_widget)

        self.occupied_label = QtWidgets.QLabel(self.central_widget)
        self.occupied_label.setGeometry(QtCore.QRect(430, 70, 120, 40))
        self.occupied_label.setFont(font)
        self.occupied_label.setAlignment(QtCore.Qt.AlignVCenter)

        self.occupied_text_edit = QtWidgets.QTextEdit(self.central_widget)
        self.occupied_text_edit.setGeometry(QtCore.QRect(560, 70, 50, 40))
        self.occupied_text_edit.setFont(font)
        self.occupied_text_edit.setObjectName("textEdit")
        PyMOL.setCentralWidget(self.central_widget)

        self.total_column_label = QtWidgets.QLabel(self.central_widget)
        self.total_column_label.setGeometry(QtCore.QRect(640, 70, 90, 40))
        self.total_column_label.setFont(font)
        self.total_column_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.total_column_combo_box = QtWidgets.QComboBox(self.central_widget)
        self.total_column_combo_box.setGeometry(QtCore.QRect(740, 70, 40, 40))
        self.total_column_combo_box.setFont(font)
        self.total_column_combo_box.setObjectName("comboBox_2")
        self.total_column_combo_box.addItems(["" for _ in range(2)])
        self.total_column_combo_box.setEnabled(False)

        self.graphics_view = QtWidgets.QGraphicsView(self.central_widget)
        self.graphics_view.setGeometry(QtCore.QRect(20, 120, 760, 340))
        self.graphics_view.setObjectName("graphicsView")
        self.graphics_view.setScene(QtWidgets.QGraphicsScene())

        self.button_group = QtWidgets.QButtonGroup()
        self.push_button_1 = QtWidgets.QPushButton(self.central_widget)
        self.push_button_1.setGeometry(QtCore.QRect(25, 125, 750, 330))
        self.push_button_1.setFont(font)
        self.push_button_1.setObjectName("push_button_1")
        self.push_button_1.setStyleSheet("border: 1px dashed black; background: #B4C7E7;")
        self.button_group.addButton(self.push_button_1, 0)

        self.layout_label = QtWidgets.QLabel(self.central_widget)
        self.layout_label.setGeometry(QtCore.QRect(20, 470, 60, 40))
        self.layout_label.setFont(font)
        self.layout_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.layout_combo_box = QtWidgets.QComboBox(self.central_widget)
        self.layout_combo_box.setGeometry(QtCore.QRect(80, 470, 180, 40))
        self.layout_combo_box.setFont(font)
        self.layout_combo_box.setObjectName("comboBox_3")
        self.layout_combo_box.addItems(["" for _ in range(4)])

        self.implement_label = QtWidgets.QLabel(self.central_widget)
        self.implement_label.setGeometry(QtCore.QRect(290, 470, 80, 40))
        self.implement_label.setFont(font)
        self.implement_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.implement_combo_box = QtWidgets.QComboBox(self.central_widget)
        self.implement_combo_box.setGeometry(QtCore.QRect(375, 470, 55, 40))
        self.implement_combo_box.setFont(font)
        self.implement_combo_box.setObjectName("comboBox_4")
        self.implement_combo_box.addItem("")

        line = QtWidgets.QFrame(self.central_widget)
        line.setGeometry(QtCore.QRect(455, 470, 10, 40))
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.undo_button = QtWidgets.QPushButton(self.central_widget)
        self.undo_button.setGeometry(QtCore.QRect(480, 470, 80, 40))
        self.undo_button.setFont(font)
        self.undo_button.setObjectName("pushButton_3")

        self.redo_button = QtWidgets.QPushButton(self.central_widget)
        self.redo_button.setGeometry(QtCore.QRect(580, 470, 80, 40))
        self.redo_button.setFont(font)
        self.redo_button.setObjectName("pushButton_4")

        line = QtWidgets.QFrame(self.central_widget)
        line.setGeometry(QtCore.QRect(675, 470, 10, 40))
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.output_button = QtWidgets.QPushButton(self.central_widget)
        self.output_button.setGeometry(QtCore.QRect(700, 470, 80, 40))
        self.output_button.setFont(font)
        self.output_button.setObjectName("pushButton_2")

        line = QtWidgets.QFrame(self.central_widget)
        line.setGeometry(QtCore.QRect(20, 515, 760, 10))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.progress_label = QtWidgets.QLabel(self.central_widget)
        self.progress_label.setGeometry(QtCore.QRect(300, 520, 200, 40))
        self.progress_label.setFont(font)
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar = QtWidgets.QProgressBar(self.central_widget)
        self.progress_bar.setGeometry(QtCore.QRect(20, 560, 760, 20))
        self.progress_bar.setFont(font)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")

        self.retranslateUi(PyMOL)
        QtCore.QMetaObject.connectSlotsByName(PyMOL)

        self.molpub = PyMOL

    # noinspection PyPep8Naming
    def retranslateUi(self, PyMOL):
        _translate = QtCore.QCoreApplication.translate
        PyMOL.setWindowTitle(_translate("PyMOL", "PyMOL-PUB surface"))
        self.history_label.setText(_translate("PyMOL", "history:"))
        self.targets_label.setText(_translate("PyMOL", "targets:"))
        self.targets_combo_box.setItemText(0, _translate("PyMOL", "Nature"))
        self.targets_combo_box.setItemText(1, _translate("PyMOL", "Science"))
        self.targets_combo_box.setItemText(2, _translate("PyMOL", "Cell"))
        self.targets_combo_box.setItemText(3, _translate("PyMOL", "PNAS"))
        self.targets_combo_box.setItemText(4, _translate("PyMOL", "ACS"))
        self.targets_combo_box.setItemText(5, _translate("PyMOL", "Oxford"))
        self.targets_combo_box.setItemText(6, _translate("PyMOL", "PLOS"))
        self.targets_combo_box.setItemText(7, _translate("PyMOL", "IEEE"))
        self.radio_label.setText(_translate("PyMOL", "height / weight:"))
        self.occupied_label.setText(_translate("PyMOL", "occupied column:"))
        self.total_column_label.setText(_translate("PyMOL", "total column:"))
        self.total_column_combo_box.setItemText(0, _translate("PyMOL", "2"))
        self.total_column_combo_box.setItemText(1, _translate("PyMOL", "3"))
        self.layout_label.setText(_translate("PyMOL", "layouts"))
        self.layout_combo_box.setItemText(0, _translate("PyMOL", "+ a row of panels"))
        self.layout_combo_box.setItemText(1, _translate("PyMOL", "- a row of panels"))
        self.layout_combo_box.setItemText(2, _translate("PyMOL", "+ a column of panels"))
        self.layout_combo_box.setItemText(3, _translate("PyMOL", "- a column of panels"))
        self.implement_label.setText(_translate("PyMOL", "implement"))
        self.implement_combo_box.setItemText(0, _translate("PyMOL", "a"))
        self.undo_button.setText(_translate("PyMOL", "undo"))
        self.redo_button.setText(_translate("PyMOL", "redo"))
        self.output_button.setText(_translate("PyMOL", "output"))
        self.progress_label.setText(_translate("PyMOL", "painting task progress"))
        self.push_button_1.setText(_translate("PyMOL", "a"))


class EntryWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(EntryWindow, self).__init__()
        self.setupUi(self)

        # noinspection PyUnresolvedReferences
        self.history_button.clicked.connect(self.add_history)
        self.layout = [1, 1]
        self.new_button_list = [self.push_button_1]
        self.detail_button_list = []
        self.detail_window = DetailWindow([1, 1], 0)
        self.current_label = ""
        self.combobox_label = ["a"]
        self.button_state = [1]
        self.case = None
        self.progress = 0.0
        self.draw_number = 0
        self.history_text = []
        self.targets_text = []
        self.occupied_text = []
        self.ratio_text = []
        self.format_text = []

        # noinspection PyUnresolvedReferences
        self.layout_combo_box.activated.connect(lambda: self.change_layout(self.layout_combo_box.currentIndex()))
        # noinspection PyUnresolvedReferences
        self.output_button.clicked.connect(self.figure_output)
        # noinspection PyUnresolvedReferences
        self.undo_button.clicked.connect(self.set_undo)
        # noinspection PyUnresolvedReferences
        self.redo_button.clicked.connect(self.set_redo)

    def add_history(self):
        figure_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "Figure (*.png *.pdf)")
        self.history_browser.append(figure_name)

    def change_layout(self, index):
        self.implement_combo_box.clear()
        self.combobox_label = []
        if index == 0:
            self.layout[0] += 1

        elif index == 1:
            if self.layout[0] > 1:
                self.layout[0] -= 1
            else:
                return "The figure needs at least one row of panels!"

        elif index == 2:
            self.layout[1] += 1

        else:
            if self.layout[1] > 1:
                self.layout[1] -= 1
            else:
                return "The figure needs at least one column of panels!"

        button_list = self.button_group.buttons()
        for button in button_list:
            self.button_group.removeButton(button)
            # noinspection PyTypeChecker
            button.setParent(None)

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.new_button_list, self.button_state = [], []
        width = int((750 - 5 * (self.layout[1] - 1)) / self.layout[1])
        height = int((330 - 5 * (self.layout[0] - 1)) / self.layout[0])
        for i in range(self.layout[0] * self.layout[1]):
            button = QPushButton(self.central_widget)
            button.setFont(font)
            button.setObjectName("push_button_" + str(i))
            button.setStyleSheet("border: 1px dashed black;")
            button.resize(width, height)
            button.move(25 + i % self.layout[1] * (width + 5), 125 + i // self.layout[1] * (height + 5))
            # noinspection PyUnresolvedReferences
            button.clicked.connect(self.show_detail)
            self.new_button_list.append(button)
            self.button_group.addButton(self.new_button_list[i], i)
            self.button_state.append(0)
            self.new_button_list[i].show()

    def check_surface(self, new_index):
        matrix = []
        for order, button in enumerate(self.new_button_list):
            matrix.append(button.text())
        matrix[new_index] = self.current_label
        matrix = array(matrix).reshape(self.layout)

        values = []
        for row in matrix:
            for value in row:
                if value != '':
                    values.append(ord(value) - 97)
                else:
                    values.append(-1)
        indices = array(values).reshape(self.layout)
        counter = Counter(indices.reshape(-1))
        order = sorted(list(counter.keys()))
        if order[0] == -1 and len(order) == 1:
            return True
        if order[0] == -1:
            order = order[1:]
        if order[0] != 0:
            return "The label should start from a!"
        if len(order) > 1:
            for former_index, latter_index in zip(order[:-1], order[1:]):
                if latter_index - former_index != 1:
                    return "The labels should be consecutive!"

        for index in order:
            xs, ys = where(indices == index)
            ranges = {"x": (min(xs), max(xs)), "y": (min(ys), max(ys))}
            chuck_matrix = zeros(shape=(ranges["x"][1] - ranges["x"][0] + 1, ranges["y"][1] - ranges["y"][0] + 1))
            for x, y in zip(xs, ys):
                chuck_matrix[x - ranges["x"][0], y - ranges["y"][0]] = 1
            if any(chuck_matrix != 1):
                return "The area covered by this label should be rectangular!"

        return True

    def show_detail(self):
        # noinspection PyTypeChecker
        order = self.new_button_list.index(self.sender())
        self.detail_window = DetailWindow(self.layout, order)
        self.detail_window.show()
        self.hide()

        # noinspection PyUnresolvedReferences
        self.detail_window.pushButton.clicked.connect(self.detail_window.hide)
        # noinspection PyUnresolvedReferences
        self.detail_window.pushButton.clicked.connect(self.show)
        # noinspection PyUnresolvedReferences
        self.detail_window.pushButton.clicked.connect(lambda: self.label_set(order))

    def label_set(self, order):
        self.current_label = self.detail_window.textEdit.toPlainText()
        warning_text = self.check_surface(order)

        if warning_text is True:
            if self.current_label == '':
                self.new_button_list[order].setText(self.current_label)
                self.new_button_list[order].setStyleSheet("border: 1px dashed black; background: #FFFFFF;")
            else:
                self.new_button_list[order].setText(self.current_label)
                self.new_button_list[order].setStyleSheet("border: 1px dashed black; background: #B4C7E7;")
                self.button_state[order] = 1
                if self.current_label not in self.combobox_label:
                    self.combobox_label.append(self.current_label)
                    self.implement_combo_box.addItem(self.current_label)
        else:
            QMessageBox.warning(self, "Illegal Label", warning_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    # noinspection PyGlobalUndefined
    def image_set(self):
        global image_list
        global statistical_list

        if len(image_list) > 0 or len(statistical_list) > 0:
            self.progress += 1

            for order, button in enumerate(self.new_button_list):
                if button.text() == self.implement_combo_box.currentText():
                    button.setStyleSheet("border: 1px dashed black; background: #F8CBAD;")
                    self.button_state[order] = 2

            label_number = self.implement_combo_box.count()
            self.progress_bar.setValue(int(self.progress / label_number * 100))

    def calculate_image_ratio(self):
        panel_width = 1.0 / self.layout[1]
        panel_height = 1.0 / self.layout[0]
        panel_list = []

        for order, button in enumerate(self.new_button_list):
            if button.text() == self.implement_combo_box.currentText():
                x = order % self.layout[1] * panel_width
                y = 1.0 - (order // self.layout[1] + 1) * panel_height
                coordinate = [x, y, x + panel_width, y + panel_height]
                panel_list.append(coordinate)
        panel_array = array(panel_list)
        panel_location = [min(panel_array[:, 0]), min(panel_array[:, 1]),
                          max(panel_array[:, 2]) - min(panel_array[:, 0]),
                          max(panel_array[:, 3]) - min(panel_array[:, 1])]
        return panel_location[3] / panel_location[2] / float(self.radio_text_edit.toPlainText())

    def figure_output(self):
        manuscript_format = self.targets_combo_box.currentText()
        occupied_columns = int(self.occupied_text_edit.toPlainText())
        aspect_ratio = (1, float(self.radio_text_edit.toPlainText()))

        if manuscript_format == "Cell":
            column_format = int(self.total_column_combo_box.currentText())
        else:
            column_format = None

        self.case = Figure(manuscript_format=manuscript_format, aspect_ratio=aspect_ratio,
                           occupied_columns=occupied_columns, column_format=column_format)
        if self.history_browser.toPlainText() != "":
            self.case.set_image(image_path=self.history_browser.toPlainText(), locations=[0, 0, 1, 1])

        panel_width = 1.0 / self.layout[1]
        panel_height = 1.0 / self.layout[0]
        label_number = self.implement_combo_box.count()
        image_dict = {}

        for i in range(label_number):
            panel_list = []
            label = self.implement_combo_box.itemText(i)
            for order, button in enumerate(self.new_button_list):
                if button.text() == label and self.button_state[order] == 2:
                    x = order % self.layout[1] * panel_width
                    y = 1.0 - (order // self.layout[1] + 1) * panel_height
                    coordinate = [x, y, x + panel_width, y + panel_height]
                    panel_list.append(coordinate)
            panel_array = array(panel_list)

            if len(panel_array) > 0:
                image_dict[label] = [min(panel_array[:, 0]), min(panel_array[:, 1]),
                                     max(panel_array[:, 2]) - min(panel_array[:, 0]),
                                     max(panel_array[:, 3]) - min(panel_array[:, 1])]
        for image_label, locations in image_dict.items():
            self.case.set_image(image_path="./temp/panel_" + image_label + ".png", locations=locations)
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save file', '.')
        self.case.save_figure(save_path)

        if self.draw_number < len(self.history_text):
            self.history_text = self.history_text[:self.draw_number + 1]
            self.history_text[self.draw_number] = self.history_browser.toPlainText()
        else:
            self.history_text.append(self.history_browser.toPlainText())

        if self.draw_number < len(self.targets_text):
            self.targets_text = self.targets_text[:self.draw_number + 1]
            self.targets_text[self.draw_number] = self.targets_combo_box.currentText()
        else:
            self.targets_text.append(self.targets_combo_box.currentText())

        if self.draw_number < len(self.occupied_text):
            self.occupied_text = self.occupied_text[:self.draw_number + 1]
            self.occupied_text[self.draw_number] = self.occupied_text_edit.toPlainText()
        else:
            self.occupied_text.append(self.occupied_text_edit.toPlainText())

        if self.draw_number < len(self.ratio_text):
            self.ratio_text = self.ratio_text[:self.draw_number + 1]
            self.ratio_text[self.draw_number] = self.radio_text_edit.toPlainText()
        else:
            self.ratio_text.append(self.radio_text_edit.toPlainText())

        if self.draw_number < len(self.format_text):
            self.format_text = self.format_text[:self.draw_number + 1]
            self.format_text[self.draw_number] = self.total_column_combo_box.currentText()
        else:
            self.format_text.append(self.total_column_combo_box.currentText())

        self.draw_number += 1

    def set_undo(self):
        if self.draw_number > 1:
            self.history_browser.setText(self.history_text[self.draw_number - 2])
            self.targets_combo_box.setCurrentText(self.targets_text[self.draw_number - 2])
            self.occupied_text_edit.setText(self.occupied_text[self.draw_number - 2])
            self.radio_text_edit.setText(self.ratio_text[self.draw_number - 2])
            self.total_column_combo_box.setCurrentText(self.format_text[self.draw_number - 2])
            self.draw_number -= 1
        else:
            self.history_browser.setText("")
            self.targets_combo_box.setCurrentIndex(0)
            self.occupied_text_edit.setText("")
            self.radio_text_edit.setText("")
            self.total_column_combo_box.setCurrentIndex(0)
            self.draw_number = 0

    def set_redo(self):
        if self.draw_number < len(self.history_text):
            self.history_browser.setText(self.history_text[self.draw_number])
            self.targets_combo_box.setCurrentText(self.targets_text[self.draw_number])
            self.occupied_text_edit.setText(self.occupied_text[self.draw_number])
            self.radio_text_edit.setText(self.ratio_text[self.draw_number])
            self.total_column_combo_box.setCurrentText(self.format_text[self.draw_number])
            self.draw_number += 1
        else:
            self.history_browser.setText(self.history_text[-1])
            self.targets_combo_box.setCurrentText(self.targets_text[-1])
            self.occupied_text_edit.setText(self.occupied_text[-1])
            self.radio_text_edit.setText(self.ratio_text[-1])
            self.total_column_combo_box.setCurrentText(self.format_text[-1])


if __name__ == '__main__':
    # noinspection PyTypeChecker
    QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(argv)

    entry_window = EntryWindow()
    select_window = SelectWindow()
    statistical_window = StatisticalWindow()
    structure_window_1 = StructureImage1()
    structure_window_2 = StructureImage2()
    structure_window_3 = StructureImage3()
    structure_window_4 = StructureImage4()

    entry_window.show()

    # noinspection PyUnresolvedReferences
    entry_window.implement_combo_box.activated.connect(select_window.show)
    # noinspection PyUnresolvedReferences
    entry_window.implement_combo_box.activated.connect(entry_window.hide)

    # noinspection PyUnresolvedReferences
    select_window.pushButton.clicked.connect(structure_window_1.show)
    # noinspection PyUnresolvedReferences
    select_window.pushButton.clicked.connect(select_window.hide)
    # noinspection PyUnresolvedReferences
    select_window.pushButton_2.clicked.connect(statistical_window.show)
    # noinspection PyUnresolvedReferences
    select_window.pushButton_2.clicked.connect(select_window.hide)
    # noinspection PyUnresolvedReferences
    select_window.pushButton_3.clicked.connect(select_window.hide)
    # noinspection PyUnresolvedReferences
    select_window.pushButton_3.clicked.connect(entry_window.show)

    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_5.clicked.connect(statistical_window.hide)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_5.clicked.connect(select_window.show)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_5.clicked.connect(statistical_window.window_clear)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_6.clicked.connect(entry_window.show)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_6.clicked.connect(statistical_window.hide)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_6.clicked.connect(
        lambda: statistical_window.save_image(entry_window.implement_combo_box.currentText(),
                                              entry_window.targets_combo_box.currentText()))
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_6.clicked.connect(entry_window.image_set)
    # noinspection PyUnresolvedReferences
    statistical_window.pushButton_6.clicked.connect(statistical_window.window_clear)

    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_5.clicked.connect(structure_window_1.hide)
    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_5.clicked.connect(select_window.show)
    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_5.clicked.connect(structure_window_1.window_clear)
    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_6.clicked.connect(structure_window_2.show)
    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_6.clicked.connect(structure_window_1.hide)
    # noinspection PyUnresolvedReferences
    structure_window_1.pushButton_6.clicked.connect(structure_window_2.start_image)

    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_5.clicked.connect(structure_window_2.hide)
    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_5.clicked.connect(structure_window_1.show)
    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_5.clicked.connect(structure_window_2.window_initialization)
    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_6.clicked.connect(structure_window_3.show)
    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_6.clicked.connect(structure_window_2.hide)
    # noinspection PyUnresolvedReferences
    structure_window_2.pushButton_6.clicked.connect(structure_window_3.start_image)

    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_5.clicked.connect(structure_window_3.hide)
    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_5.clicked.connect(structure_window_2.show)
    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_5.clicked.connect(structure_window_3.window_initialization)
    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_6.clicked.connect(structure_window_4.show)
    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_6.clicked.connect(structure_window_3.hide)
    # noinspection PyUnresolvedReferences
    structure_window_3.pushButton_6.clicked.connect(structure_window_4.start_image)

    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_5.clicked.connect(structure_window_4.hide)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_5.clicked.connect(structure_window_3.show)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_5.clicked.connect(structure_window_4.window_initialization)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(entry_window.show)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(structure_window_4.hide)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(
        lambda: structure_window_4.save_image(entry_window.implement_combo_box.currentText(),
                                              entry_window.calculate_image_ratio()))
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(entry_window.image_set)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(structure_window_1.window_clear)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(structure_window_2.window_clear)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(structure_window_3.window_clear)
    # noinspection PyUnresolvedReferences
    structure_window_4.pushButton_6.clicked.connect(structure_window_4.window_clear)

    exit(app.exec_())
