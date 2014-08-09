#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         LabCuro Laboratory Suite
# Created:      2014
# Version:      Version: 2.0
# Copyright:    (c) German Campuzano Zuluaga gcampuzanozuluaga@med.miami.edu
#-------------------------------------------------------------------------------
import os
import time
import shutil
import re
import json
import csv
import datetime
import useful_fx
import install_labcuro
import map_network_drive
import multi_inputbox
import pdf_merger
import admin_settings
import database_handler
import webbrowser
import sys
import distutils
from easygui_labcuro import msgbox, buttonbox, ccbox, choicebox


#from PySide.QtCore import *
#from PySide import *
#from PySide.QtGui import *
#import date_range

#python C:\Users\germancz\Dropbox\Programming\Python\APPS\pyinstaller\Makespec.py --noconsole --icon="D:\Dropbox\Programming\Python\PY_APPS_COLLABORATIVE\LabCuro\LabCuro_clinical\src\bin\images\labcuro_chromatogram.ico" --name="LabCuro Laboratory Suite v2.0" LabCuro_lab_v2.0.py 

# compile executable: python -O C:\Users\germancz\Dropbox\Programming\Python\APPS\pyinstaller\pyinstaller.py --onefile C:\Users\germancz\Dropbox\Programming\Python\APPS\flow_manager_program\FlowIt v2.1.py

