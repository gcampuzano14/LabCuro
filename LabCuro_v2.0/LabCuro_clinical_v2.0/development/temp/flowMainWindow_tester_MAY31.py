# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flowMainWindow.ui'
#
# Created: Sun Apr 20 00:23:42 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import os
import re
from PySide.QtGui import QTreeView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, structure):
        print structure
        self.setWindowTitle("LabCuro v3.0 Clinical Suite")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 850)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Untitled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.centralwidget.showEvent()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 22))
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
        #myTreeWidget()

        #self.eOutput.setRootIsDecorated(False)
        #self.tree = myTree(self.centralwidget)
        #self.tree.setObjectName("treeView")
        #self.tree.setGeometry(QtCore.QRect(9, 9, 1110, 650))
        #self.treeView = self.mytree.tabwidgetcreate(structure)
        
        
        self.tabwidgetcreate(structure)
        self.createbuttons()
        
    def tabwidgetcreate(self, structure):
        #create tabwidget
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(10, 10, 1000, 500))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.tab_widget.setFont(font)
        
        self.tab_widget.setMouseTracking(True)
        self.tab_widget.setToolTip("Tjis is the TB")
        self.tab_widget.setStatusTip("")
        self.tab_widget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tab_widget.setMovable(True)
        self.tab_widget.setObjectName("tabWidget")
        
        self.increase = {}
        for service in structure: 
            #create tabwidget
            self.tab_site = QtGui.QWidget(self)
            self.tab_widget.addTab(self.tab_site, str(service)) 
            
            #horizontal layout within tabwidget
            self.horizontalLayoutWidget = QtGui.QWidget(self.tab_site)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 1110, 650))
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            
            for lab in structure[service]:
                #treename = '-'.join([lab,service])
                #print 'lab'
                #path = structure[service][lab]
                #print path
                #self.treeWidget = myTree(self.horizontalLayoutWidget)
                self.treeWidget = myTree(self.horizontalLayoutWidget, lab, service)
                #self.treeWidget.setObjectName(treename)
                #self.increase[treename] = self.treeWidget
                for dirs in structure[service][lab]:
                    treename = '-'.join([lab,service])
                    #print dirs
                    path = structure[service][lab]
                    dire = dirs['path']
                    #self.treeWidget = myTree(self.horizontalLayoutWidget, structure, service, lab, self.increase, treename, dirs, dire)
                    #QtGui.QTreeWidgetItem(self.treeWidget, ["DDDD"])
                    #
                    self.treeWidget.setObjectName(treename)
                    self.increase[treename] = self.treeWidget

                    self.treeWidget.realtreee(structure, service, lab, self.increase, treename, dirs, dire)
                
                self.horizontalLayout.addWidget(self.increase[treename])
            
        #self.treeWidget.itemClicked.connect(lambda: self.cselect(self.treeWidget.currentItem(), 1))
                    
    def createbuttons(self):
        #create buttonbox layout
        #font for btns
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        
        #open btns - group1
        self.groupBox_1 = QtGui.QGroupBox(self)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 680, 241, 80))
        self.groupBox_1.setObjectName("groupBox_1")
        self.groupBox_1.setTitle('Preview')
        
        self.openbtn = QtGui.QPushButton(self.groupBox_1)
        self.openbtn.setGeometry(QtCore.QRect(26, 30, 93, 41))
        self.openbtn.setFont(font)
        self.openbtn.setObjectName("openbtn")
        self.openbtn.setText('Open')
        #action
        self.openbtn.clicked.connect(self.openfil)
        
        self.raw_openbtn = QtGui.QPushButton(self.groupBox_1)
        self.raw_openbtn.setGeometry(QtCore.QRect(130, 30, 93, 41))
        self.raw_openbtn.setFont(font)
        self.raw_openbtn.setObjectName("raw_openbtn")
        self.raw_openbtn.setText('Raw files')
        
        #remove/restore btns - group2
        self.groupBox_2 = QtGui.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(260, 680, 551, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setTitle('Signout')
        
        self.removebtn = QtGui.QPushButton(self.groupBox_2)
        self.removebtn.setGeometry(QtCore.QRect(16, 30, 91, 41))
        self.removebtn.setFont(font)
        self.removebtn.setObjectName("removebtn")
        self.removebtn.setText('Remove')
        
        self.removeallbtn = QtGui.QPushButton(self.groupBox_2)
        self.removeallbtn.setGeometry(QtCore.QRect(112, 30, 151, 41))
        self.removeallbtn.setFont(font)
        self.removeallbtn.setObjectName("removeallbtn")
        self.removeallbtn.setText('Remove previous')
                    
        self.restorebtn = QtGui.QPushButton(self.groupBox_2)
        self.restorebtn.setGeometry(QtCore.QRect(272, 30, 71, 41))
        self.restorebtn.setFont(font)
        self.restorebtn.setObjectName("restorebtn")
        self.restorebtn.setText('Restore')
        
        self.restoreallbtn = QtGui.QPushButton(self.groupBox_2)
        self.restoreallbtn.setGeometry(QtCore.QRect(350, 30, 93, 41))
        self.restoreallbtn.setFont(font)
        self.restoreallbtn.setObjectName("restoreallbtn")
        self.restoreallbtn.setText('Restore all')
    
        #Extra btns
        self.groupBox_3 = QtGui.QGroupBox(self)
        self.groupBox_3.setGeometry(QtCore.QRect(811, 680, 551, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setTitle('Extras')
        
        self.qcbtn = QtGui.QPushButton(self.groupBox_3)
        self.qcbtn.setGeometry(QtCore.QRect(830, 710, 71, 41))
        self.qcbtn.setFont(font)
        self.qcbtn.setObjectName("qcbtn")
        self.qcbtn.setText('Qc')
        
        self.refreshbtn = QtGui.QPushButton(self.groupBox_3)
        self.refreshbtn.setGeometry(QtCore.QRect(350, 30, 93, 41))
        self.refreshbtn.setFont(font)
        self.refreshbtn.setObjectName("refreshbtn")
        self.refreshbtn.setText('Refresh')
        
        self.rxhbtn = QtGui.QPushButton(self.groupBox_3)
        self.rxhbtn.setGeometry(QtCore.QRect(450, 30, 80, 41))
        self.rxhbtn.setFont(font)
        self.rxhbtn.setObjectName("rxhbtn")
        self.rxhbtn.setText('Research')
        
        self.cases_donebtn = QtGui.QPushButton(self.groupBox_3)
        self.cases_donebtn.setGeometry(QtCore.QRect(450, 30, 93, 41))
        self.cases_donebtn.setFont(font)
        self.cases_donebtn.setObjectName("donebtn")
        self.cases_donebtn.setText('Done') 
        
        
    def cselect(self, selected, o):
        print o
        w = os.path.dirname(__file__) + os.sep + 'bf3.gif'
        #print w
        #os.startfile(w)
        print selected.text(0)
        
                
    def openfil(self):
        print 'dsdsds'

class myTree(QtGui.QTreeWidget):
    def __init__(self, parent,  lab, service):
        super(myTree, self).__init__(parent)
        #self.lab = lab
        #print lab
        #self.realtreee(structure, service, lab, increase, treename, dirs, dire)
        self.itemClicked.connect(lambda: self.cselect(self.currentItem(),lab, service))
        

    def realtreee(self, structure, service, lab, increase, treename, dirs, dire):

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        header = QtGui.QTreeWidgetItem([lab])
        self.setHeaderItem(header)
        path,folder=os.path.split(dirs['path'])
        logo = QtGui.QPixmap("bf3.png")
        root = QtGui.QTreeWidgetItem(self, [folder])
        
        #root = QtGui.QTreeWidgetItem(self.increase[treename], [folder])
        #root = QtGui.QTreeWidgetItem(self.treeWidget, [folder])
        root.setIcon(0, logo)
        font.setBold(True)
        root.setFont(0,font)

        for pattern in dirs['patterns']:
            #print pattern
            casetype = QtGui.QTreeWidgetItem(root, [pattern])
            #print dirs['patterns'][pattern]
            item_cases = self.pullfiles(dirs['path'], dirs['patterns'][pattern])
            for a in item_cases:
                case_new = QtGui.QTreeWidgetItem(casetype, [a])
        self.expandAll()


    
        #self.itemClicked.connect(lambda: self.cselect(self.currentItem()))

    
    def mousePressEvent(self, mouseEvent):
        QtGui.QTreeView.mousePressEvent(self, mouseEvent)
        
                
    #def mouseReleaseEvent(self, event):
     #   print 'released'
      #  self.mousePressPos = QtCore.QPoint()
       # event.accept()     
        
    def keyPressEvent(self, qKeyEvent):
        #QtGui.QTreeView.keyPressEvent(self, qKeyEvent)
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.itemClicked.connect(lambda: self.cselect(self.currentItem()))
                        
    def cselect(self, selected, lab, service,dire):
        t = selected.text(0)
        print t, lab, service, dire
        #w = os.path.dirname(__file__) + os.sep + 'bf3.gif'
        #print w
        #os.startfile(w)
        self.clearSelection()
        self.clearFocus()
        
        return t
        
    def pullfiles(self, folder, pattern):  # called to pull file names into gui lists
        caselist = []
        for filef in os.listdir(folder):
            if re.match(pattern, filef, re.IGNORECASE):
                caselist.append(filef)    
        return caselist
    