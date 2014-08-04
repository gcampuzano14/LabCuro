#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         LabCuro Lab
# Created:      September 9  2014
# Version:      Version: 3.0
# German Campuzano Zuluaga gcampuzanozuluaga@med.miami.edu 2014
#-------------------------------------------------------------------------------
import os
import time
import shutil
import re
import json
import datetime
import useful_fx
import install_labcuro
import map_network_drive
import multi_inputbox
import pdf_merger
import admin_settings
import database_handler
from easygui_labcuro import msgbox, buttonbox, ccbox, choicebox

# compile executable: python -O C:\Users\germancz\Dropbox\Programming\Python\APPS\pyinstaller\pyinstaller.py --onefile C:\Users\germancz\Dropbox\Programming\Python\APPS\flow_manager_program\FlowIt v2.1.py
def main():
    
    place = 'vprotocz_testenviron'
    inst = install_labcuro.install_labcuro()
    setup = install_labcuro.setup_labcuro()
    #place = 'hosp'
    #MASTER ADMIN CONFIGURATION
    localconfig = os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep + 'config.json'
    with open(localconfig, 'r+') as set_json:
        config_json = set_json.read()
    admin_config = json.loads(config_json)
    
    settings_path = os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep + 'local_settings_'+ place +'.json'
    if os.path.exists(settings_path):
        pass
    else:
        inst.install_main(settings_path, admin_config, place)
    #PULL LOCAL SETTINGS TO VARIABLE
    with open(settings_path, 'r+') as set_json:
        settings_json = set_json.read()
    local_settings = json.loads(settings_json)  


   #CONNECT TO NETWORK DRIVE
    msg         = ('Enter values for laboratory service')
    title       = 'LabCuro  v3.0'
    fieldNames  = ['User name', 'Password']
    vals = ['gcampuzano ', 'g3rcamzul']
    #vals = ['gcampuzanozuluaga', 'Gcz2348.']
    netdrive_access = multi_inputbox.multipleinput(msg, title, fieldNames, True, False, fieldValues = vals, verification = False)
    db_clin_name = str(os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep +'clinical_cases_' + place + '.db')
    db_tech_name = str(os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep +'tech_runs_' + place + '.db')
    #db_clin_name = 'clinical_cases_' + place + '.db'
    #db_tech_name = 'tech_runs_' + place + '.db'

    #SELECT LABORATORY SERVICE
    service_list = []
    service = local_settings['lab_attributes']['service']
    for service in service:
        service_list.append(service['test_category'])
    if len(service_list) > 1:
        msg =('Select the type laboratory test category to transfer')
        sites = service_list
        lab_service = choicebox(msg, title, sites)
        service_number = service_list.index(lab_service)
    else:
        lab_service = service[0]['test_category']
        service_number = 0

    #CONNECT TO NETWORK DRIVE
    netdrive = local_settings['lab_attributes']['service'][service_number]['directories']['destination_server']['serv_path']
    domain = local_settings['lab_attributes']['service'][service_number]['directories']['destination_server']['domain']
    username = netdrive_access[0]
    password = netdrive_access[1]
    networkdriveletter = map_network_drive.map_netdrive(netdrive, domain, username, password) + ':'

    #INITIAL SCREEN
    msg =   'Welcome LabCuro v3.0'
    title = "LabCuro v3.0"
    image = "mol.gif"
    btnchoices = ["Run file transfer", "Setup", 'Quit']
    intro = buttonbox(image=image,msg=msg, title=title, choices=btnchoices)
    if intro == "Quit":
        quit()
    elif intro == "Setup":
        setup.setup_main(local_settings, admin_config, place, networkdriveletter, domain)
        main()




    
    #RUN MAIN FILE PROCESS FUNCTION
    fp = file_process()
    fp.path_cycle(local_settings, lab_service, username, service_number, networkdriveletter, db_clin_name, db_tech_name)
    
    #DISCONNECT TO NETWORK DRIVE WHEN DONE
    os.system(r"NET USE %s: /DELETE /YES" % networkdriveletter[0])