def main():
    
    #print os.path.dirname(__file__)
    if getattr(sys, 'frozen', False):
        print os.path.dirname(os.path.dirname(sys.executable))
    else:
        print 'not fs'
        os.path.dirname(__file__)
    
    place = ''
    inst = install_labcuro.install_labcuro()
    #setup = install_labcuro.setup()

    bindir = ''.join(['labcuro_bin', place])
    ## MASTER ADMIN CONFIGURATION
    #settings_path = os.path.join(os.path.dirname(__file__),bindir,'local_settings.json')
    settings_path = bindir + '\\local_settings.json'
    if os.path.exists(settings_path):
        #localconfig = os.path.join(os.path.dirname(__file__),bindir,'config.json')
        localconfig = bindir + '\\config.json'
        with open(localconfig, 'r+') as set_json:
            config_json = set_json.read()
        admin_config = json.loads(config_json)
        #print masteruser_list 

    else:
        #localconfig_dir = os.path.join(os.path.dirname(__file__), bindir)
        localconfig_dir = bindir
        localconfig = os.path.join(localconfig_dir, 'config.json')
        admin_settings.config(localconfig_dir)
        with open(localconfig, 'r+') as set_json:
            config_json = set_json.read()
        admin_config = json.loads(config_json)
        inst.install_main(settings_path, admin_config, place, bindir)
        #os.mkdir(os.path.join(os.path.dirname(__file__), str('temp'+place)))
        os.mkdir(str('temp'+place))
        
    ## PULL LOCAL SETTINGS TO VARIABLE
    with open(settings_path, 'r+') as set_json:
        settings_json = set_json.read()
    local_settings = json.loads(settings_json)  


    ## CONNECT TO NETWORK DRIVE
    msg         =  None
    title       = 'LabCuro v2.0 - Laboratory Suite'
    #image = "labcuro_sim.gif"
    fieldNames  = ['User name', 'Password']
    #vals = ['gcampuzano ', 'cAmpzUlu52']
    vals = ['', '']    
    #vals = ['gcampuzanozuluaga', 'Gcz2348.']
    netdrive_access = multi_inputbox.multipleinput(msg, title, fieldNames, True, False, fieldValues = vals, verification = False)
    
    ## CONNECT TO NETWORK DRIVE
    netdrive = local_settings['lab_attributes']['service']['directories']['destination_server']['serv_path']
    domain = local_settings['lab_attributes']['service']['directories']['destination_server']['domain']
    username = netdrive_access[0]
    password = netdrive_access[1]
    map_network_drive.mapped_drives(netdrive)
    networkdriveletter = map_network_drive.map_netdrive(netdrive, domain, username, password) + ':'
    #print netdrive
    map_network_drive.mapped_drives(netdrive)
    lab_service = local_settings['lab_attributes']['service']['test_category']
    
    
    db_clin_name = os.path.join(networkdriveletter, 'TECHNICAL', 'clinical_cases.db')
    #db_tech_name = os.path.join(str(os.path.dirname(__file__)), bindir, str('tech_runs_' + place + '.db'))
    if getattr(sys, 'frozen', False):
        db_tech_name = os.path.join(str(os.path.dirname(sys.executable)), bindir, str('tech_runs_' + place + '.db'))
    elif __file__:
        db_tech_name = os.path.join(str(os.path.dirname(__file__)), bindir, str('tech_runs_' + place + '.db'))
    #db_clin_name = 'clinical_cases_' + place + '.db' 
    #db_tech_name = 'tech_runs_' + place + '.db'

    #INITIAL SCREEN
    masteruser_list = [str(x) for x in admin_config['master_users']]
    title = "LabCuro v2.0 - Laboratory Suite"
    #icon_dir = os.path.join(os.path.dirname(__file__),'bin','images')
    #image = os.path.join(icon_dir,'labcuro_sim.gif')
    image = 'bin\\images\\labcuro_sim.gif'
    if username.lower().strip() in masteruser_list:
        btnchoices = ["Run file transfer", 'Add new path', 'Utilization data dump', 'About', 'Help', 'Quit']
    else:
        btnchoices = ["Run file transfer", 'About', 'Help', 'Quit']
    intro = buttonbox(image=image, title=title, choices=btnchoices)
    if intro == "Quit":
        #quit()
        os.system(r"NET USE %s: /DELETE /YES" % networkdriveletter[0])
        sys.exit(0)
    elif intro == "Add new path":
        labname = local_settings['lab_name']
        test_category = lab_service
        instrument_id = local_settings['lab_attributes']['machine_id']
        networkdrive_letter = networkdriveletter[-2]
        remote_techDir = os.path.join(networkdrive_letter, netdrive, 'TECHNICAL')
        setup = install_labcuro.install_labcuro()
        local_settings = setup.set_filesystem(labname, test_category, instrument_id, local_settings, networkdrive_letter, admin_config, place)
        setup.write_config(local_settings, settings_path)
        setup.remote_set_generator(remote_techDir, local_settings, labname, instrument_id, test_category)
        os.system(r"NET USE %s: /DELETE /YES" % networkdriveletter[0])  
        sys.exit(0)
        #quit()
    elif intro == 'Utilization data dump':
        db_remote = os.path.join(networkdriveletter, 'TECHNICAL', 'clinical_cases.db')
        
        #print db_remote
        #print QDate.currentDate()
        #t = date_range.Ui_dates()
        #t.setupUi([QDate.currentDate(),QDate.currentDate()])
        nowtime = ' '.join([str(datetime.date.today()), str(time.asctime()[11:19])])   
        query = '''SELECT * FROM case_log WHERE date_sent_to_pathology BETWEEN "2013-07-06 00:00:00" AND "''' + nowtime + '''" '''
        #query = '''SELECT * FROM case_log WHERE date_sent_to_pathology BETWEEN "2013-07-06 00:00:00" AND "2014-09-30 00:00:00" '''
        data = database_handler.query_data(db_remote, query)
        #out_csv = os.path.join(os.path.dirname(__file__),bindir,'output.csv')
        if getattr(sys, 'frozen', False):
            out_csv = os.path.join(os.path.dirname(sys.executable),bindir,'output.csv')
        elif __file__:
            out_csv = os.path.join(os.path.dirname(__file__),bindir,'output.csv')
            
        os.open(out_csv, os.O_RDWR | os.O_CREAT)
        with open(out_csv, 'wb') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(['index', 'lab_name', 'lab_service', 'instrument_id', 'accession_number',  'patient_name', 'matrix', 'panel', 'lab_tech', 'date_sent_to_pathology', 'training_pathologist', 'pathologist', 'date_reviewed_pathologist'])
            writer.writerows(data)
        #os.startfile(out_csv)  
        os.system('start ' + out_csv)
        os.system(r"NET USE %s: /DELETE /YES" % networkdriveletter[0])  
        sys.exit(0)
        #quit()    
    elif intro == "About":
            msg_about = """ 
                LabCuro version 2.0 - Laboratory Suite
                
                Copyright (C) 2014  GERMAN CAMPUZANO-ZULUAGA 
                
                This program is free software: you can redistribute it and/or modify
                it under the terms of the GNU General Public License as published by
                the Free Software Foundation, version 3 of the License.
                
                This is free software, and you are welcome to redistribute it
                under certain conditions.          
                      
                This program is distributed in the hope that it will be useful,
                but WITHOUT ANY WARRANTY; without even the implied warranty of
                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                GNU General Public License for more details.
                
                To find a copy of the license please visit:
                http://www.gnu.org/licenses/
                
                Contact: germancz81@gmail.com
                Source: https://github.com/gcampuzano14/LabCuro
                """
            msgbox(image=image, title='About LabCuro v2.0', msg = msg_about)
            sys.exit(0)
            #quit()
    elif intro == 'Help':
        new = 2 # open in a new tab, if possible
        # open a public URL, in this case, the webbrowser docs
        url = "https://github.com/gcampuzano14/LabCuro/tree/master/LabCuro_v2.0/manuals"
        webbrowser.open(url,new=new)
    
    #RUN MAIN FILE PROCESS FUNCTION
    fp = file_process()
    fp.path_cycle(local_settings, lab_service, username, networkdriveletter, db_clin_name, db_tech_name, place)
    
    print 'FILE TRANSFER COMPLETE'
    print 'CLICK "ENTER" KEY TO EXIT'
    os.system("pause")
    
    
    #DISCONNECT TO NETWORK DRIVE WHEN DONE
    os.system(r"NET USE %s: /DELETE /YES" % networkdriveletter[0])

