# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startupGui.ui'
#
# Created: Tue Aug 06 10:27:49 2013
#      by: pyside-uic 0.2.7 running on PySide 1.0.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_start(object):
    def setupUi(self, Dialog_start):
        Dialog_start.setObjectName("Dialog_start")
        Dialog_start.resize(677, 326)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Untitled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_start.setWindowIcon(icon)
        self.frame = QtGui.QFrame(Dialog_start)
        self.frame.setGeometry(QtCore.QRect(10, 10, 301, 301))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.start_kill = QtGui.QPushButton(self.frame)
        self.start_kill.setGeometry(QtCore.QRect(170, 240, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_kill.setFont(font)
        self.start_kill.setObjectName("start_kill")
        self.start_ok = QtGui.QPushButton(self.frame)
        self.start_ok.setGeometry(QtCore.QRect(70, 240, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_ok.setFont(font)
        self.start_ok.setObjectName("start_ok")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.password = QtGui.QLineEdit(self.frame)
        self.password.setGeometry(QtCore.QRect(110, 110, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password.setFont(font)
        self.password.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.password.setText("")
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 190, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.domain = QtGui.QLineEdit(self.frame)
        self.domain.setGeometry(QtCore.QRect(110, 180, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.domain.setFont(font)
        self.domain.setObjectName("domain")
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.username = QtGui.QLineEdit(self.frame)
        self.username.setGeometry(QtCore.QRect(110, 40, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username.setFont(font)
        self.username.setText("")
        self.username.setObjectName("username")
        self.frame_2 = QtGui.QFrame(Dialog_start)
        self.frame_2.setGeometry(QtCore.QRect(320, 10, 341, 301))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.netdrives = QtGui.QListWidget(self.frame_2)
        self.netdrives.setGeometry(QtCore.QRect(20, 40, 301, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.netdrives.setFont(font)
        self.netdrives.setObjectName("netdrives")
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog_start)
        QtCore.QMetaObject.connectSlotsByName(Dialog_start)
        Dialog_start.setTabOrder(self.username, self.password)
        Dialog_start.setTabOrder(self.password, self.domain)
        Dialog_start.setTabOrder(self.domain, self.netdrives)
        Dialog_start.setTabOrder(self.netdrives, self.start_ok)
        Dialog_start.setTabOrder(self.start_ok, self.start_kill)

    def retranslateUi(self, Dialog_start):
        Dialog_start.setWindowTitle(QtGui.QApplication.translate("Dialog_start", "FlowCuro v 2.1", None, QtGui.QApplication.UnicodeUTF8))
        self.start_kill.setText(QtGui.QApplication.translate("Dialog_start", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.start_ok.setText(QtGui.QApplication.translate("Dialog_start", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog_start", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_start", "Domain", None, QtGui.QApplication.UnicodeUTF8))
        self.domain.setText(QtGui.QApplication.translate("Dialog_start", "MEDICAL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog_start", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog_start", "Available network drives", None, QtGui.QApplication.UnicodeUTF8))
