# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flowMainWindow.ui'
#
# Created: Thu Aug 08 00:59:01 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 641)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Untitled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 821, 581))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setToolTip("")
        self.tabWidget.setStatusTip("")
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_jmh = QtGui.QWidget()
        self.tab_jmh.setObjectName("tab_jmh")
        self.tabWidget_2 = QtGui.QTabWidget(self.tab_jmh)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 20, 791, 391))
        self.tabWidget_2.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget_2.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget_2.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_jmh_patho = QtGui.QWidget()
        self.tab_jmh_patho.setObjectName("tab_jmh_patho")
        self.jmh_patho_bm_num = QtGui.QLineEdit(self.tab_jmh_patho)
        self.jmh_patho_bm_num.setGeometry(QtCore.QRect(530, 22, 51, 22))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_bm_num.setFont(font)
        self.jmh_patho_bm_num.setAlignment(QtCore.Qt.AlignCenter)
        self.jmh_patho_bm_num.setReadOnly(True)
        self.jmh_patho_bm_num.setObjectName("jmh_patho_bm_num")
        self.bm_num = QtGui.QLabel(self.tab_jmh_patho)
        self.bm_num.setGeometry(QtCore.QRect(390, 18, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.bm_num.setFont(font)
        self.bm_num.setObjectName("bm_num")
        self.jmh_patho_tissue_num = QtGui.QLineEdit(self.tab_jmh_patho)
        self.jmh_patho_tissue_num.setGeometry(QtCore.QRect(100, 22, 51, 22))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_tissue_num.setFont(font)
        self.jmh_patho_tissue_num.setAlignment(QtCore.Qt.AlignCenter)
        self.jmh_patho_tissue_num.setReadOnly(True)
        self.jmh_patho_tissue_num.setObjectName("jmh_patho_tissue_num")
        self.label_4 = QtGui.QLabel(self.tab_jmh_patho)
        self.label_4.setGeometry(QtCore.QRect(30, 18, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayoutWidget = QtGui.QWidget(self.tab_jmh_patho)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 60, 711, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.jmh_patho_tissue_list = QtGui.QListWidget(self.horizontalLayoutWidget)
        self.jmh_patho_tissue_list.setObjectName("jmh_patho_tissue_list")
        self.horizontalLayout.addWidget(self.jmh_patho_tissue_list)
        self.jmh_patho_bm_list = QtGui.QListWidget(self.horizontalLayoutWidget)
        self.jmh_patho_bm_list.setObjectName("jmh_patho_bm_list")
        self.horizontalLayout.addWidget(self.jmh_patho_bm_list)
        self.tabWidget_2.addTab(self.tab_jmh_patho, "")
        self.tab_jmh_lab = QtGui.QWidget()
        self.tab_jmh_lab.setObjectName("tab_jmh_lab")
        self.label_5 = QtGui.QLabel(self.tab_jmh_lab)
        self.label_5.setGeometry(QtCore.QRect(30, 18, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.jmh_patho_tissue_num_2 = QtGui.QLineEdit(self.tab_jmh_lab)
        self.jmh_patho_tissue_num_2.setGeometry(QtCore.QRect(100, 22, 51, 22))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_tissue_num_2.setFont(font)
        self.jmh_patho_tissue_num_2.setAlignment(QtCore.Qt.AlignCenter)
        self.jmh_patho_tissue_num_2.setReadOnly(True)
        self.jmh_patho_tissue_num_2.setObjectName("jmh_patho_tissue_num_2")
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.tab_jmh_lab)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 60, 711, 311))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.jmh_patho_tissue_list_2 = QtGui.QListWidget(self.horizontalLayoutWidget_2)
        self.jmh_patho_tissue_list_2.setObjectName("jmh_patho_tissue_list_2")
        self.horizontalLayout_2.addWidget(self.jmh_patho_tissue_list_2)
        self.tabWidget_2.addTab(self.tab_jmh_lab, "")
        self.groupBox_2 = QtGui.QGroupBox(self.tab_jmh)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 420, 141, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.jmh_patho_openbtn = QtGui.QPushButton(self.groupBox_2)
        self.jmh_patho_openbtn.setGeometry(QtCore.QRect(26, 30, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_openbtn.setFont(font)
        self.jmh_patho_openbtn.setObjectName("jmh_patho_openbtn")
        self.groupBox = QtGui.QGroupBox(self.tab_jmh)
        self.groupBox.setGeometry(QtCore.QRect(169, 420, 631, 80))
        self.groupBox.setObjectName("groupBox")
        self.jmh_patho_removebtn = QtGui.QPushButton(self.groupBox)
        self.jmh_patho_removebtn.setGeometry(QtCore.QRect(16, 30, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_removebtn.setFont(font)
        self.jmh_patho_removebtn.setObjectName("jmh_patho_removebtn")
        self.jmh_patho_openremovebtn = QtGui.QPushButton(self.groupBox)
        self.jmh_patho_openremovebtn.setGeometry(QtCore.QRect(160, 30, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_openremovebtn.setFont(font)
        self.jmh_patho_openremovebtn.setObjectName("jmh_patho_openremovebtn")
        self.jmh_patho_removeprevbtn = QtGui.QPushButton(self.groupBox)
        self.jmh_patho_removeprevbtn.setGeometry(QtCore.QRect(310, 30, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_removeprevbtn.setFont(font)
        self.jmh_patho_removeprevbtn.setObjectName("jmh_patho_removeprevbtn")
        self.jmh_patho_donebtn = QtGui.QPushButton(self.groupBox)
        self.jmh_patho_donebtn.setGeometry(QtCore.QRect(525, 30, 93, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_donebtn.setFont(font)
        self.jmh_patho_donebtn.setObjectName("jmh_patho_donebtn")
        self.qc_btn = QtGui.QPushButton(self.tab_jmh)
        self.qc_btn.setGeometry(QtCore.QRect(551, 510, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.qc_btn.setFont(font)
        self.qc_btn.setObjectName("qc_btn")
        self.jmh_patho_refresh = QtGui.QToolButton(self.tab_jmh)
        self.jmh_patho_refresh.setGeometry(QtCore.QRect(709, 510, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.jmh_patho_refresh.setFont(font)
        self.jmh_patho_refresh.setObjectName("jmh_patho_refresh")
        self.rxh_btn = QtGui.QPushButton(self.tab_jmh)
        self.rxh_btn.setGeometry(QtCore.QRect(630, 510, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.rxh_btn.setFont(font)
        self.rxh_btn.setObjectName("rxh_btn")
        self.tabWidget.addTab(self.tab_jmh, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 22))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtGui.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_server = QtGui.QAction(MainWindow)
        self.actionNew_server.setObjectName("actionNew_server")
        self.actionManual = QtGui.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")
        self.menuMain.addAction(self.actionNew_server)
        self.menuHelp.addAction(self.actionManual)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "FlowCuro v2.1", None, QtGui.QApplication.UnicodeUTF8))
        self.bm_num.setText(QtGui.QApplication.translate("MainWindow", "Bone marrow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Tissue", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_jmh_patho), QtGui.QApplication.translate("MainWindow", "Pathology Cases", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Cases", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_jmh_lab), QtGui.QApplication.translate("MainWindow", "Clinical Lab. Cases", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_openbtn.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Pathologist", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_removebtn.setText(QtGui.QApplication.translate("MainWindow", "Remove from list", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_openremovebtn.setText(QtGui.QApplication.translate("MainWindow", "Open and remove", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_removeprevbtn.setText(QtGui.QApplication.translate("MainWindow", "Remove previously opened", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_donebtn.setText(QtGui.QApplication.translate("MainWindow", "Done cases", None, QtGui.QApplication.UnicodeUTF8))
        self.qc_btn.setText(QtGui.QApplication.translate("MainWindow", "QC", None, QtGui.QApplication.UnicodeUTF8))
        self.jmh_patho_refresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.rxh_btn.setText(QtGui.QApplication.translate("MainWindow", "Research", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_jmh), QtGui.QApplication.translate("MainWindow", "Jackson Memorial Hospital", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMain.setTitle(QtGui.QApplication.translate("MainWindow", "Main", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_server.setText(QtGui.QApplication.translate("MainWindow", "New server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionManual.setText(QtGui.QApplication.translate("MainWindow", "Manual", None, QtGui.QApplication.UnicodeUTF8))
