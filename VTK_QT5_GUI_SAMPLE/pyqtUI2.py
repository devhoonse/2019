# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(618, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame.setGeometry(QtCore.QRect(10, 0, 104, 90))
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.horizontalFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalFrame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalFrame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.vtk_panel = QtWidgets.QFrame(self.centralwidget)
        self.vtk_panel.setGeometry(QtCore.QRect(230, 0, 381, 531))
        self.vtk_panel.setObjectName("vtk_panel")
        # self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.vtk_panel)
        # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(10, 100, 109, 31))
        self.radioButton.setObjectName("radioButton")
        self.opacity_slider = QtWidgets.QSlider(self.centralwidget)
        self.opacity_slider.setGeometry(QtCore.QRect(10, 160, 160, 24))
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setSingleStep(1)
        self.opacity_slider.setProperty("value", 50)
        self.opacity_slider.setOrientation(QtCore.Qt.Horizontal)
        self.opacity_slider.setObjectName("opacity_slider")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 140, 63, 20))
        self.label.setObjectName("label")
        self.shrink_slider = QtWidgets.QSlider(self.centralwidget)
        self.shrink_slider.setGeometry(QtCore.QRect(10, 230, 160, 24))
        self.shrink_slider.setMinimum(1)
        self.shrink_slider.setMaximum(100)
        self.shrink_slider.setPageStep(10)
        self.shrink_slider.setProperty("value", 50)
        self.shrink_slider.setOrientation(QtCore.Qt.Horizontal)
        self.shrink_slider.setObjectName("shrink_slider")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 210, 101, 20))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Viewer"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.radioButton.setText(_translate("MainWindow", "RadioButton"))
        self.label.setText(_translate("MainWindow", "Opacity"))
        self.label_2.setText(_translate("MainWindow", "ShrinkFactor"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
