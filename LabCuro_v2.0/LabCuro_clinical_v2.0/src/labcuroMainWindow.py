# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import time
import os
import re
import datetime
import shutil
import database_handler
import images_qr
import webbrowser



class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow, structure, username_in, poweruser, poweruser_list_in):
        global chosenfile
        global power
        global opened_cases
        global removed_cases
        global username
        global poweruser_list
        global remove_type
        power = poweruser#1haveth3p0w3r  
        poweruser_list = poweruser_list_in
        poweruser_list = [str(x) for x in poweruser_list]
        username = username_in
        opened_cases = []
        removed_cases = []
        #print structure
        #image_dir = os.path.join(os.path.dirname(__file__),'bin','images')
        self.setWindowTitle("LabCuro v2.0 Clinical Suite")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 700)
        MainWindow.setFixedSize(1020, 700)
        resolution = QtGui.QDesktopWidget().screenGeometry()
        MainWindow.move((resolution.width() / 2) - (self.frameSize().width() / 2), 
                        (resolution.height() / 2) - (self.frameSize().height() / 2))
        #MainWindow.move(100,100)
        MainWindow.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.TopDockWidgetArea)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(':/bin/images/labcuro_chromatogram.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #icon.addPixmap(QtGui.QPixmap(os.path.join(image_dir,"labcuro_chromatogram.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

#####
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 22))
        self.menubar.setObjectName("menubar")
        
        self.menuMain = QtGui.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.actionNew_server = QtGui.QAction(MainWindow)
        self.actionNew_server.setObjectName("actionNew_server")
        self.menuMain.addAction(self.actionNew_server)
        #self.menubar.addAction(self.menuMain.menuAction())
        
        self.intructions = QtGui.QAction(MainWindow)
        self.intructions.setObjectName("intructions")
        self.menuMain.addAction(self.intructions)
        self.menubar.addAction(self.menuMain.menuAction())        
        
        self.menuMain.setTitle(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_server.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.intructions.setText(QtGui.QApplication.translate("MainWindow", "Instructions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew_server.triggered.connect(self.cri)
        self.intructions.triggered.connect(self.instruct)
  
#########


        #CREATE TABWIDGET
        #self.tab_widget = QtGui.QTabWidget(self)
        self.create_tab(structure)
        self.createbuttons(structure)
        
    def instruct(self):
        new = 2 # open in a new tab, if possible
        # open a public URL, in this case, the webbrowser docs
        url = "https://github.com/gcampuzano14/LabCuro/tree/master/LabCuro_clinical/manuals/LabCuro User Manual.pdf"
        webbrowser.open(url,new=new)
        
    def cri(self):
        flags = QtGui.QMessageBox.StandardButton.Ok
        msg = """ 
                LabCuro version 2.0 - Clinical Suite
                
                Copyright (C) 2014 GERMAN CAMPUZANO-ZULUAGA 
                
                This program is free software: you can redistribute 
                it and/or modify it under the terms of the GNU 
                General Public License as published by the 
                Free Software Foundation, version 3 of the License.
                
                This is free software, and you are welcome to 
                redistribute it under certain conditions.          
                      
                This program is distributed in the hope that it will 
                be useful, but WITHOUT ANY WARRANTY; without 
                even the implied warranty of MERCHANTABILITY 
                or FITNESS FOR A PARTICULAR PURPOSE.  
                
                See the GNU General Public License for more details.
                To find a copy of the license please visit:
                http://www.gnu.org/licenses/
                
                Contact: germancz81@gmail.com
                Source: https://github.com/gcampuzano14/LabCuro
                """
        QtGui.QMessageBox.about(self, "About LabCuro Clinical Suite v2.0", msg)  
        
    def create_tab(self, structure, curr_index = 1): 
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(10, 26, 1010, 560))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)    
        self.tab_widget.setFont(font)
        #self.tab_widget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tab_widget.setMovable(True)
        self.tab_widget.setObjectName("tabWidget")
        self.tabwidgetcreate(structure)
        
    def tabwidgetcreate(self, structure):
        global chosenfile
        treedict = {}
        ## GET SERVICE (EX. FLOW, MOL, SPEC_CHEM, ECT) AND CREATE TABWIDGET
        for service in structure: 
            #create tabwidget
            self.tab_site = QtGui.QWidget(self)
            #print self.tab_site

            image_dir = os.path.join(os.path.dirname(__file__),'bin','images')
            #image_dir = os.path.join(os.path.dirname(__file__),'bin','images')
            if service == 'FLOW': 
                logo = QtGui.QPixmap(':/bin/images/flow.png')
                #logo = QtGui.QPixmap(os.path.join(image_dir,'flow.png'))
            elif service == 'MOLECULAR':
                logo = QtGui.QPixmap(':/bin/images/molec.png')
                #logo = QtGui.QPixmap(os.path.join(image_dir,'molec.png'))
            self.tab_widget.addTab(self.tab_site, logo, str(service))
            #self.tab_widget.setEnabled(curr_index)
            curr = self.tab_widget.currentIndex()
            #horizontal layout within tabwidget
            self.horizontalLayoutWidget = QtGui.QWidget(self.tab_site)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, self.tab_widget.width()-9, self.tab_widget.height()-29))
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            cnt_files = 0
            #FOR EACH LAB CREATE A TREEWIDGET
            for lab in structure[service]:
                root_path = structure[service][lab]['root_path']
                self.treeWidget = myTree(root_path)
                font = QtGui.QFont()
                font.setPointSize(15)
                font.setWeight(55)
                font.setBold(True)
                self.treeWidget.setHeaderLabel(lab)
                t = self.treeWidget.header()
                t.setFont(font)
                # FOR EACH CLINICAL FILE CATEGORY (EX. COPATH, SUNQUEST, ECT)
                folders = []
                for dirs in structure[service][lab]['path_chars']:
                    case_logo = QtGui.QPixmap(':/bin/images/cases.png')
                    #case_logo = QtGui.QPixmap(os.path.join(image_dir,'cases.png'))
                    path,folder=os.path.split(dirs['path'])
                    for f in os.listdir(dirs['path']):
                        if f.find('DONE') == -1:
                            cnt_files += 1
                    #if len(os.listdir(dirs['path'])) > 1 and folder not in folders:
                    if cnt_files > 0 and folder not in folders:
                    #if folder not in folders:
                        case_type  = QtGui.QTreeWidgetItem(self.treeWidget, [folder])
                        font.setPointSize(11)
                        font.setBold(True)
                        case_type.setFont(0, font)
                        case_type.setIcon(0, case_logo)
                        folders.append(folder)
                    #elif  len(os.listdir(dirs['path'])) > 1:
                    elif  cnt_files > 0:
                        pass 
                    patterns = []
                    # FOR EACH TYPE OF MATRIX (EX. BM, TISSUE, ECT)
                    for pattern in dirs['patterns']:
                        item_cases, case_timed = self.pullfiles(dirs['path'], dirs['patterns'][pattern])
                        case_timed = sorted(case_timed.items(), key=lambda x: x[1], reverse=True)
                        if len(item_cases) > 0:
                            if pattern not in patterns:
                                if pattern == 'BONE MARROW | PERIPHERAL BLOOD':
                                    pattern_logo = QtGui.QPixmap(':/bin/images/bm.png')
                                    #pattern_logo = QtGui.QPixmap(os.path.join(image_dir,'bm.png'))
                                if pattern == 'TISSUE | FLUIDS | OTHER':
                                    pattern_logo = QtGui.QPixmap(':/bin/images/tissue.png')
                                    #pattern_logo = QtGui.QPixmap(os.path.join(image_dir,'tissue.png'))
                                regex_type  = QtGui.QTreeWidgetItem(case_type, [pattern])
                                font.setPointSize(10)
                                font.setBold(True)
                                regex_type.setFont(0, font)
                                regex_type.setIcon(0, pattern_logo)
                                patterns.append(pattern)
                            for a in case_timed:
                                terminal_file = QtGui.QTreeWidgetItem(regex_type, [a][0])
                                font.setPointSize(10)
                                font.setBold(False)
                                terminal_file.setFont(0, font)
                                if a[1] > 1:
                                    terminal_file.setForeground(0,QtGui.QBrush(QtGui.QColor('red')))    
                                self.horizontalLayout.addWidget(self.treeWidget)
                                
                                    #elif len(os.listdir(dirs['path'])) == 0:
                            self.treeWidget.expandAll()
 
                
        
                file_access_path = os.path.join(root_path, str(folder), 'mockfile.pdf')
                        
                
                treedict[self.treeWidget] = file_access_path
            if cnt_files == 0: 

                self.label = QtGui.QLabel(self.tab_site)
                self.label.setGeometry(QtCore.QRect(10, 10, 1000, 560))
                self.label.setText("")
                self.label.setPixmap(QtGui.QPixmap(":/bin/images/freedom.png"))
                #self.label.setPixmap(QtGui.QPixmap("../src/bin/images/freedom.png"))
                self.label.setObjectName("label")
        chosenfile = treedict[self.treeWidget]
        return chosenfile
        
    def createbuttons(self, structure):
        global chosenfile
        global opened_cases
         
        #SET FONTS
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        
        #BUTTON PANEL COORDINATES
        x_one = 10
        y_one = 590
        x_two = 200
        y_two = 80

        #open btns - group1
        self.groupBox_1 = QtGui.QGroupBox(self)
        self.groupBox_1.setGeometry(QtCore.QRect(x_one, y_one, x_two, y_two))
        self.groupBox_1.setObjectName("groupBox_1")
        self.groupBox_1.setTitle('Preview')
        
        #BUTTON COORDINATES
        butt_x_one = 10
        butt_y_one = 30
        butt_x_two = 80
        butt_y_two = 40

        self.openbtn = QtGui.QPushButton(self.groupBox_1)
        self.openbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.openbtn.setFont(font)
        self.openbtn.setObjectName("openbtn")
        self.openbtn.setText('Open')
        #action
        self.openbtn.clicked.connect(self.openfil)
        
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
        
        self.raw_openbtn = QtGui.QPushButton(self.groupBox_1)
        self.raw_openbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.raw_openbtn.setFont(font)
        self.raw_openbtn.setObjectName("raw_openbtn")
        self.raw_openbtn.setText('Raw files')
        #action
        self.raw_openbtn.clicked.connect(lambda: self.openfolder(''.join(['RAW', re.match('.+\\\\PROCESSED(\\\\.+)\\\\.+\.\D{3}$', 
                                                                                     str(chosenfile), re.IGNORECASE).group(1)])))    
        
        #Slide BUTTON panel over x_______________
        x_one = x_one + x_two
        x_two = x_two + 200
        
        #remove/restore btns - group2
        self.groupBox_2 = QtGui.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(x_one, y_one, x_two, y_two))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setTitle('Signout')
        
        #BUTTON COORDINATES
        butt_x_one = 10
        butt_y_one = 30
        butt_x_two = 80
        butt_y_two = 40
        
        self.removebtn = QtGui.QPushButton(self.groupBox_2)
        self.removebtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.removebtn.setFont(font)
        self.removebtn.setObjectName("removebtn")
        self.removebtn.setText('Remove')
        if  power == '1haveth3p0w3r' or username in poweruser_list:
            self.removebtn.setDisabled(False)
        else:
            self.removebtn.setDisabled(True)
        #action        
        self.removebtn.clicked.connect(lambda: self.removefile())
        
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 120
        
        self.removeallbtn = QtGui.QPushButton(self.groupBox_2)
        self.removeallbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.removeallbtn.setFont(font)
        self.removeallbtn.setObjectName("removeallbtn")
        self.removeallbtn.setText('Remove previous')
        if  power == '1haveth3p0w3r' or username in poweruser_list:
            self.removeallbtn.setDisabled(False)
        else:
            self.removeallbtn.setDisabled(True)
            
        #action
        self.removeallbtn.clicked.connect(lambda: self.removemultifile())
        
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
                    
        self.restorebtn = QtGui.QPushButton(self.groupBox_2)
        self.restorebtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.restorebtn.setFont(font)
        self.restorebtn.setObjectName("restorebtn")
        self.restorebtn.setText('Restore')
        if  power == '1haveth3p0w3r' or username in poweruser_list:
            self.restorebtn.setDisabled(False)
        else:
            self.restorebtn.setDisabled(True)
            
        #action
        self.restorebtn.clicked.connect(lambda: self.restore())
        
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
        
        self.restoreallbtn = QtGui.QPushButton(self.groupBox_2)
        self.restoreallbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.restoreallbtn.setFont(font)
        self.restoreallbtn.setObjectName("restoreallbtn")
        self.restoreallbtn.setText('Restore all')
        if  power == '1haveth3p0w3r' or username in poweruser_list:
            self.restoreallbtn.setDisabled(False)
        else:
            self.restoreallbtn.setDisabled(True)
        #action
        self.restoreallbtn.clicked.connect(lambda: self.restoremulti())
        
        #Slide BUTTON panel over x_______________
        x_one = x_one + x_two
        x_two = 280
        
        #Extra btns
        self.groupBox_3 = QtGui.QGroupBox(self)
        if  power == '1haveth3p0w3r' or username in poweruser_list:
            self.groupBox_3.setDisabled(False)
        else:    
            self.groupBox_3.setDisabled(True)
        self.groupBox_3.setGeometry(QtCore.QRect(x_one, y_one, x_two, y_two))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setTitle('Extras')
        
        #BUTTON COORDINATES
        butt_x_one = 10
        butt_y_one = 30
        butt_x_two = 80
        butt_y_two = 40
        
        self.qcbtn = QtGui.QPushButton(self.groupBox_3)
        self.qcbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.qcbtn.setFont(font)
        self.qcbtn.setObjectName("qcbtn")
        self.qcbtn.setText('Qc')
        #action
        self.qcbtn.clicked.connect(lambda: self.openfolder(re.match('.+(\\\\PROCESSED)\\\\.+\\\\.+\.\D{3}$', 
                                                                                     str(chosenfile), re.IGNORECASE).group(1)))
        
                        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
        
        self.rxhbtn = QtGui.QPushButton(self.groupBox_3)
        self.rxhbtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.rxhbtn.setFont(font)
        self.rxhbtn.setObjectName("rxhbtn")
        self.rxhbtn.setText('Research')
        #action
        self.rxhbtn.clicked.connect(lambda: self.openfolder(re.match('.+(\\\\PROCESSED)\\\\.+\\\\.+\.\D{3}$', 
                                                                                     str(chosenfile), re.IGNORECASE).group(1)))
        
                        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
        
        self.cases_donebtn = QtGui.QPushButton(self.groupBox_3)
        self.cases_donebtn.setGeometry(QtCore.QRect(butt_x_one, butt_y_one, butt_x_two, butt_y_two))
        self.cases_donebtn.setFont(font)
        self.cases_donebtn.setObjectName("donebtn")
        self.cases_donebtn.setText('Done') 
        #action
        self.cases_donebtn.clicked.connect(lambda: self.openfolder(''.join([re.match('.+(\\\\PROCESSED\\\\.+)\\\\.+\.\D{3}$', 
                                                                                     str(chosenfile), re.IGNORECASE).group(1)])))
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
 
    def openfil(self):
        global opened_cases
        opened_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
        global remove_type
        remove_type = 'list'
        os.startfile(chosenfile)

    def openfolder(self, tail = None):
        path_raw = ''.join([re.match('(.+)\\\\PROCESSED.+$', str(chosenfile), re.IGNORECASE).group(1),'\\', tail]) 
        os.startfile(path_raw) 
    
    def removefile(self):
        global removed_cases
        global remove_type
        global selected_file
        try:
            if remove_type == 'direct':
                shutil.move(chosenfile, destin_file)
                removed_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
                file_in = chosenfile
                self.db_write(file_in, 'remove')
                t = selected_file.parent()
                t.removeChild(selected_file)
            elif remove_type == 'list':
                shutil.move(opened_cases[-1][0], opened_cases[-1][1])
                removed_cases.append(opened_cases[-1])
                file_in = opened_cases[-1][0]
                self.db_write(file_in, 'remove')
                t = opened_cases[-1][2].parent()
                t.removeChild(opened_cases[-1][2])
                opened_cases.pop()
            remove_type = 'list'
        except:
            pass
               
    def removemultifile(self):
        global removed_cases
        global opened_cases
        for e in opened_cases:
            try:
                shutil.move(e[0], e[1])
                removed_cases.append(e)
                file_in = e[0]
                self.db_write(file_in, 'remove')
                t = e[2].parent()
                t.removeChild(e[2])
            except:            
                pass
        opened_cases = []
         
    def restore(self):
        global removed_cases
        shutil.move(removed_cases[-1][1], removed_cases[-1][0])
        file_in = removed_cases[-1][0]
        self.db_write(file_in, 'restore')
        removed_cases[-1][4].insertChild(removed_cases[-1][3].row(), removed_cases[-1][2])
        removed_cases.pop()
        
    def restoremulti(self):
        global removed_cases
        for e in removed_cases:
            try:
                shutil.move(e[1], e[0])
                file_in = e[0]
                self.db_write(file_in, 'restore')
                e[4].insertChild(e[3].row(), e[2])
            except:            
                pass
        removed_cases = [] 
        
    def pullfiles(self, folder, pattern):  # called to pull file names into gui lists
        caselist = []
        case_timed = {}
        for filef in os.listdir(folder):
            if re.match(pattern, filef, re.IGNORECASE):
                caselist.append(filef)
                item = os.path.join(folder, filef)
                timestamp = (((os.stat(item).st_mtime)/60)/60)/24
                now_number = ((time.time()/60)/60)/24
                timestamp  = now_number - timestamp 
                case_timed[filef] = timestamp     
        return caselist, case_timed

    def db_write(self, file_in, input_type):
        
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        drive_letter = re.match('(^\w)', file_in).group(1) + ':'
        db_clin = os.path.join(drive_letter,'\\TECHNICAL\\clinical_cases.db')
        cases_id_rx = re.match('.+\\\\(.+?)\s(.+?)\s(.+?)\s(.+?)\s.+\.\D{3}$', file_in)
        access_num = cases_id_rx.group(1)
        pte_name = cases_id_rx.group(2)
        matrix = cases_id_rx.group(3) 
        panel = cases_id_rx.group(4)
        #print access_num, pte_name, matrix, panel, now_str
        
        if input_type == 'restore':
            #print 'restore'
            insert_vals = '''UPDATE case_log SET training_pathologist = ?, pathologist = ?, 
                                date_reviewed_pathologist = ? WHERE accession_number = ? and patient_name = ? and matrix = ? and panel = ?'''
            dicts = (str(username), str(username), None, str(access_num), str(pte_name), str(matrix), str(panel))
        
        elif input_type == 'remove':
            #print 'remove'
            insert_vals = '''UPDATE case_log SET training_pathologist = ?, pathologist = ?, 
                                date_reviewed_pathologist = ? WHERE accession_number = ? and patient_name = ? and matrix = ? and panel = ?'''
            dicts = (str(username), str(username), str(now_str), str(access_num), str(pte_name), str(matrix), str(panel)) 
        
        #print 'calling db'
        #print db_clin
        database_handler.insert_data(insert_vals, dicts, db_clin)

