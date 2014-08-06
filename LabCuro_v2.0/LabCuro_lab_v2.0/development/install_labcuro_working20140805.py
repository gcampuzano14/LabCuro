import os
import sys
import datetime
import json
import map_network_drive
import multi_inputbox
import database_handler
from easygui_labcuro import diropenbox, buttonbox, choicebox, enterbox, multchoicebox, msgbox

class install_labcuro:
    def install_main(self, settings_path, admin_config, place, bindir):
        # INTRO MESSAGGEBOX
        msg =   """ 
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
        title = "LabCuro v2.0 License"
        image = 'bin\\images\\labcuro_sim.gif'
        #icon_dir = os.path.join(os.path.dirname(__file__),'bin','images')
        #image = os.path.join(icon_dir,'labcuro_sim.gif')
        msgbox(image=image, msg=msg, title=title, ok_button="OK")
        msg =  """
               This is the first time you run LabCuro Lab on this instrument.
               Follow these instructions:\n
               1. Designate a laboratory name, laboratory service and instrument name
               2. Set the file paths that will be backed up
               3. Set the file paths that will be used to transmit PDF files for clinical use*
               4. Set the file paths that will be used to transmit raw analysis data files for clinical use*\n    
               * Backup paths will be created for files designated for clinical use.
               
               The information obtained from this setup will be saved to "\\labcuro_bin\\local_settings.json".
               """
        title = "LabCuro v2.0 Installation"
        image = 'bin\\images\\labcuro_sim.gif'
        #icon_dir = os.path.join(os.path.dirname(__file__),'bin','images')
        #image = os.path.join(icon_dir,'labcuro_sim.gif')
        btnchoices = ["Setup", "Cancel"]
        intro = buttonbox(image=image, msg=msg, title=title, choices=btnchoices)
        if intro == "Setup":
            pass
        else:
            quit()
        #DESIGNATE LABORATORY SERVICE ATTRIBUTES
        msg         = ('Enter values for laboratory service\nInput user name and password used to access network drive\n')
        title       = 'LabCuro v2.0 Installation'
        fieldNames  = ['Laboratory name',
                       'Test category',
                       'Instrument Name',
                       'Network drive address',
                       'Domain', 
                       'User name', 
                       'Password']
        
        #CREATE local_settings DATA STRUCTURE
        vals = ['', '', '', '', '', '', '']
        vals = ['MyLab', 'FLOW | MOLECULAR', '', '\\\\DOMAIN\DIRECTORY', 'MEDICAL', '', '']
        #vals = ['MyLab2', 'MOLECULAR', 'intrument_111', '\\\\protocz\german_share\labcurotest_1', 'protocz', 'gcampuzano ', 'cAmpzUlu52']
        #vals = ['test_lab_hospital', 'FLOW', 'intrument_666', '\\\\jhscel01.um-jmh.org\JMH_Flow_Cytometry\TESTING', 'MEDICAL', 'gcampuzanozuluaga', 'Gcz2348.']
        
        settings_input = multi_inputbox.multipleinput(msg, title, fieldNames, True, False, fieldValues = vals)
        
        #BASE SETTINGS INPUT
        labname = settings_input[0]
        test_category = settings_input[1]
        instrument_id = settings_input[2]
        netdrive = settings_input[3]
        domain = settings_input[4]
        username = settings_input[5]
        password = settings_input[6]
        print netdrive
        map_network_drive.mapped_drives(netdrive)
        
        networkdrive_letter = map_network_drive.map_netdrive(netdrive, domain, username, password)
        
        local_settings = self.local_set_generator(labname, test_category, instrument_id, netdrive, domain, username)
        
        local_settings = self.set_filesystem(labname, test_category, instrument_id, local_settings, networkdrive_letter, admin_config, place)
        server = settings_input[3]
        remote_techDir =  os.path.join(networkdrive_letter, server, 'TECHNICAL')
        #create database
        self.case_log(labname, instrument_id, place, bindir, remote_techDir)
        #create remote config database
        self.remote_set_generator(remote_techDir, local_settings)
        self.write_config(local_settings, settings_path)
        os.system(r"NET USE %s: /DELETE /YES" % networkdrive_letter)
        
    def write_config(self, local_settings, settings_path):   
        json_settings = json.dumps(local_settings, encoding="latin-1",indent = 6)
        os.open(settings_path, os.O_RDWR | os.O_CREAT)
        with open(settings_path, 'wb') as out:
            out.write(json_settings)

    def set_filesystem(self, labname, test_category, instrument_id, local_settings, networkdrive_letter, admin_config, place, labs_path = None):
        (local_dir, 
         days_del_local, 
         days_del_remote, 
         type_file, 
         name_netdrive, 
         deltabkp) = self.designate_folder()
         
        networkdrive = networkdrive_letter + ':'
        
        #CREATE remote TECHNICAL FOLDER ON FIRST PASS
        if not os.path.isdir(os.path.join(networkdrive, 'TECHNICAL')):
            tech_path = os.path.join(networkdrive, 'TECHNICAL')
            print tech_path
            os.makedirs(tech_path)
        
        #CREATE remote LABS FOLDER ON FIRST PASS
        labs_path = os.path.join(networkdrive, 'LABS')
        if not os.path.isdir(labs_path):
            os.makedirs(labs_path)    
        
        #CREATE LOCAL SENT AND NETDRIVE BACKUP FOLDERS - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED 
        

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            #print 'script'
            print os.path.join(os.path.dirname(sys.executable), str('LABCURO_SENT' + place), test_category)
            #os.system("pause")
            local_sentdir = str(os.path.join(os.path.dirname(sys.executable), str('LABCURO_SENT' + place), test_category))
            
        elif __file__:
            print 'frozen'
            print os.path.join(os.path.dirname(__file__), str('LABCURO_SENT' + place), test_category)
            #os.system("pause")
           
            local_sentdir = os.path.join(os.path.dirname(__file__), str('LABCURO_SENT' + place), test_category)
        
        print 'LOCAL SENT FILE :' + str(local_sentdir)
        #os.system("pause")
        #local_sentdir = os.path.join(os.path.dirname(__file__), str('LABCURO_SENT' + place), test_category)
        #local_sentdir = str('LABCURO_SENT' + place) + '\\' + test_category
        #backuppath = os.path.join(labname, test_category, 'BACKUP', instrument_id, name_netdrive)
        instrument_backuppath = os.path.join(labname, test_category, 'BACKUP', instrument_id)
        #instrument_backuppath = labname + '\\' + test_category + '\\' + 'BACKUP' + '\\' + instrument_id
        backup_path = os.path.join(labs_path, instrument_backuppath)
        arr = [local_sentdir, backup_path]
        for dirpath in arr:
            if not dirpath: 
             #   os.mkdir(dirpath)
            #os.mkdir(os.path.join(dirpath, name_netdrive))
                os.makedirs(dirpath)
            os.makedirs(os.path.join(dirpath, name_netdrive))
        backuppath = os.path.join(instrument_backuppath, name_netdrive)     
        
        #CREATE NETDRIVE CLINICAL IF FOLDERS IN COMMON "CLINICAL" DIRECTORY - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED
        if type_file == 'CLINICAL':
            title = "LabCuro v2.0 Installation"
            msg =   ('The files in this folder will be sent to the Clinical folder in the network drive for pathologist to view\n'
                    'Select the type of files that this directory will contain\n'
                    'Processed: Examples are PDF and DOC files\n'
                    'Raw: Examples are FCS or LMD')
            btnchoices = ['PROCESSED', 'RAW']
            clin_file_type = buttonbox(msg=msg, title=title, choices=btnchoices)
            clinical_paths = {}
            
            #if clin_file_type == 'PROCESSED':
            sites = ["COPATH", "SUNQUEST", "QC", "RESEARCH"]
            choice_site = multchoicebox(msg, title, sites)
            for name_dir in choice_site:
                print name_dir
                if clin_file_type == 'RAW':
                    sent_path = os.path.join(labname, test_category, type_file, clin_file_type)
                else:
                    sent_path = os.path.join(labname, test_category, type_file, clin_file_type, name_dir)
                curr_sent_path = os.path.join(labs_path, sent_path)
                if not os.path.isdir(curr_sent_path):
                    os.makedirs(curr_sent_path)
                #   os.makedirs(os.path.join(curr_sent_path, 'DONE'))
                
                if clin_file_type == 'PROCESSED':
                    filename_regex = admin_config['file_types'][name_dir]['in_processed_folder']
                else:
                    filename_regex = admin_config['file_types'][name_dir]['in_raw_folder']
                clinical_paths[sent_path] = {}
                clinical_paths[sent_path]['find_folder'] = filename_regex
                
                #CLINICAL FILE ADDED TO CLINICAL CASE DATABASE
                file_clinicaldb = admin_config['file_types'][name_dir]['add_to_clin_database']
                if file_clinicaldb and clin_file_type == 'PROCESSED':
                    clinical_paths[sent_path]['add_to_clin_database'] =  admin_config["file_types"][name_dir]['add_to_clin_database']
                else:
                    clinical_paths[sent_path]['add_to_clin_database'] = None 
                if clin_file_type == 'PROCESSED' and  admin_config['file_types'][name_dir]["add_to_clin_database"]:
                    #CLINICAL PDF FILE MERGING REQUIRED
                    msg =   ('Clinical case type: ' + name_dir + '\nDo cases (PDF files) require merging by accesion number and name')
                    btnchoices = ['YES', 'NO']
                    pdf_merge = buttonbox(msg=msg, title=title, choices=btnchoices)
                    merger_regex = admin_config['file_types'][name_dir]['to_merge']
                    if pdf_merge == 'YES':
                        clinical_paths[sent_path]['to_merge'] =  merger_regex 
                    else:
                        clinical_paths[sent_path]['to_merge'] = None 
                else:
                    clinical_paths[sent_path]['to_merge'] = None                                 
        else:   
            clinical_paths = None
            clin_file_type = None
            days_del_remote = None
            print 'no clinical generated'
        new_path = {
                    'local_origin_path' : local_dir, 
                    'local_sent_path' : local_sentdir,
                    'netdrive_backup_path': backuppath, 
                    'name_backup_path' : name_netdrive,
                    'netdrive_clinical_paths': clinical_paths,
                    'clinical_file': type_file,  
                    'static_vs_raw_file' : clin_file_type,
                    'local_choptail_days' : days_del_local,
                    'netdrive_clinical_choptail_days' : days_del_remote,
                    'delta_hr_bkp' : deltabkp,
                    }
        local_settings['lab_attributes']['service']['directories']['local_paths'].append(new_path)
        msg =   "Do you want to add a new directory to transfer clinical data and/or backup to the network drive?"
        title = "LabCuro v2.0 Installation"
        btnchoices = ["Yes, add more directories", "No, that is it"]
        moredirs = buttonbox(msg=msg, title=title, choices=btnchoices)
        if moredirs == "Yes, add more directories":
            self.set_filesystem(labname, test_category, instrument_id, local_settings, networkdrive_letter, admin_config, place, labs_path)
        return local_settings
    
    def designate_folder(self, instruction = [], local_dir = '', errors_in = False):
        instructions = '\n'.join(instruction)
        instruction=[]
        title = "Select a directory to integrate to system"
        if not errors_in:
            local_dir = diropenbox(title = title)
        msg         = ('Enter attributes for this directory:\n%s\n%s' % (local_dir, instructions))
        title       = 'LabCuro v2.0 Installation'
        
        #INITIAL SCREEN
        title = "LabCuro v2.0 Laboratory Suite - Setup"
        msg =   'Select type of files contained in directory to be added'
        image = "mol.gif"
        btnchoices = ['Only backup', 'Clinical cases and backup']
        file_categ = buttonbox(msg=msg, title=title, choices=btnchoices)
        print file_categ
        
        if file_categ == 'Only backup':
            type_file = 'BACKUP'
            fieldNames  = ['Name of network drive folder where files will be backed up',
                           'Days to delete local files after transfer',
                           'Hours between backup']
            path_attr = multi_inputbox.multipleinput(msg, title, fieldNames, 'no', True, ['bkp', 1, 1])
            deltabkp = path_attr[2]
            days_del_remote = None
            #clinical_fold_names = None
        else:
            type_file = 'CLINICAL'
            fieldNames  = ['Name of network drive folder where files will be backed up', 
                           'Days to delete local files after transfer',
                           'Days to delete clinical use files from clinical network directory']
            path_attr = multi_inputbox.multipleinput(msg, title, fieldNames, 'no', True, ['pdfs',1,1])
            #clinical_fold_names = path_attr[3].split(',')
            #clinical_fold_names = [x.upper() for x in clinical_fold_names]
            days_del_remote = path_attr[2]
            deltabkp = None
        name_netdrive = path_attr[0]  
        days_del_local = path_attr[1]
        return (local_dir, 
                days_del_local, 
                days_del_remote, 
                type_file, 
                name_netdrive, 
                deltabkp)
    
    def local_set_generator(self, labname, test_category, instrument_id, netdrive, domain, username):
       
        #SETTINGS_INPUT = ['Instrument Name','Laboratory name','Test category','Network drive address','Domain', 'User name']
        local_settings = {'lab_name' : labname,
                          'lab_attributes':{
                                            'machine_id' : instrument_id,
                                            'creation date' : str(datetime.datetime.today()),
                                            'creation user' : username,
                                            'service' :
                                                         {
                                                         'test_category': test_category,
                                                          'directories':{
                                                                         'local_paths' : [],
                                                                         'destination_server' :{
                                                                                                'serv_path' : netdrive, 
                                                                                                'domain' : domain
                                                                                                }
                                                                          }
                                                           }
                                                         
                                             }
                                            
                          } 
        
        print 'local setting created'
        #os.system("pause")
        return local_settings
    
    def remote_set_generator(self, remote_techDir, local_settings, lab_name=None, machine_id=None, test_category=None): 
        config_remote = os.path.join(remote_techDir,'lc_clinial_config.json') 
        if os.path.isfile(config_remote):
            #PULL LOCAL SETTINGS TO VARIABLE
            with open(config_remote, 'r+') as set_json:
                settings_json = set_json.read()
            cnt = 0
            remote_settings = json.loads(settings_json)
            not_new = False
            for machine in remote_settings:
                print machine
                if (machine['lab_name'] == lab_name and 
                    machine['lab_attributes']['machine_id'] == machine_id and 
                    machine['lab_attributes']['service']['test_category'] == test_category):
                    new_paths = local_settings['lab_attributes']['service']['directories']['local_paths']
                    remote_settings[cnt]['lab_attributes']['service']['directories']['local_paths'] = new_paths
                    not_new = True
                cnt += 1
            if not_new != True:
                #remote_settings = json.loads(settings_json) 
                remote_settings.append(local_settings) 
        else:
            remote_settings = []
            remote_settings.append(local_settings)
        json_remote_settings = json.dumps(remote_settings, encoding="latin-1",indent = 6)
        os.open(config_remote, os.O_RDWR | os.O_CREAT)
        with open(config_remote, 'wb') as out:
            out.write(json_remote_settings)
        
    def case_log(self, lab_name, instrument_id, place, bindir, remote_techDir):
        create_clinical_log = ('CREATE TABLE case_log('
        'id INTEGER PRIMARY KEY,'
        'lab_name TEXT,'##
        'lab_service TEXT,'
        'instrument_id TEXT,'###
        'accession_number TEXT,'
        'patient_name TEXT,'
        'matrix TEXT, '
        'panel TEXT, '
        'lab_tech TEXT,'
        'date_sent_to_pathology DATETIME,'
        'training_pathologist TEXT,'
        'pathologist TEXT,'
        'date_reviewed_pathologist DATETIME)')
        
        create_machine_log = ('CREATE TABLE tech_log('
        'id INTEGER PRIMARY KEY,'
        'date_run DATETIME,'
        'lab_name TEXT,'##
        'instrument_id TEXT,'## 
        'lab_service TEXT,'
        'backed_up_items TEXT,'
        'bkp_cnt INTEGER,'
        'deleted_items_local TEXT,'
        'del_cnt INTEGER,'
        'clinical_cases_sent TEXT, '
        'clin_cnt INTEGER,'
        'clinical_cases_failtosend TEXT,'
        'fail_cnt INTEGER,'
        'lab_tech TEXT)')
        
        db_clin_name = remote_techDir + '\\' + str('clinical_cases.db')
        db_tech_name = bindir + '\\' + str('tech_runs_' + place + '.db')
        
        #db_clin_name = os.path.join(remote_techDir, str('clinical_cases.db'))
        #db_tech_name = os.path.join(str(os.path.dirname(__file__)), bindir, str('tech_runs_' + place + '.db'))
        
        if not os.path.isfile(db_clin_name):## CREATE REMOTE DB IF IT DOESNT EXIST - AVOID CONFLIC WITH MULTIPL MACHINES TO SAME SERVER
            print db_clin_name
            database_handler.create(create_clinical_log, db_clin_name)
        database_handler.create(create_machine_log, db_tech_name)