# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import time
import os
import re
import datetime
import shutil
import database_handler


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow, structure, db_clin_list_in, username_in, poweruser):
        global power
        global opened_cases
        global removed_cases
        global username
        global db_clin_list
        global remove_type
        
        power = poweruser#1haveth3p0w3r  
        db_clin_list = db_clin_list_in
        username = username_in
        
        opened_cases = []
        #opened_cases = {}
        #removed_cases = {}
        removed_cases = []
        
        print structure
        print db_clin_list
        
        self.setWindowTitle("LabCuro Clinical Suite")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 700)
        MainWindow.setFixedSize(1020, 700)
        MainWindow.move(10,10)
        MainWindow.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.TopDockWidgetArea)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Untitled.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        #CREATE TABWIDGET
        #self.tab_widget = QtGui.QTabWidget(self)
        self.create_tab(structure)
        self.createbuttons(structure)

    def create_tab(self, structure, curr_index = 1): 
        self.tab_widget = QtGui.QTabWidget(self)
        self.tab_widget.setGeometry(QtCore.QRect(10, 10, 1000, 560))
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
        #print 'in'
        #GET SERVICE (EX. FLOW, MOL, SPEC_CHEM, ECT) AND CREATE TABWIDGET
        for service in structure: 
            #print service
            #create tabwidget
            self.tab_site = QtGui.QWidget(self)
            logo = QtGui.QPixmap("bf3.png")
            
            #image = QtGui.QPixmap("fr.jpg")
            #lbl = QtGui.QLabel(self)
            #lbl.setPixmap(image)
            
            self.tab_widget.addTab(self.tab_site, logo, str(service))

            #self.tab_widget.setEnabled(curr_index)
            curr = self.tab_widget.currentIndex()
            #horizontal layout within tabwidget
            self.horizontalLayoutWidget = QtGui.QWidget(self.tab_site)
            #self.horizontalLayoutWidget.setGraphicsEffect(self.shadow)
            self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, self.tab_widget.width()-9, self.tab_widget.height()-29))
            self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
            self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            
            #FOR EACH LAB CREATE A TREEWIDGET
            for lab in structure[service]:
                root_path = structure[service][lab]['root_path']
                self.treeWidget = myTree(root_path)
                font = QtGui.QFont()
                font.setPointSize(15)
                font.setWeight(50)
                font.setBold(True)
                self.treeWidget.setHeaderLabel(lab)
                t = self.treeWidget.header()
                t.setFont(font)
                
                # FOR EACH CLINICAL FILE CATEGORY (EX. COPATH, SUNQUEST, ECT)
                folders = []
                for dirs in structure[service][lab]['path_chars']:
                    case_logo = QtGui.QPixmap("bf3.png")
                    
                    path,folder=os.path.split(dirs['path'])
                    
                    if len(os.listdir(dirs['path'])) > 1 and folder not in folders:
                        #r = self.treeWidget.currentItem()
                        #print self.text(0)
                        
                        case_type  = QtGui.QTreeWidgetItem(self.treeWidget, [folder])
                        print case_type.text(0)
                        case_type.setIcon(0, case_logo)
                        folders.append(folder)
                    
                    elif  len(os.listdir(dirs['path'])) > 1:
                        pass 
                    patterns = []
                    for pattern in dirs['patterns']:
                        item_cases, case_timed = self.pullfiles(dirs['path'], dirs['patterns'][pattern])
                        case_timed = sorted(case_timed.items(), key=lambda x: x[1], reverse=True)
                        print case_timed
                        if len(item_cases) > 0:
                            if pattern not in patterns:
                                regex_type  = QtGui.QTreeWidgetItem(case_type, [pattern])
                                patterns.append(pattern)
                            for a in case_timed:
                                terminal_file = QtGui.QTreeWidgetItem(regex_type, [a][0])
                                if a[1] > 1:
                                    terminal_file.setForeground(0,QtGui.QBrush(QtGui.QColor('red')))    
                                self.horizontalLayout.addWidget(self.treeWidget)
                        #else: 
                            #image = QtGui.QPixmap("fr.jpg")
                            #plt = QtGui.QPalette(self)
                            #plt.setColor(QtGui.QColor(1))
                            #lbl = QtGui.QLabel(self)
                            #lbl.setPixmap(image)
                            #self.tab_site.setPalette(plt)
                                #self.tab_widget.setTabEnabled(curr, False)   
                #print property(self.treeWidget)
                self.treeWidget.expandAll()
             
    def createbuttons(self, structure):
        global opened_cases
        #SET FONTS
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        
        #BUTTON PANEL COORDINATES
        x_one = 10
        y_one = 580
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
        if  power != '1haveth3p0w3r':
            self.raw_openbtn.setDisabled(True)
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
        #action
        self.restoreallbtn.clicked.connect(lambda: self.restoremulti())
        
        #Slide BUTTON panel over x_______________
        x_one = x_one + x_two
        x_two = 280
        
        #Extra btns
        self.groupBox_3 = QtGui.QGroupBox(self)
        if  power != '1haveth3p0w3r':
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
                                                                                     str(chosenfile), re.IGNORECASE).group(1),'\\DONE'])))
        #slide to next button over x
        butt_x_one = butt_x_one + butt_x_two + 5
        butt_x_two = 80
 
    def openfil(self):
        global opened_cases
        opened_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
        print opened_cases
        global remove_type
        remove_type = 'list'
        #opened_cases[chosenfile] = selected_file
        #os.startfile(chosenfile)

    def openfolder(self, tail):
        path_raw = ''.join([re.match('(.+)\\\\PROCESSED.+$', str(chosenfile), re.IGNORECASE).group(1),'\\', tail]) 
        #os.startfile(path_raw) 
        print opened_cases
        print removed_cases
    
    def removefile(self):
        global removed_cases
        global db_clin_list
        global remove_type
        
        try:
            print 'yes'
            if remove_type == 'direct':
                print 'dir'
                print chosenfile, destin_file
                shutil.move(chosenfile, destin_file)
                removed_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
                #removed_cases.append([chosenfile, destin_file, selected_file.parent(), selected_file, selected_index.row()])
                print 'dir'
                file_in = chosenfile
                self.db_write(file_in)
                t = selected_file.parent()
                t.removeChild(selected_file)
            elif remove_type == 'list':
                print 'list'
                print opened_cases[-1][0], opened_cases[-1][1]
                shutil.move(opened_cases[-1][0], opened_cases[-1][1])
                removed_cases.append(opened_cases[-1])
                #removed_cases.append([opened_cases[-1][0],opened_cases[-1][1], opened_cases[-1][2].parent(), opened_cases[-1][2], opened_cases[-1][2].row()])
                file_in = opened_cases[-1][0]
                #chosenfile = opened_cases[-1][1]
                self.db_write(file_in)
                print opened_cases[-1]
                t = opened_cases[-1][2].parent()
                t.removeChild(opened_cases[-1][2])
                opened_cases.pop()
            
            #removed_cases[chosenfile] = [destin_file, selected_file.parent(), selected_file, selected_index.row()]
            
            #removed_file = [chosenfile, destin_file, selected_file.parent(), selected_file, selected_index.row()]

            remove_type = 'list'
        except:
            pass
               
    def removemultifile(self):
        global removed_cases
        global opened_cases
        
        print opened_cases
        #removed_file = [chosenfile, destin_file, selected_file.parent(), selected_file, selected_index.row()]
        for e in opened_cases:
            try:
                print e[2]
                shutil.move(e[0], e[1])
                removed_cases.append(e)
                #removed_cases[e] = [destin_file, selected_file.parent(), selected_file, selected_index.row()]
                file_in = e[0]
                self.db_write(file_in)

                t = e[2].parent()
                t.removeChild(e[2])

                #t = opened_cases[e].parent()
                #t.removeChild(opened_cases[e]) 
            except:            
                pass
        print removed_cases
        opened_cases = []
         
    def restore(self):
        
        global removed_cases
        print removed_cases
        print removed_cases[-1][2].parent()
        print removed_cases[-1][4]
        shutil.move(removed_cases[-1][1], removed_cases[-1][0])
        print removed_cases[-1][3].row()
        #t = removed_cases[-1][2].parent()
        removed_cases[-1][4].insertChild(removed_cases[-1][3].row(), removed_cases[-1][2])
        #insertChild(removed_cases[-1][3].row(), removed_cases[-1][2])
        #removed_cases[-1][2].insertChild(removed_cases[-1][3].row(), removed_cases[-1][2].parent())
        #print removed_cases
        removed_cases.pop()
        #print removed_cases
        #removed_file[2].insertChild(removed_file[4], removed_file[3])
        #delete from removed cases dictionary
        #del removed_cases[chosenfile]
        
    def restoremulti(self):
        global removed_cases
        for e in removed_cases:
            try:
                shutil.move(e[1], e[0])
                e[4].insertChild(e[3].row(), e[2])
                #removed_cases[e][1].insertChild(removed_cases[e][3], removed_cases[e][2])  
            except:            
                pass
        #removed_cases = {}
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
        print case_timed       
        return caselist, case_timed

    def db_write(self, file_in):
        
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        drive_letter = re.match('(^\w)', file_in).group(1) + ':'
        db_clin = os.path.join(drive_letter,'\\TECHNICAL\\clinical_cases.db')
        cases_id_rx = re.match('.+\\\\(.+?)\s(.+?)\s(.+?)\s(.+_).+\.\D{3}$', file_in)
        access_num = cases_id_rx.group(1)
        pte_name = cases_id_rx.group(2)
        matrix = cases_id_rx.group(3) 
        panel= cases_id_rx.group(4)
        
        #if input_type == 'remove':
        #elif input_type == 'restore':

        print  access_num, pte_name, matrix, panel
        insert_vals = '''UPDATE case_log SET training_pathologist = ?, pathologist = ?, 
                            date_reviewed_pathologist = ? WHERE accession_number = ? and patient_name = ? and matrix = ? and panel = ?'''
        dicts = (str(username), str(username), str(now_str), str(access_num), str(pte_name), str(matrix), str(panel))
        database_handler.insert_data(insert_vals, dicts, db_clin)

