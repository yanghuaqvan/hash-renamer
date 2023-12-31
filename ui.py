# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\resources\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from utils import RenameThread
from PyQt5 import QtCore, QtGui, QtWidgets


class TextLabel(QtWidgets.QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.path=None
        self.setText("把需要重命名的文件夹拖入文本框。\n")
 
    def getPath(self):
        return self.path

    def dragEnterEvent(self, e):
        self.path=e.mimeData().text().removeprefix(r'file:///')
        if not os.path.isdir(self.path):
            self.setText('文件夹路径错误，请拖入文件夹\n')
            self.path=None
        else:
            self.setText('文件路径：\n' + e.mimeData().text())
        e.accept()
 
    def dragLeaveEvent(self, e):
        if(self.path is None):
            self.setText("把需要重命名的文件夹拖入文本框。\n")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setWindowTitle("HASH RENAMER")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.textBrowser = TextLabel(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBoxItemInit()
        self.horizontalLayout.addWidget(self.comboBox)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setAccessibleName("rename")
        self.pushButton.setText("START")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start_action)

        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

    def comboBoxItemInit(self):
        methods = ['sha1', 'sha224',  'sha256',  'sha384',  'sha512',  'md5']
        self.comboBox.addItems(methods)

    def start_action(self):
        if (self.textBrowser.getPath is None):
            return
        self.renameThread = RenameThread(self.textBrowser.getPath(), method=self.comboBox.currentText()	)
        self.renameThread.processSignal.connect(self.changeProcess)
        self.renameThread.stateSignal.connect(self.changeButton)
        self.renameThread.start()
    
    def changeButton(self, state: int):
        if(state==0):
            self.pushButton.setDisabled(False)
        if(state==1):
            self.pushButton.setDisabled(True)
    
    def changeProcess(self, process: int):
        self.progressBar.setValue(process)