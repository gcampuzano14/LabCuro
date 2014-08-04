# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'date_range.ui'
#
# Created: Tue Jul 22 00:06:45 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dates(object):
    def setupUi(self, dates):
        dates.setObjectName("dates")
        dates.resize(625, 273)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../src/bin/images/labcure_chromatogram.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dates.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(dates)
        self.buttonBox.setGeometry(QtCore.QRect(10, 230, 621, 41))
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.calendarWidget = QtGui.QCalendarWidget(dates)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 60, 271, 155))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget_2 = QtGui.QCalendarWidget(dates)
        self.calendarWidget_2.setGeometry(QtCore.QRect(330, 60, 271, 155))
        self.calendarWidget_2.setObjectName("calendarWidget_2")
        self.label = QtGui.QLabel(dates)
        self.label.setGeometry(QtCore.QRect(30, 20, 271, 41))
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(dates)
        self.label_2.setGeometry(QtCore.QRect(330, 20, 271, 41))
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(dates)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dates.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dates.reject)
        QtCore.QMetaObject.connectSlotsByName(dates)

    def retranslateUi(self, dates):
        dates.setWindowTitle(QtGui.QApplication.translate("dates", "LabCuro 2.0 data dump - Select date range", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dates", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Start date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dates", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">End date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

