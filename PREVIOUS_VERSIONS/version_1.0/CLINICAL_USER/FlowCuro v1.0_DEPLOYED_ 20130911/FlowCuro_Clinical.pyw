#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         FlowIt Clinical v2.1
# Created:      September 9  2013
# Version:      Version: 2.1
# Copyright:    (c) German Campuzano Zuluaga gcampuzanozuluaga@med.miami.edu 2013
#-------------------------------------------------------------------------------
import os
import time
import shutil
import re
import sys
from PySide.QtCore import *
from PySide import *
from PySide.QtGui import *
import flowMainWindow
import startupGui
import win32api
from contextlib import contextmanager
import subprocess

# interpret QT GUI into PYHTON CODE: C:\Python27\Scripts\pyside-uic.exe flowMainWindow.ui -o flowMainWindow.py
# compile executable: python -O C:\Users\germancz\Dropbox\Programming\Python\pyinstaller\pyinstaller.py --onefile --noconsole main.pyw

class StartupGui(QDialog, startupGui.Ui_Dialog_start):

    def __init__(self, parent=None):
        super(StartupGui, self).__init__(parent)
        self.setupUi(self)
        self.netdrives.addItem(str("\\\\jhscel01.um-jmh.org\JMH_Flow_Cytometry"))
        self.connect(self.start_ok, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.start_kill.clicked.connect(self.end_all)

    def end_all(self):
        self.close()  

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.accept()

class MainWindow(QMainWindow, flowMainWindow.Ui_MainWindow, StartupGui):

    global now
    global nowtime
    


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.startdialog()

    def startdialog(self):
        t = StartupGui(self)
        if t.exec_():
            username = str(t.username.text())
            password = str(t.password.text())
            domain_name = str(t.domain.text())
            # share = str(t.netdrives.currentItem().text())
            share = "\\\\jhscel01.um-jmh.org\JMH_Flow_Cytometry"
            # share="\\\\Perforin\i\GERMAN\FlowIt test directory\JTEST_R"
            # share="\\\\Perforin\i"

        self.network_share_auth(username, password, domain_name, share)

    def network_share_auth(self, username, password, domain_name, share):
        
        global drive

        localtest = 0
        if localtest != 1:
            # with network_share_auth(r"\\Perforin\i",domain_name, username, password):
            # username="gcz"
            # password="gcz"    
            # domain_name="GERMANCZ"
            
            letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            driveletter = []
            
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for e in drives:
                drive = e[0]
                driveletter.append(e[0])

            availletter = list(set(letters) - set(driveletter))
    
            """Context manager that mounts the given share using the given
            username and password to the given drive letter when entering
            the context and unmounts it when exiting."""
            
            cmd_parts = ["NET USE %s: %s" % (availletter[0], share)]  # uses first letter available to map drive
            cmd_parts.append(password)
            cmd_parts.append("/USER:%s\%s" % (domain_name, username))
            # print cmd_parts
            # print " ".join(cmd_parts)
            t = subprocess.call(" ".join(cmd_parts))  # t = 0 is successful connection
            # print " ".join(cmd_parts)
            # print t
            # print username,password,domain_name,share
        else: 
            drive = "C"
            t = 0
            
        if t == 0:
            drive = availletter[0]
            self.drives(drive, username)
        # os.system(r"NET USE %s: /DELETE" % availletter[0])
        # os.system(" ".join(cmd_parts)) 
        else:
            flags = QtGui.QMessageBox.StandardButton.Ok
            msg = "Wrong input. Check password and/or username"
            QtGui.QMessageBox.warning(self, "Warning!", msg, flags)  
            self.startdialog()
              

    def drives(self, drive, username):
        global jpth_tech
        global txt
        global jpth_cln_cpath
        global jpth_cln_sq 
        global jpth_cln_rsch 
        global jpth_cln_qc 
        global jpth_cln_cpathdone 
        global jpth_cln_sqdone
        global jpth_cln_rschdone 
        global jpth_cln_qcdone 
        global case_log
        global tissue_case
        global bm_case
        global sq_case
        global qcf_case
        global rxh_case      
        global openedfiles
        global copathcase 
        global sqcase
        global copthpatt
        global sunqpatt

        openedfiles = []

        totest = 0
        if totest == 1:
            j = "/GERMAN/FlowIt test directory/JTEST_RW/J"
        elif totest == 2:
            j = "/J"
            drive = "C"
        else:
            j = ""
        
        nowyr = time.ctime()[-4:]  # current year
        jpth_tech = drive + ":" + j + "/TECHNICAL/CASE_LOG/"  # log file directory
        case_log_patho = jpth_tech + "/CLINICAL_CASE_LOG_" + nowyr + ".txt"  # create text file with CASELOG 
        self.check_case_log(case_log_patho)
         
        # Variables for paths on J: drive clinical
        jpth_cln_cpath = drive + ":" + j + "/CLINICAL_FLOW/COPATH"
        jpth_cln_sq = drive + ":" + j + "/CLINICAL_FLOW/SUNQUEST"
        jpth_cln_rsch = drive + ":" + j + "/CLINICAL_FLOW/RESEARCH"
        jpth_cln_qc = drive + ":" + j + "/CLINICAL_FLOW/QC"
        jpth_cln_cpathdone = drive + ":" + j + "/CLINICAL_FLOW/COPATH/DONE"
        jpth_cln_sqdone = drive + ":" + j + "/CLINICAL_FLOW/SUNQUEST/DONE"
        jpth_cln_rschdone = drive + ":" + j + "/CLINICAL_FLOW/RESEARCH/DONE"
        jpth_cln_qcdone = drive + ":" + j + "/CLINICAL_FLOW/QC/DONE"
        
        arr = [jpth_cln_cpath, jpth_cln_sq, jpth_cln_rsch, jpth_cln_qc, jpth_cln_cpathdone , jpth_cln_sqdone, jpth_tech]
        for e in arr:
            try: 
                if not os.path.exists(e):  # check if path for log file exists, else create it
                    os.makedirs(e)
            except:
                break

        # regex type of case
# rsrchpatt = re.compile("(.*RXH.*).pdf") #REGEX RESEARCH cases
# qcpatt =    re.compile("(.*QCF.*).pdf") #REGEX QC cases
# copthpatt = re.compile("(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s+(\w+\d*)\s+\d+(?=.pdf)") #REGEX COPATH cases
# sunqpatt =  re.compile("([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s(\w+\d*)\s+?\d+(?=.pdf)") #REGEX SUNQUEST cases
        
        
        tissue_case = re.compile("(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:TS)|(?:FL))\s+(\w+\d*)\s+\d+(?=.pdf)")  # r".*\s{1}((TS)|(FL)){1}\s{1}.*.pdf"
        bm_case = re.compile("(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB))\s+(\w+\d*)\s+\d+(?=.pdf)")  # r".*\s{1}((BM)|(PB)){1}\s{1}.*.pdf"
        sq_case = re.compile("([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s(\w+\d*)\s+?\d+(?=.pdf)")
        
        qcf_case = re.compile(".*(QCF).*.pdf")
        rxh_case = re.compile(".*(RXH).*.pdf")
        
        copathcase = re.compile(".*COPATH.*.pdf")
        sqcase = re.compile(".*SUNQUEST.*.pdf")
        
        copthpatt = re.compile("(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s+(\w+\d*)\s+\d+(?=.pdf)")  # REGEX COPATH cases
        sunqpatt = re.compile("([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s(\w+\d*)\s+?\d+(?=.pdf)")  # REGEX SUNQUEST cases
        
        ts, bm, sq = self.pullfiles(tissue_case, bm_case, sq_case, jpth_cln_cpath, jpth_cln_sq)

        for e in ts:  # populate JMH_TS list
            self.jmh_patho_tissue_list.addItem(str(e))
        
        for e in bm:  # populate JMH_BM list
            self.jmh_patho_bm_list.addItem(str(e))
            
        for e in sq:  # populate JMH_SUNQUEST case list
            self.jmh_patho_tissue_list_2.addItem(str(e))

        # SIGNALS: list item selection
        self.jmh_patho_tissue_list.itemClicked.connect(lambda: self.cselect(jpth_cln_cpath, self.jmh_patho_tissue_list))
        self.jmh_patho_bm_list.itemClicked.connect(lambda: self.cselect(jpth_cln_cpath, self.jmh_patho_bm_list))
        self.jmh_patho_tissue_list_2.itemClicked.connect(lambda: self.cselect(jpth_cln_sq, self.jmh_patho_tissue_list_2))
        
        # SIGNALS: open file
        self.jmh_patho_openbtn.clicked.connect(self.openfil)
        self.jmh_patho_tissue_list.itemDoubleClicked.connect(self.openfil)
        self.jmh_patho_bm_list.itemDoubleClicked.connect(self.openfil)
        self.jmh_patho_tissue_list_2.itemDoubleClicked.connect(self.openfil)
        
        # SIGNALS: removefiles and create logs        
        self.jmh_patho_removebtn.clicked.connect(lambda: self.removefile(chosenfile, copathcase, sqcase, singlefile,
                                                                         jpth_cln_cpathdone, jpth_cln_sqdone, case_log_patho, username))
        self.jmh_patho_openremovebtn.clicked.connect(lambda: self.openmove(copathcase, sqcase, chosenfile, singlefile,
                                                                           jpth_cln_cpathdone, jpth_cln_sqdone, case_log_patho,
                                                                           username))    
        self.jmh_patho_removeprevbtn.clicked.connect(lambda: self.removeprev(copthpatt, sunqpatt,
                                                                             jpth_cln_cpathdone, jpth_cln_sqdone,
                                                                             jpth_cln_cpath, jpth_cln_sq, case_log_patho, username))

        # SIGNALS: open folders and refresh
        self.jmh_patho_donebtn.clicked.connect(lambda: self.donecases(jpth_cln_cpathdone, jpth_cln_sqdone))
        self.qc_btn.clicked.connect(lambda: self.qccases(jpth_cln_qc))
        self.rxh_btn.clicked.connect(lambda: self.rxhcases(jpth_cln_rsch))
        self.jmh_patho_refresh.clicked.connect(self.refreshall)
    
    def check_case_log(self, case_log_patho):
        try:  # allows read only access users to use the drive while allowing read/write users to modify directories and files
            os.open(case_log_patho, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
            with open(case_log_patho, "r+") as log:  # open file name of case log as object "log", read
                logtext = log.read()  # read "log" and assign text to string variable "logtext"
                isnewlog = logtext.rfind("FILE_NAME,CASE_ID,CASE_NAME,SAMPLE_MATRIX,PANEL,DATE,HOUR,PATHOLOGIST")

            if isnewlog == -1:
                with open(case_log_patho, "a") as log:
                    log.write("FILE_NAME,CASE_ID,CASE_NAME,SAMPLE_MATRIX,PANEL,DATE,HOUR,PATHOLOGIST\n")
                    log.close   
        except:  # pass if above fails due to read only access
            pass

    def cselect(self, direct, selected):
        global chosenfile
        global singlefile      
        chosenfile = direct + "/" + selected.currentItem().text()
        singlefile = selected.currentItem().text()
        selected.setFocus()

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.openfil()

    def openfil(self):
        global openedfiles
        global chosenfile
        ofi = chosenfile
        os.startfile(ofi)
        if singlefile not in openedfiles:
            openedfiles.append(singlefile)
        # print str(openedfiles)
        
    def removefile(self, chosenfile, copathcase, sqcase, singlefile, jpth_cln_cpathdone, jpth_cln_sqdone, case_log_patho, username):
        
        if copathcase.match(chosenfile):
            file_name = copthpatt.match(singlefile)
            casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
            destin_file = jpth_cln_cpathdone + "/" + singlefile
            
        if sqcase.match(chosenfile):
            file_name = sunqpatt.match(singlefile)
            casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
            destin_file = jpth_cln_sqdone + "/" + singlefile

        try:
            shutil.move(chosenfile, destin_file)       
            self.refreshall()
            
            if singlefile in openedfiles:
                openedfiles.remove(singlefile)
                
   
            self.logcase(singlefile, case_log_patho, casenum, casename, matrix, typeflow, username)
        except:
            pass

    def openmove(self, copathcase, sqcase, chosenfile, singlefile, jpth_cln_cpathdone, jpth_cln_sqdone, case_log_patho, username):
        
        if copathcase.match(chosenfile):
            file_name = copthpatt.match(singlefile)
            casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
            destin_file = jpth_cln_cpathdone + "/" + singlefile
            
        if sqcase.match(chosenfile):
            file_name = sunqpatt.match(singlefile)
            casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
            destin_file = jpth_cln_sqdone + "/" + singlefile
        try: 
            shutil.move(chosenfile, destin_file)
            if singlefile in openedfiles:
                openedfiles.remove(singlefile)
            self.logcase(singlefile, case_log_patho, casenum, casename, matrix, typeflow, username)
            os.startfile(destin_file)
            self.refreshall()
        except:
            pass

    def removeprev(self, copthpatt, sunqpatt, jpth_cln_cpathdone, jpth_cln_sqdone, jpth_cln_cpath, jpth_cln_sq, case_log_patho, username):
        
        global openedfiles
        for e in openedfiles:
            if copthpatt.match(e):
                file_name = copthpatt.match(e)
                casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
                origin_file = jpth_cln_cpath + "/" + e
                destin_file = jpth_cln_cpathdone + "/" + e
            if sunqpatt.match(e):
                file_name = sunqpatt.match(e)
                casenum, casename, matrix, typeflow = file_name.group(1), file_name.group(2), file_name.group(3), file_name.group(4) 
                origin_file = jpth_cln_sq + "/" + e
                destin_file = jpth_cln_sqdone + "/" + e
            try:    
                shutil.move(origin_file, destin_file)  
                self.logcase(e, case_log_patho, casenum, casename, matrix, typeflow, username)     
            except:
                break
        self.refreshall()
        openedfiles = []

    def refreshall(self):
        ts, bm, sq = self.pullfiles(tissue_case, bm_case, sq_case, jpth_cln_cpath, jpth_cln_sq)
        self.jmh_patho_tissue_list.clear()
        self.jmh_patho_bm_list.clear()
        self.jmh_patho_tissue_list_2.clear()
        # populate JMH_TS list
        for e in ts:
            self.jmh_patho_tissue_list.addItem(str(e))
        # populate JMH_BM list
        for e in bm:
            self.jmh_patho_bm_list.addItem(str(e))
            
        for e in sq:
            self.jmh_patho_tissue_list_2.addItem(str(e))

    def pullfiles(self, tissue_case, bm_case, sq_case,
                  jpth_cln_cpath, jpth_cln_sq):  # called to pull file names into gui lists
        arro = [tissue_case, bm_case]
        caselist_ts = []
        caselist_bm = []
        caselist_sq = []
        bmnum = 0
        tsnum = 0
        sqnum = 0

        src = jpth_cln_cpath
        for filef in os.listdir(src):
                if re.match(arro[0], filef):
                    caselist_ts.append(filef)        
                    tsnum += 1
                elif re.match(arro[1], filef):
                    caselist_bm.append(filef)
                    bmnum += 1

        src = src = jpth_cln_sq
        for files in os.listdir(src):
            if re.match(sq_case, files):
                caselist_sq.append(files)
                sqnum += 1
 
        self.jmh_patho_tissue_num.setText(str(tsnum))
        self.jmh_patho_bm_num.setText(str(bmnum))
        self.jmh_patho_tissue_num_2.setText(str(sqnum)) 

        return caselist_ts, caselist_bm, caselist_sq

    def logcase(self, singlefile, case_log_patho, casenum, casename, matrix, typeflow, username):

        nowyr = time.ctime()[-4:]  # curr year
        nowday = time.ctime()[8:10]  # curr day
        nowmonth = time.ctime()[4:7]  # curr day 
        nowhr = time.ctime()[11:19]  # curr hr
        month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        date = str(month[nowmonth]) + "/" + str(nowday) + "/" + str(nowyr)
        
        
        os.open(case_log_patho, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
        with open(case_log_patho, "r+") as log:  # title to text log - runonly once
            titler = log.read()
            isnewlog = titler.rfind(singlefile)
            
        if isnewlog == -1:
            with open(case_log_patho, "a") as log:
                log.write(singlefile + "," + casenum + "," + casename + "," + matrix + "," + typeflow + ","
                          + date + "," + nowhr + "," + username + "\n")
                log.close

    def donecases(self, jpth_cln_cpathdone, jpth_cln_sqdone):
        os.startfile(jpth_cln_cpathdone)
        os.startfile(jpth_cln_sqdone)

    def qccases(self, jpth_cln_qc): 
        os.startfile(jpth_cln_qc)   

    def rxhcases(self, jpth_cln_rsch): 
        os.startfile(jpth_cln_rsch)  

    def closeEvent(self, event):
        os.system(r"NET USE %s: /DELETE /YES" % drive)
        return "N"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
    