class myTree(QtGui.QTreeWidget):
    def __init__(self, root_path):
        super(myTree, self).__init__()
        self.update()
        self.itemDoubleClicked.connect(lambda: self.cselect(self.currentItem(), root_path))
        self.itemClicked.connect(lambda: self.get_path(self.currentItem(), self.currentIndex(), root_path))

    def get_path(self, selected, sel_index, root_path):
        global opened_cases
        global selected_index
        global selected_file
        global chosenfile
        global destin_file
        global remove_type
        remove_type = 'direct'
        selected_file = selected
        selected_index = sel_index

        parent = selected.parent()
        
        parent_parent = parent.parent()
        parent_text = parent_parent.text(0)
        file_text = selected.text(0)
        destin_file = os.path.join(root_path, parent_text, 'DONE', file_text)
        #print destin_file
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
            #os.startfile(chosenfile) 
        
        if qKeyEvent.key() == QtCore.Qt.Key_Delete:
            global removed_file
            global removed_cases
            
            try:
                shutil.move(chosenfile, destin_file) 
                removed_cases[chosenfile] = [destin_file, selected_file.parent(), selected_file, selected_index.row()]
                #.append([chosenfile, destin_file, selected_file, selected_index
                #removed_file = [chosenfile, destin_file, selected_file.parent(), selected_file, selected_index.row()]
                t = selected_file.parent()
                t.removeChild(selected_file)  
            except:
                pass 
        if qKeyEvent.key() == QtCore.Qt.Key_Up:
            self.setCurrentIndex(self.indexAbove((selected_index)))
            self.get_path(self.currentItem(), self.currentIndex(), root_path)
            
            
    def cselect(self, selected_item, root_path):
        global opened_cases
        parent = selected_item.parent()
        parent_parent = parent.parent()
        parent_text = parent_parent.text(0)
        file_text = selected_item.text(0)
        full_path = os.path.join(root_path, parent_text, file_text)
        opened_cases.append([chosenfile, destin_file, selected_file, selected_index, selected_file.parent()])
        #opened_cases[chosenfile] = selected_file
        global remove_type
        remove_type = 'list'
        
        #os.startfile(full_path)
        return full_path 