class file_process: 
    global now_number
    global now
    global now_str
    global year
    now_number = (((time.time() / 60) / 60) / 24) ## DAYS SINCE PYTHON SELECED START TIME 1970S??
    now = datetime.datetime.now()
    year = now.year
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #print 'times'
    #print now_number, now, now_str

    def path_cycle(self, local_settings, lab_service, username, networkdriveletter,   db_clin_name, db_tech_name, place=None):
        paths = local_settings['lab_attributes']['service']['directories']['local_paths'] 
        lab_name = local_settings['lab_name']
        deleted_items_local = {}
        clinical_cases_sent = {}
        clinical_cases_failtosend = {}
        backed_up_items = {}
        bkp_cnt = 0
        clin_cnt = 0
        fail_cnt = 0
        del_local_cnt = 0
        instrument_id = local_settings["lab_attributes"]["machine_id"]
        for path in paths:
            #bkp paths
            source = path['local_origin_path']
            local_temp_destination = os.path.join(path['local_sent_path'], path['name_backup_path'])
            remote_perm_destination = os.path.join(networkdriveletter, 'LABS', path['netdrive_backup_path'], str(year)) #SEPARATE BACKUP BY YEAR
            if not os.path.isdir(remote_perm_destination):
                os.mkdir(remote_perm_destination)
            
            ## GET TIMES
            days_del_local = float(path['local_choptail_days'])
            #print 'days del local = '+str(days_del_local)
            
            if path['clinical_file'] == 'CLINICAL':
                days_del_remote = float(path['netdrive_clinical_choptail_days']) #CHECKED AND WORKS JULY 1 2014
                #print 'days del done remote = '+str(days_del_remote)
            else:
                delta_backup = float(path['delta_hr_bkp'])
                #print 'hrs delta bkp = '+str(delta_backup)
            ## ____________________
            
            #clinical paths
            clinical_paths = path['netdrive_clinical_paths']
            
            source_results = self.file_cycle(networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup=None)
            #print clinical_paths
            if source_results:
                clinical_cases_sent[path['name_backup_path']] = source_results['yes_match']
                clin_cnt = clin_cnt + len(source_results['yes_match'])
                clinical_cases_failtosend[path['name_backup_path']] = source_results['no_match']
                fail_cnt = fail_cnt + len(source_results['no_match'])
                backed_up_items[path['name_backup_path']] = source_results['bkp_file']                 
                bkp_cnt = bkp_cnt + source_results['count']
            
            if path['clinical_file'] == 'CLINICAL':

                removed_done = [] 
                for clinical_path in clinical_paths:
                    true_clinical_path = os.path.join(networkdriveletter, 'LABS', clinical_path)
                    clinical_done = true_clinical_path
                    #clinical_done = os.path.join(true_clinical_path, 'DONE') ## GETTING RID OF 'DONE' FOLDER
                    for file_name in os.listdir(clinical_done):
                        item = os.path.join(clinical_done, file_name)
                        file_time_days = (((os.stat(item).st_mtime)/ 60) / 60) / 24
                        file_time_days = now_number - file_time_days
                        
                        ## REMOVE OLD FILES FROM REMOTE CLINICAL (PROCESSED AND RAW) DIRECTORIES
                        #print 'FILE: ' + str(file_name) + ' AGE DAYS: ' + str(file_time_days) + ' del remote: ' + str(days_del_remote)
                        if file_time_days > days_del_remote:
                            removed_done.append(item)
                            if os.path.isdir(item):
                               shutil.rmtree(item)
                            elif os.path.isfile(item):
                                os.remove(item) 
                        ## _______________________ # CHECKED AND WORKS JULY 1 2014
                    #temp_path = os.path.join(os.path.dirname(__file__), str('temp'+place))
                    if getattr(sys, 'frozen', False):
                        temp_path = os.path.join(os.path.dirname(sys.executable), str('temp'+place))  
                        
                    elif __file__:    
                        temp_path = os.path.join(os.path.dirname(__file__), str('temp'+place))
                        
                    files_to_log = {}     
                    if clinical_paths[clinical_path]['to_merge']: 
                        merge_regex = clinical_paths[clinical_path]['to_merge']
                        for file_unmerged in os.listdir(true_clinical_path):
                            #file_tomerge = os.path.join(true_clinical_path, file_unmerged)
                            files_to_kill = pdf_merger.pdfmerger(true_clinical_path, file_unmerged, merge_regex, temp_path)
                            if files_to_kill:
                                for file_kill in files_to_kill:
                                    os.remove(file_kill)
                        for temp_file in os.listdir(temp_path):
                            source = os.path.join(temp_path, temp_file)
                            destination = os.path.join(true_clinical_path, temp_file.upper())
                            shutil.move(source, destination)
                            os.system("start " + destination)  
                            #os.startfile(destination)     
                            if clinical_paths[clinical_path]['add_to_clin_database']:
                                file_regex_pattern = clinical_paths[clinical_path]['find_folder']
                                matches = re.match(file_regex_pattern, temp_file, re.IGNORECASE)
                                accession_number = matches.group(1)
                                patient_name = matches.group(2)
                                matrix = matches.group(3)
                                panel = matches.group(4)
                                files_to_log[temp_file] =  {'accession_number':accession_number, 'patient_name':patient_name, 'matrix':matrix, 'panel':panel}
                                #print accession_number, patient_name, matrix, panel, str(now_str), str(instrument_id)    
                    else:
                        if clinical_paths[clinical_path]['add_to_clin_database']:
                            for file_unsorted in os.listdir(true_clinical_path):
                                newfile_match = re.match('^{{{_NEW_FILE_}}}(.+)', file_unsorted, re.IGNORECASE)
                                if newfile_match:
                                    #print file_unsorted
                                    processed_file = newfile_match.group(1)
                                    #print processed_file
                                    file_regex_pattern = clinical_paths[clinical_path]['find_folder']
                                    matches = re.match(file_regex_pattern, processed_file, re.IGNORECASE)
                                    accession_number = matches.group(1)
                                    patient_name = matches.group(2)
                                    matrix = matches.group(3)
                                    panel = matches.group(4)
                                    files_to_log[processed_file] = {'accession_number':accession_number, 'patient_name':patient_name, 'matrix':matrix, 'panel':panel}
                                    
                                    if processed_file in os.listdir(true_clinical_path):
                                        os.remove(os.path.join(true_clinical_path,processed_file))
                                        os.rename(os.path.join(true_clinical_path, file_unsorted), os.path.join(true_clinical_path, processed_file))
                                    else:
                                        os.rename(os.path.join(true_clinical_path, file_unsorted), os.path.join(true_clinical_path, processed_file))
                                    #os.startfile(os.path.join(true_clinical_path, processed_file))
                                    os.system("start " + os.path.join(true_clinical_path, processed_file))
                    if clinical_paths[clinical_path]['add_to_clin_database']:             
                        for filename in files_to_log:
                            accession_number = files_to_log[filename]['accession_number']
                            patient_name = files_to_log[filename]['patient_name']
                            matrix = files_to_log[filename]['matrix']
                            panel = files_to_log[filename]['panel']
                            
                            insert_vals = ('INSERT INTO case_log(lab_name, lab_service, instrument_id, accession_number, patient_name, matrix, panel, lab_tech, date_sent_to_pathology)'    
                                          'VALUES(:lab_name, :lab_service, :instrument_id, :accession_number, :patient_name, :matrix, :panel, :lab_tech, :date_sent_to_pathology)')
                            
                            dicts = {'lab_name':str(lab_name), 'lab_service':str(lab_service), 'instrument_id':str(instrument_id), 'accession_number':str(accession_number), 
                                     'patient_name':str(patient_name), 'matrix':str(matrix),'panel':str(panel), 'lab_tech':str(username), 'date_sent_to_pathology' : str(now_str)}
                            #print dicts
                            database_handler.insert_data(insert_vals, dicts, db_clin_name)
                        #os.startfile(true_clinical_path)
                        os.system('start '  + true_clinical_path)
                    
            deleted_items_local[path['name_backup_path']] = []
            for file_name  in os.listdir(local_temp_destination):
                #local_done = os.path.join(local_temp_destination,file_name)
                #for file_name in os.listdir(local_done):
                item = os.path.join(local_temp_destination, file_name)
                file_time_days = (((os.stat(item).st_mtime)/ 60) / 60) / 24
                file_time_days = now_number - file_time_days
                
                ## REMOVE OLD LOCAL FILES - DIRECTORY WHERE ALL FILES GET SENT AFTER THEY ARE COPYED TO THE NETDRIVE BACKUP
                #print 'FILE: ' +  ' AGE DAYS: ' + str(file_time_days) + ' dele remote: ' + str(days_del_local)
                if file_time_days > days_del_local:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    del_local_cnt += 1
                    deleted_items_local[path['name_backup_path']].append(item)
                ## _______________________________ # CHECKED AND WORKS JULY 1 2014

        insert_vals = ('INSERT INTO tech_log(date_run, lab_name, instrument_id, lab_service, backed_up_items, bkp_cnt, deleted_items_local, del_cnt,' 
                       'clinical_cases_sent, clin_cnt, clinical_cases_failtosend, fail_cnt, lab_tech)'    
                       'VALUES(:date_run, :lab_name, :instrument_id, :lab_service, :backed_up_items, :bkp_cnt, :deleted_items_local, :del_cnt,' 
                       ':clinical_cases_sent, :clin_cnt, :clinical_cases_failtosend, :fail_cnt, :lab_tech)')
        
        dicts = {'date_run':str(now_str), 'lab_name':lab_name, 'instrument_id':instrument_id, 'lab_service': str(lab_service), 'backed_up_items':str(backed_up_items), 
                 'bkp_cnt': bkp_cnt, 'deleted_items_local':str(deleted_items_local), 'del_cnt': del_local_cnt,'clinical_cases_sent': str(clinical_cases_sent), 
                 'clin_cnt' : clin_cnt,  'clinical_cases_failtosend':str(clinical_cases_failtosend), 'fail_cnt':fail_cnt, 'lab_tech':str(username)}
        
        database_handler.insert_data(insert_vals, dicts, db_tech_name)
    
    def file_cycle(self, networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup):
        cnt = 0
        no_match = []
        yes_match = []
        bkp_file = []
        case_atributtes = True
        for file_name in os.listdir(source):
            file_name = file_name.upper()
            file_origin = os.path.join(source, file_name)
            file_local_destination = os.path.join(local_temp_destination, file_name)
            file_name_fixspaces = re.sub(r'\s{2,}', ' ', file_name)
            file_remote_destination = os.path.join(remote_perm_destination, file_name_fixspaces)
            if path['clinical_file'] == 'CLINICAL':
                case_atributtes = self.match(networkdriveletter, file_name_fixspaces, file_origin, clinical_paths)
                if case_atributtes == True:
                    yes_match.append(file_origin)                
                else:
                    no_match.append(file_origin)
            #backup if pattern is correct
            if case_atributtes:
                file_creation = os.stat(file_origin).st_mtime
                agehrs = (now_number * 24) - (((file_creation) / 60) / 60)
                
                ## PERFORM BACKUP IN BACKUP-ONLY DIRECTORIES AT SPECIFIED INTERVALS (HOURS) TO AVOID CONFLICT WITH ONGOING EXPERIMENTS
                #print file_name
                #print agehrs
                #agehrs = now_number - agehrs
                if agehrs > delta_backup:
                    self.copydirsfiles(file_origin, file_local_destination, file_remote_destination, now)
                elif path['clinical_file'] == 'CLINICAL': #clinical cases crossover to backup at the same time they go to clinical folders to avoid dups
                    self.copydirsfiles(file_origin, file_local_destination, file_remote_destination, now)
                cnt += 1
                bkp_file.append(file_name)
                ## _________________________
                
        if len(no_match) > 0:
            no_match_str = ""
            for e in no_match:
                no_match_str = "\n".join([no_match_str,e])
            msg = ('Clinical case name does not have an acceptable pattern.\nIncorrect case:' + no_match_str )
            title = "LabCuro v2.0 - Laboratory Suite - Setup"
            choice = ccbox(msg, title)
            if choice == 1:
                useful_fx.openFolder(source)
                #os.startfile(os.path.dirname(file_origin))
                os.system('start ' + os.path.dirname(file_origin))
                self.file_cycle(networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup)
            else:
                msgbox("This application will end but you must fix the files and re-run the program. These are clinical samples.")
                return None
                time.sleep(0.3)
                #os.startfile(os.path.dirname(file_origin))
                os.system('start ' + os.path.dirname(file_origin))
        return {'no_match' : no_match, 'yes_match' : yes_match, 'bkp_file' : bkp_file, 'count' : cnt}
         
    def match(self, networkdriveletter, file_name, file_origin, clinical_paths):
        chksum = useful_fx.checksums()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        time_stamp = useful_fx.date_serial(year, month, day, hour, minute, second)
        for clinical_path in clinical_paths:
            #print clinical_path
            if clinical_paths[clinical_path]['to_merge']: 
                to_merge = '{{{_FILE_TO_MERGE_}}}' + file_name
                destination_file = os.path.join(networkdriveletter, 'LABS', clinical_path, to_merge)
            else:

                if clinical_paths[clinical_path]['add_to_clin_database']:
                    newfile_name = '{{{_NEW_FILE_}}}' + file_name
                else:
                    newfile_name = file_name
                destination_file = os.path.join(networkdriveletter, 'LABS', clinical_path, newfile_name)
            file_regex_pattern = clinical_paths[clinical_path]['find_folder']
            matches = re.match(file_regex_pattern, file_name, re.IGNORECASE)
            if matches: # any file matched
                #print newfile_name, destination_file
                if os.path.isdir(file_origin):
                    if os.path.exists(destination_file):
                        destination_file = destination_file + "_COPY_" + time_stamp  
                    shutil.copytree(file_origin, destination_file, symlinks=False, ignore=None)
                    
                else:
                    if os.path.exists(destination_file):
                        extension = '.' + file_origin[-3:]
                        destination_file = destination_file[:-4] + "_COPY_" + time_stamp + extension
                    shutil.copy2(file_origin, destination_file)                
                return True
        return False

    def copydirsfiles(self, file_origin, file_local_destination, file_remote_destination, now):
        print file_origin
        chksum = useful_fx.checksums()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        time_stamp = useful_fx.date_serial(year, month, day, hour, minute, second)
        if os.path.isdir(file_origin):  #procedure for a directory
            #print 'isdir'
            if os.path.exists(file_local_destination):
                file_local_destination = file_local_destination + "_COPY_" + time_stamp
            if os.path.exists(file_remote_destination):
                file_remote_destination = file_remote_destination + "_COPY_" + time_stamp       
            #COPY DIRECTORIES AND PERFORM CHECKSUMS
            passed = []
            shutil.copytree(file_origin, file_local_destination, symlinks=False, ignore=None)
            passed.append(chksum.check_dirs([file_origin, file_local_destination]))
            shutil.copytree(file_origin, file_remote_destination, symlinks=False, ignore=None)
            passed.append(chksum.check_dirs([file_origin, file_remote_destination]))
        else:  #PROCEDURE for a file
            extension = '.' + file_origin[-3:]
            if os.path.exists(file_local_destination):
                file_local_destination = file_local_destination[:-4] + "_COPY_" + time_stamp + extension
            if os.path.exists(file_remote_destination):
                file_remote_destination = file_remote_destination[:-4] + "_COPY_" + time_stamp + extension          
            passed = []
            shutil.copy2(file_origin, file_local_destination)
            passed.append(chksum.check_files([file_origin, file_local_destination]))
            shutil.copy2(file_origin, file_remote_destination)
            passed.append(chksum.check_files([file_origin, file_remote_destination]))
            
        if False in passed:
            destinations = [file_local_destination, file_remote_destination]
            for d in destinations:
                if os.path.exists(d):
                    if os.path.isdir(d):
                        shutil.rmtree(d)
                    elif os.path.isfile(d):
                        os.remove(d)
                else:
                    pass      
        else:
            if os.path.isdir(file_origin):
                shutil.rmtree(file_origin)
            elif os.path.isfile(file_origin):
                os.remove(file_origin)
main()