class file_process: 
    global now_number
    global now
    global now_str
    global year
    now_number = time.time()
    now = datetime.datetime.now()
    year = now.year
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    def path_cycle(self, local_settings, lab_service, username, service_number, networkdriveletter,   db_clin_name, db_tech_name):
        paths = local_settings['lab_attributes']['service'][service_number]['directories']['local_paths'] 
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
            local_temp_destination = path['local_sent_path']
            remote_perm_destination = os.path.join(networkdriveletter, 'LABS', path['netdrive_backup_path'], str(year)) #SEPARATE BACKUP BY YEAR
            if not os.path.isdir(remote_perm_destination):
                os.mkdir(remote_perm_destination)
            delta_backup = path['delta_hr_bkp']
            days_del_local = path['local_choptail_days']
            #clinical paths
            clinical_paths = path['netdrive_clinical_paths']
            days_del_remote = path['netdrive_clinical_choptail_days'] #YES | NO
            source_results = self.file_cycle(networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup)
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
                    clinical_done = os.path.join(true_clinical_path, 'DONE')
                    for file_name in os.listdir(clinical_done):
                        item = os.path.join(clinical_done, file_name)
                        file_time_days = (((os.stat(item).st_mtime)/ 60) / 60) / 24
                        if file_time_days > days_del_remote:
                            removed_done.append(item)
                            os.remove(item)     
                    if clinical_paths[clinical_path]['to_merge']: 
                        merge_regex = clinical_paths[clinical_path]['to_merge']
                        for file_unmerged in os.listdir(true_clinical_path):
                            #file_tomerge = os.path.join(true_clinical_path, file_unmerged)
                            files_to_kill = pdf_merger.pdfmerger(true_clinical_path, file_unmerged, merge_regex)
                            if files_to_kill:
                                for file_kill in files_to_kill:
                                    os.remove(file_kill)
                        temp_path = os.path.join(os.path.dirname(__file__), 'temp')
                        for temp_file in os.listdir(temp_path):
                            source = os.path.join(temp_path, temp_file)
                            destination = os.path.join(true_clinical_path, temp_file)
                            shutil.move(source, destination)
                                           
                            if clinical_paths[clinical_path]['add_to_clin_database']:
                                file_regex_pattern = clinical_paths[clinical_path]['find_folder']
                                matches = re.match(file_regex_pattern, temp_file, re.IGNORECASE)
                                accession_number = matches.group(1)
                                patient_name = matches.group(2)
                                matrix = matches.group(3)
                                panel = matches.group(4)
                                insert_vals = ('INSERT INTO case_log_' + lab_name +  '(lab_service, accession_number, patient_name, matrix, panel, lab_tech, date_sent_to_pathology)'    
                                              'VALUES(:lab_service, :accession_number, :patient_name, :matrix, :panel, :lab_tech, :date_sent_to_pathology)')
                                dicts = {'lab_service':str(lab_service), 'accession_number':str(accession_number), 'patient_name':str(patient_name),
                                         'matrix':str(matrix),'panel':str(panel), 'lab_tech':str(username), 'date_sent_to_pathology' : str(now_str)}
                                database_handler.insert_data(insert_vals, dicts, db_clin_name)
        
            deleted_items_local[path['name_backup_path']] = []
            for item in os.listdir(local_temp_destination):
                file_time_days = (((os.stat(os.path.join(local_temp_destination,item)).st_mtime)/ 60) / 60) / 24
                if file_time_days > days_del_local:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    del_local_cnt += 1
                    deleted_items_local[path].append(item)

        insert_vals = ('INSERT INTO tech_log_' + lab_name + '_' + instrument_id + '(date_run, lab_service, backed_up_items, bkp_cnt, deleted_items_local, del_cnt,' 
                       'clinical_cases_sent, clin_cnt, clinical_cases_failtosend, fail_cnt, lab_tech)'    
                       'VALUES(:date_run, :lab_service, :backed_up_items, :bkp_cnt, :deleted_items_local, :del_cnt,' 
                       ':clinical_cases_sent, :clin_cnt, :clinical_cases_failtosend, :fail_cnt, :lab_tech)')
        
        dicts = {'date_run':str(now_str), 'lab_service': str(lab_service), 'backed_up_items':str(backed_up_items), 
                 'bkp_cnt': bkp_cnt, 'deleted_items_local':str(deleted_items_local), 'del_cnt': del_local_cnt, 
                 'clinical_cases_sent': str(clinical_cases_sent), 'clin_cnt' : clin_cnt, 
                 'clinical_cases_failtosend':str(clinical_cases_failtosend), 
                 'fail_cnt':fail_cnt, 'lab_tech':str(username)}
        database_handler.insert_data(insert_vals, dicts, db_tech_name)
    
    def file_cycle(self, networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup):
        cnt = 0
        no_match = []
        yes_match = []
        bkp_file = []
        case_atributtes = True
        for file_name in os.listdir(source):
            file_origin = os.path.join(source, file_name)
            file_local_destination = os.path.join(local_temp_destination, file_name)
            file_remote_destination = os.path.join(remote_perm_destination, file_name)
            if path['clinical_file'] == 'CLINICAL':
                case_atributtes = self.match(networkdriveletter, file_name,  file_origin, clinical_paths)
                if case_atributtes == True:
                    yes_match.append(file_origin)                
                else:
                    no_match.append(file_origin)
            #backup if pattern is correct
            if case_atributtes:
                file_creation = os.stat(file_origin).st_mtime
                agehrs = (((now_number - file_creation) / 60) / 60)
                if agehrs < delta_backup:
                    self.copydirsfiles(file_origin, file_local_destination, file_remote_destination, now)
                cnt += 1
                bkp_file.append(file_name)

        if len(no_match) > 0:
            no_match_str = ""
            for e in no_match:
                no_match_str = "\n".join([no_match_str,e])
            msg = ('Clinical case name does not have an acceptable pattern.\nIncorrect case:' + no_match_str )
            title = "LabCuro v3.0"
            choice = ccbox(msg, title)
            if choice == 1:
                useful_fx.openFolder(source)
                #os.startfile(os.path.dirname(file_origin))
                self.file_cycle(networkdriveletter, path, source, local_temp_destination, remote_perm_destination, clinical_paths, delta_backup)
            else:
                msgbox("This application will end but you must fix the files and re-run the program. These are clinical samples.")
                return None
                #time.sleep(0.3)
                #os.startfile(os.path.dirname(file_origin))
        return {'no_match' : no_match, 'yes_match' : yes_match, 'bkp_file' : bkp_file, 'count' : cnt}
         
    def match(self, networkdriveletter, file_name, file_origin, clinical_paths):
        for clinical_path in clinical_paths:
            if clinical_paths[clinical_path]['to_merge']:
                to_merge = '{{{_FILE_TO_MERGE_}}}' + file_name
                destination_file = os.path.join(networkdriveletter, 'LABS', clinical_path, to_merge)
            else:
                destination_file = os.path.join(networkdriveletter, 'LABS', clinical_path, file_name)
            file_regex_pattern = clinical_paths[clinical_path]['find_folder']
            matches = re.match(file_regex_pattern, file_name, re.IGNORECASE)
            if matches:
                shutil.copy2(file_origin, destination_file)
                return True
        return False

    def copydirsfiles(self, file_origin, file_local_destination, file_remote_destination, now):
        chksum = useful_fx.checksums()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        time_stamp = useful_fx.date_serial(year, month, day, hour, minute, second)
        if os.path.isdir(file_origin):  #procedure for a directory
            print 'isdir'
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

