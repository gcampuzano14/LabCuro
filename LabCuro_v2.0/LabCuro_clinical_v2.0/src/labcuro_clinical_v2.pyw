#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         LabCuro Clinical Suite
# Created:      2014
# Version:      Version: 2.0
# Copyright:    (c) German Campuzano Zuluaga gcampuzanozuluaga@med.miami.edu 
#-------------------------------------------------------------------------------
import os
import time
import shutil
import re
import sys
from PySide.QtCore import *
from PySide import *
from PySide.QtGui import *
import labcuroMainWindow
import startupGui
import win32api
from contextlib import contextmanager
import subprocess
import json
import database_handler as database_handler
import map_network_drive
import images_qr

# interpret QT GUI into PYHTON CODE: C:\anaconda\Scripts\pyside-uic.exe flowMainWindow.ui -o flowMainWindow.py
# C:\anaconda\Scripts\pyside-uic.exe startupGui.ui -o startupGui.py
# compile executable: python -O C:\Users\germancz\Dropbox\Programming\Python\pyinstaller\pyinstaller.py --onefile --noconsole main.pyw

class StartupGui(QDialog, QWidget, startupGui.Ui_Dialog_start):
    def __init__(self, parent=None, username=None, password=None, netdrive=None):
        super(StartupGui, self).__init__(parent)
        self.username = username
        self.password = password
        self.netdrive = netdrive
        self.setupUi(self, self.username, self.password, self.netdrive)
        self.connect(self.start_ok, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.start_kill.clicked.connect(self.end_all)
    def end_all(self):
        self.close()  
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            self.accept()
            
class MainWindow(QMainWindow, labcuroMainWindow.Ui_MainWindow, StartupGui):
    global now
    global nowtime

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        structure, username, poweruser, poweruser_list = self.startdialog()
        self.setupUi(self, structure, username, poweruser, poweruser_list)

    def closeEvent(self, event):
        for e in netdrives:
            os.system(r"NET USE %s: /DELETE /YES" % e)

    def startdialog(self):
        global netdrives
        global db_master
        ## COMNFIG DB PATH
        db_master = os.path.join(os.path.dirname(__file__),'bin','master_config.sqlite')
        
        ## GET POWER_USER LIST
        query = '''SELECT user FROM master_users'''
        poweruser_list = database_handler.query_data(db_master, query)
  
        #READ NETWOR DRIVE FROM LOCAL TXT CONFIG FILE
        query = '''SELECT server_path FROM server_list'''
        shares = database_handler.query_data(db_master, query)
        query = '''SELECT lab_id FROM server_list'''
        ids = database_handler.query_data(db_master, query)
        dict_shares = dict(zip(ids, shares))
        print dict_shares
        map_network_drive.mapped_drives(shares)
        netdrives,  username, poweruser = self.network_share_auth(dict_shares)
        structure = self.file_architect(netdrives, username)
        return structure, username, poweruser, poweruser_list

    def network_share_auth(self, dict_shares):
        drive_letters = []
        non_success = 1
        username = ''   
        password = ''  
        no_connect=[]   
        for netdrive in dict_shares:
            startupwin = StartupGui(self, username, password, str(netdrive))
            #Initialize StartupGui with ".exec_()"
            if startupwin.exec_():
                username = str(startupwin.username.text())
                password = str(startupwin.password.text())
                domain = str(startupwin.domain.text()) 
                poweruser =  str(startupwin.powerpassword.text())#1haveth3p0w3r
            else:
                non_success = 0
            try:
                letter = map_network_drive.map_netdrive(dict_shares[netdrive], domain, username, password)
                drive_letters.append(letter)
            except:
                no_connect.append(netdrive)
                pass
        if len(drive_letters)==0 and non_success == 1:
            flags = QtGui.QMessageBox.StandardButton.Ok
            msg = "Wrong input. Check password and/or user name"
            QtGui.QMessageBox.warning(self, "Warning!", msg, flags)  
            sys.exit(0)
        if len(drive_letters)==0 and non_success == 0:
            sys.exit(0)
        if len(drive_letters)!= len(dict_shares):     
            flags = QtGui.QMessageBox.StandardButton.Ok
            msg = "Wrong input for thew following servers: " + str(', '.join(no_connect)) + "\n You will only have access to the server\s with correct access information"
            QtGui.QMessageBox.warning(self, "Warning!", msg, flags)  
        else:
            pass     
        return drive_letters, username, poweruser
    
    # THIS FUNCTION CREATES THE FOLLOWING DATA STRUCTURE (DICTIONARY) TO BUILD THE GUI:
    # { SERVICE_1 : { TEST_LAB_1 : { PATH_CHARACTERISTICS : [ { PATH : str, PATTERNS : str }, { }, ... ], ROOT_PATH : str }, TEST_LAB_n : {} }, SERVICE_n : {}, ... } 
    def file_architect(self, netdrives, username):
        # CONSTRUCT TEMPLATE STRUCTURE FOR GUI AND SAVE TO VARIABLE  'structure' 
        # 'structure'={SERVICE:{LAB:{'root_path':PATH},'path_chars':[{'path':FULL_PATH},{'patterns':{'BM|PB':REGEX},{'TS|FL':REGEX}}]},LAB2:{...}},SERVICE2:{...},...} 
        structure = {}
        for drive in netdrives:
            # FOR EACH SERVER DIRECTORY READ CONFIG FILE (~\TECHNCAL\lc_clinical_confic.json) INTO VARIABLE 'drive_settings' 
            # 'drive_settings' IS A LIST OF MACHINE/INSTRUMENT DICTIONARIES = [{machine1},{machine2},{machine3},...]
            drive = drive + ':'
            tech_dir = os.path.join(drive, 'TECHNICAL')
            config_file = os.path.join(tech_dir, 'lc_clinial_config.json')
            with open(config_file, 'r+') as set_json:
                drive_settings = json.loads(set_json.read())
            # LOOP THROUGH MACHINES/INSTRUMENTS IN 'drive_settings', 'machine' = {'lab_name': NAME, 'lab_attributes': {ATTRIBUTES}}
            for machine in drive_settings:
                # PULL SERVICE (EX. FLOW, MOLEC, ECT) FROM 'machine'['lab_attributes']['services']' AND ADD SERVICE TO 'structure'
                lab_service = machine['lab_attributes']['service']['test_category']
                lab = machine["lab_name"]
                # CREATE LAB_SERVICE ENTRY IF DOES NOT EXIST
                if lab_service not in structure:
                    structure[lab_service] = {}
                # CREATE LAB ENTRY IS DOES NOT EXIST
                if lab not in structure[lab_service]:
                    structure[lab_service][lab] = {}
                    structure[lab_service][lab]['root_path'] = '' 
                    structure[lab_service][lab]['path_chars'] = []
                # PULL PATHS AND REGEXES
                for direct in machine['lab_attributes']['service']['directories']['local_paths']:
                    #CHECK IF THE PATH FOR A DRIVE IS MEANT FOR CLINICAL USE AND GET INFO FOR ALL THE PATHS (EX. COPATH, SUNQUEST, QC ...)
                    if direct['netdrive_clinical_paths']:
                        # LOOP THROUGH ALL CLINICAL PATHS AND SELECT ONES TO DISPLAY
                        for e in direct['netdrive_clinical_paths']:
                            if direct['netdrive_clinical_paths'][e]['add_to_clin_database']:
                                clinical_files_path = re.match('(.+)\\\\.+$', str(e), re.IGNORECASE).group(1)
                                # 'root_path' IS LAB LEVEL PATH TO CREATE LAB TREEWIDGET ONCE PER SERVICE
                                structure[lab_service][lab]['root_path'] = os.path.join(drive,'LABS', clinical_files_path)
                                path = os.path.join(drive,'LABS', e)
                                #tempdir = {'path' : path, 'patterns' : direct['netdrive_clinical_paths'][e]['add_to_clin_database']}
                                if len(structure[lab_service][lab]['path_chars']) > 0:
                                    path_list = []
                                    i = 0
                                    for all_paths in structure[lab_service][lab]['path_chars']:
                                        path_list.append(all_paths['path'])
                                    if path in path_list:
                                        for origin_pattern in direct['netdrive_clinical_paths'][e]['add_to_clin_database']:
                                            if origin_pattern not in all_paths['patterns']:
                                                structure[lab_service][lab]['path_chars'][i]['patterns'][origin_pattern] = (direct['netdrive_clinical_paths']
                                                                                                                            [e]['add_to_clin_database']
                                                                                                                           [origin_pattern])
                                        break
                                    tempdir = {'path' : path, 'patterns' : direct['netdrive_clinical_paths'][e]['add_to_clin_database']}
                                    structure[lab_service][lab]['path_chars'].append(tempdir) 
                                    i += 1
                                else:
                                    tempdir = {'path' : path, 'patterns' : direct['netdrive_clinical_paths'][e]['add_to_clin_database']}
                                    structure[lab_service][lab]['path_chars'].append(tempdir)    
        
        ## PRINT STRUCTURE FOR DEBUGGING_________
        #os.open('structure.txt', os.O_RDWR | os.O_CREAT)
        #with open('structure.txt', 'wb') as out:
         #   out.write(str(structure))
        ## ________________________
              
        return structure
  
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
    