class myTree(QtGui.QTreeWidget):
    def __init__(self, root_path):
        super(myTree, self).__init__()
        self.update()
        
        #self.itemDoubleClicked.connect(lambda: self.cselect(self.currentItem(), root_path))
        #self.currentItemChanged(lambda: self.get_path(self.currentItem(), self.currentIndex(), root_path))
        self.itemDoubleClicked.connect(lambda: self.cselect(root_path))
        self.itemClicked.connect(lambda: self.get_path(self.currentItem(), self.currentIndex(), root_path))

    def get_path(self, selected_item, sel_index, root_path):
        global opened_cases
        global selected_index
        global selected_file
        global chosenfile
        global destin_file
        global remove_type
        global reuse_root
        reuse_root = root_path
        remove_type = 'direct'
        selected_file = selected_item
        selected_index = sel_index
        parent = selected_item.parent()
        parent_parent = parent.parent()
        parent_text = parent_parent.text(0)
        file_text = selected_item.text(0)
        destin_file = os.path.join(root_path, parent_text, 'DONE_' + file_text)
        chosenfile = os.path.join(root_path, parent_text,file_text)

    def mousePressEvent(self, mouseEvent):
        QtGui.QTreeView.mousePressEvent(self, mouseEvent)    

    def keyPressEvent(self, qKeyEvent):
        global remove_type
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            global opened_cases
            opened_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
            remove_type = 'list'
            #opened_cases[chosenfile] = selected_file
            os.startfile(chosenfile) 
        
        if qKeyEvent.key() == QtCore.Qt.Key_Delete:
            global removed_file
            global removed_cases
            if  power == '1haveth3p0w3r' or username in poweruser_list:

                try:
                    shutil.move(chosenfile, destin_file)
                    removed_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
                    file_in = chosenfile
                    g = Ui_MainWindow()
                    g.db_write(file_in, 'remove')
                    t = selected_file.parent()
                    t.removeChild(selected_file)
                except:
                    pass
            else:
                pass
        elif ((qKeyEvent.key() == QtCore.Qt.Key_Up) or (qKeyEvent.key() == QtCore.Qt.Key_Down) 
              or (qKeyEvent.key() == QtCore.Qt.Key_Right) or (qKeyEvent.key() == QtCore.Qt.Key_Left)):
            QtGui.QTreeView.keyPressEvent(self,qKeyEvent)
            self.get_path(self.currentItem(), self.currentIndex(), reuse_root)
            
    #def cselect(self, selected_item, root_path):
    def cselect(self, root_path):
        global opened_cases

        global remove_type
        
        #parent = selected_item.parent()
        parent = selected_file.parent()
        parent_parent = parent.parent()
        parent_text = parent_parent.text(0)
        #file_text = selected_item.text(0)
        file_text = selected_file.text(0)
        full_path = os.path.join(root_path, parent_text, file_text)
        opened_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
        remove_type = 'list'
        os.startfile(full_path)
        return full_path 
