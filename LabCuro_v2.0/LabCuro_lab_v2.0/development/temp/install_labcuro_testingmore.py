import os
import datetime
import json
import map_network_drive
import multi_inputbox
import database_handler
from easygui_labcuro import diropenbox, buttonbox, choicebox, enterbox, multenterbox

class common_settings():
    def local_set_generator(self, settings_input = None, local_settings = None, test_category = None, netdrive= None, domain= None):
        if not settings_input:
            #SETTINGS_INPUT = ['Instrument Name','Laboratory name','Test category','Network drive address','Domain', 'User name', 'Password']
            local_settings = {'lab_name' : settings_input[0],
                              'lab_attributes':{
                                                'creation date' : str(datetime.datetime.today()),
                                                'creation user' : settings_input[5],
                                                'services' :[
                                                             {
                                                             'test_category': settings_input[1],
                                                             'machine_id' : settings_input[2],
                                                              'directories':{
                                                                             'local_paths' : [],
                                                                             'destination_server' :{
                                                                                                    'serv_path' : settings_input[3], 
                                                                                                    'domain' : settings_input[4]
                                                                                                    }
                                                                              }
                                                               }
                                                             ]
                                                 }
                                                
                              } 
            
         
        else: 
            new_paths = {'test_category': test_category,
                         'machine_id' : settings_input[2],
                         'directories':{'local_paths' : [],
                                        'destination_server' :{
                                                               'serv_path' : netdrive,
                                                               'domain' : domain
                                                               }
                                        }
                         }

            local_settings['lab_attributes']['services'].append(new_paths)
            
        
        return local_settings
    
    def set_filesystem(self, labname, test_category, instrument_id, local_settings, networkdrive_letter = None, admin_config, place, labs_path = None):
        (local_dir, 
         days_del_local, 
         days_del_remote, 
         type_file, 
         name_netdrive, 
         clinical_fold_names, 
         deltabkp) = self.designate_folder()
        
        #CREATE remote TECHNICAL FOLDER ON FIRST PASS
        #CREATE remote LABS FOLDER ON FIRST PASS
        if len(local_settings['lab_attributes']['services'][0]['directories']['local_paths']) == 0:
            tech_path = os.path.join(networkdrive, 'TECHNICAL')
            os.makedirs(tech_path)
            labs_path = os.path.join(networkdrive, 'LABS')
            os.makedirs(labs_path)   

        #CREATE LOCAL SENT AND NETDRIVE BACUP FOLDERS - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED 
        local_sentdir = os.path.join(os.path.dirname(__file__), str('LABCURO_SENT_' + place), test_category, name_netdrive)
        backuppath = os.path.join(labname, test_category, 'BACKUP', ment_id, name_netdrive)
        backup_path = os.path.join(labs_path, backuppath)
        arr = [local_sentdir, backup_path]
        for p in arr:
            os.makedirs(p)
            
        #CREATE NETDRIVE CLINICAL IF FOLDERS IN COMMON "CLINICAL" DIRECTORY - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED
        if type_file == 'CLINICAL':
            title = "LabCuro Installation"
            msg =   ('The files in this folder will be sent to the Clinical folder in the network drive for pathologist to view\n'
                    'Select the type of files that this directory will contain\n'
                    'Processed: Examples are PDF and DOC files\n'
                    'Raw: Examples are FCS or LMD')
            btnchoices = ['PROCESSED', 'RAW']
            clin_file_type = buttonbox(msg=msg, title=title, choices=btnchoices)
            clinical_paths = {}
            for name_dir in clinical_fold_names:
                sent_path = os.path.join(labname, test_category, type_file, clin_file_type, name_dir)
                curr_sent_path = os.path.join(labs_path, labname, test_category, type_file, clin_file_type, name_dir)
                os.makedirs(curr_sent_path)
                os.makedirs(os.path.join(curr_sent_path, 'DONE'))
                
                #CLINICAL FILE REGEX
                msg =('Select the type of case that will go in the folder\n'
                      'Name of clinical case directory:' + name_dir + '\n RAW FILES MUST COINCIDE WITH CORRESPONDING PROCESSED FILES FOR LABCURO CLINICAL TO FUNCTION PROPERLY')
                sites = ["COPATH", "SUNQUEST", "QC", "RESEARCH"]
                choice_site = choicebox(msg, title, sites)
                filename_regex = admin_config['file_types'][choice_site]['in_folder']
                clinical_paths[sent_path] = {}
                clinical_paths[sent_path]['find_folder'] = filename_regex
                
                #CLINICAL FILE ADDED TO CLINICAL CASE DATABASE
                file_clinicaldb = admin_config['file_types'][choice_site]['add_to_clin_database']
                if file_clinicaldb and clin_file_type == 'PROCESSED':
                    clinical_paths[sent_path]['add_to_clin_database'] =  admin_config["file_types"][choice_site]['add_to_clin_database']
                else:
                    clinical_paths[sent_path]['add_to_clin_database'] = None 
    
                #CLINICAL PDF FILE MERGING REQUIRED
                msg =   ('Would merging of PDF files for clinical cases be required')
                btnchoices = ['YES', 'NO']
                pdf_merge = buttonbox(msg=msg, title=title, choices=btnchoices)
                merger_regex = admin_config['file_types'][choice_site]['to_merge']
                if pdf_merge == 'YES':
                    clinical_paths[sent_path]['to_merge'] =  merger_regex 
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
        local_settings['lab_attributes']['services'][0]['directories']['local_paths'].append(new_path)
        msg =   "Do you want to add a new directory to transfer clinical data and/or backup to the network drive?"
        title = "LabCuro Installation"
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
        title       = 'LabCuro Installation'
        fieldNames  = ['Is this for clinical use?',
                       'Days to delete local files after transfer',
                       'Days to delete network drive files after transfer (only clinical)',
                       'New clinical folder names (separate by comma)',
                       'Name of network drive folder where files will be backed up',
                       'Hours between backup']
        path_attr = multi_inputbox.multipleinput(msg, title, fieldNames, 'no', True, ['YES | NO',120,120,'','',24, 'YES | NO'])
        print path_attr 
        if  path_attr[0] == 'YES':
            type_file = "CLINICAL"
        elif path_attr[0] == 'NO':
            type_file = "BACKUP"   
        clinical_fold_names = path_attr[3].split(',')
        clinical_fold_names = [x.upper() for x in clinical_fold_names]
        days_del_local = path_attr[1]
        days_del_remote = path_attr[2]
        name_netdrive = path_attr[4]
        deltabkp = path_attr[5]
        return (local_dir, 
                days_del_local, 
                days_del_remote, 
                type_file, 
                name_netdrive, 
                clinical_fold_names, 
                deltabkp)   
    
class install_labcuro(common_settings):
    def install_main(self, settings_path, admin_config, place):
        # INTRO MESSAGGEBOX
        msg =   """
               This is the first time you run LabCuro on this instrument.
               Follow these instructions:\n
               1. Designate an instrument name.
               2. Set the file paths that will be backed up
               3. Set the file paths that will be used to transmit PDF files for clinical use*
               4. Set the file paths that will be used to transmit raw analysis data files for clinical use*\n    
               * Backup paths will be created if these where not specivied in item 2.\n 
               The information obtained from this initial setup will be saved to "local_settings.json" file in the current folder.\n
               LabCuro v3.0
               Authors: 
               """
        title = "LabCuro Installation"
        image = "mol.gif"
        btnchoices = ["Setup", "Cancel"]
        intro = buttonbox(image=image, msg=msg, title=title, choices=btnchoices)
        if intro == "Setup":
            pass
        else:
            quit()
        #DESIGNATE LABORATORY SERVICE ATTRIBUTES
        msg         = ('Enter values for laboratory service\nInput user name and password used to access network drive\n'
                       'Refer to installation log for history on this installation')
        title       = 'LabCuro Installation'
        fieldNames  = ['Laboratory name',
                       'Test category',
                       'Instrument Name',
                       'Network drive address',
                       'Domain', 
                       'User name', 
                       'Password']
        
        #CREATE local_settings DATA STRUCTURE
        vals = ['test_lab', 'FLOW', 'intrument_111', '\\\\vprotocz\gcz_testshare', 'vprotocz', 'gcampuzano ', 'g3rcamzul']
        #vals = ['test_lab_hospital', 'FLOW', 'intrument_666', '\\\\jhscel01.um-jmh.org\JMH_Flow_Cytometry\TESTING', 'MEDICAL', 'gcampuzanozuluaga', 'Gcz2348.']
        settings_input = multi_inputbox.multipleinput(msg, title, fieldNames, True, False, fieldValues = vals)
        networkdrive_letter = map_network_drive.map_netdrive(settings_input[3], settings_input[4], settings_input[5], settings_input[6]) + ':'
        #networkdrive_letter = "C:"
        local_settings = self.local_set_generator(settings_input)
        local_settings = self.set_filesystem(settings_input[0], settings_input[1], settings_input[2], local_settings, networkdrive_letter, admin_config, place)
        
        #create database
        self.case_log(settings_input[0], settings_input[2], place)
        
        #create remote config database
        self.remote_set_generator(settings_input[3], settings_input[4], local_settings)
        
        json_settings = json.dumps(local_settings, encoding="latin-1",indent = 6)
    
        #settings_path = os.path.join(os.path.dirname(__file__), 'local_settings.json')
        os.open(settings_path, os.O_RDWR | os.O_CREAT)
        with open(settings_path, 'wb') as out:
            out.write(json_settings)
        
        os.system(r"NET USE %s: /DELETE /YES" % networkdrive_letter)
    
    def set_filesystem(self, labname, test_category, instrument_id, local_settings, networkdrive_letter, admin_config, place, labs_path = None):
        (local_dir, 
         days_del_local, 
         days_del_remote, 
         type_file, 
         name_netdrive, 
         clinical_fold_names, 
         deltabkp) = self.designate_folder()
        
        
        #CREATE remote TECHNICAL FOLDER ON FIRST PASS
        if len(local_settings['lab_attributes']['services'][0]['directories']['local_paths']) == 0:
            tech_path = os.path.join(networkdrive, 'TECHNICAL')
            os.makedirs(tech_path)
            
        #CREATE remote LABS FOLDER ON FIRST PASS
        if labs_path == None:
            labs_path = os.path.join(networkdrive, 'LABS')
            os.makedirs(labs_path)   
        
        #CREATE LOCAL SENT AND NETDRIVE BACUP FOLDERS - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED 
        local_sentdir = os.path.join(os.path.dirname(__file__), str('LABCURO_SENT_' + place), test_category, name_netdrive)
        backuppath = os.path.join(labname, test_category, 'BACKUP', instrument_id, name_netdrive)
        backup_path = os.path.join(labs_path, backuppath)
        arr = [local_sentdir, backup_path]
        for p in arr:
            os.makedirs(p)
            
        #CREATE NETDRIVE CLINICAL IF FOLDERS IN COMMON "CLINICAL" DIRECTORY - FOR AS LONG AS FUNCTION IS RECURSIVELY CALLED
        if type_file == 'CLINICAL':
            title = "LabCuro Installation"
            msg =   ('The files in this folder will be sent to the Clinical folder in the network drive for pathologist to view\n'
                    'Select the type of files that this directory will contain\n'
                    'Processed: Examples are PDF and DOC files\n'
                    'Raw: Examples are FCS or LMD')
            btnchoices = ['PROCESSED', 'RAW']
            clin_file_type = buttonbox(msg=msg, title=title, choices=btnchoices)
            clinical_paths = {}
            for name_dir in clinical_fold_names:
                sent_path = os.path.join(labname, test_category, type_file, clin_file_type, name_dir)
                curr_sent_path = os.path.join(labs_path, labname, test_category, type_file, clin_file_type, name_dir)
                os.makedirs(curr_sent_path)
                os.makedirs(os.path.join(curr_sent_path, 'DONE'))
                
                #CLINICAL FILE REGEX
                msg =('Select the type of case that will go in the folder\n'
                      'Name of clinical case directory:' + name_dir + '\n RAW FILES MUST COINCIDE WITH CORRESPONDING PROCESSED FILES FOR LABCURO CLINICAL TO FUNCTION PROPERLY')
                sites = ["COPATH", "SUNQUEST", "QC", "RESEARCH"]
                choice_site = choicebox(msg, title, sites)
                filename_regex = admin_config['file_types'][choice_site]['in_folder']
                clinical_paths[sent_path] = {}
                clinical_paths[sent_path]['find_folder'] = filename_regex
                
                #CLINICAL FILE ADDED TO CLINICAL CASE DATABASE
                file_clinicaldb = admin_config['file_types'][choice_site]['add_to_clin_database']
                if file_clinicaldb and clin_file_type == 'PROCESSED':
                    clinical_paths[sent_path]['add_to_clin_database'] =  admin_config["file_types"][choice_site]['add_to_clin_database']
                else:
                    clinical_paths[sent_path]['add_to_clin_database'] = None 
    
                #CLINICAL PDF FILE MERGING REQUIRED
                msg =   ('Would merging of PDF files for clinical cases be required')
                btnchoices = ['YES', 'NO']
                pdf_merge = buttonbox(msg=msg, title=title, choices=btnchoices)
                merger_regex = admin_config['file_types'][choice_site]['to_merge']
                if pdf_merge == 'YES':
                    clinical_paths[sent_path]['to_merge'] =  merger_regex 
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
        local_settings['lab_attributes']['services'][0]['directories']['local_paths'].append(new_path)
        msg =   "Do you want to add a new directory to transfer clinical data and/or backup to the network drive?"
        title = "LabCuro Installation"
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
        title       = 'LabCuro Installation'
        fieldNames  = ['Is this for clinical use?',
                       'Days to delete local files after transfer',
                       'Days to delete network drive files after transfer (only clinical)',
                       'New clinical folder names (separate by comma)',
                       'Name of network drive folder where files will be backed up',
                       'Hours between backup']
        path_attr = multi_inputbox.multipleinput(msg, title, fieldNames, 'no', True, ['YES | NO',120,120,'','',24, 'YES | NO'])
        print path_attr 
        if  path_attr[0] == 'YES':
            type_file = "CLINICAL"
        elif path_attr[0] == 'NO':
            type_file = "BACKUP"   
        clinical_fold_names = path_attr[3].split(',')
        clinical_fold_names = [x.upper() for x in clinical_fold_names]
        days_del_local = path_attr[1]
        days_del_remote = path_attr[2]
        name_netdrive = path_attr[4]
        deltabkp = path_attr[5]
        return (local_dir, 
                days_del_local, 
                days_del_remote, 
                type_file, 
                name_netdrive, 
                clinical_fold_names, 
                deltabkp)
    
    def local_set_generatorNOOOOOOOOOOOOO(self, settings_input):
        #SETTINGS_INPUT = ['Instrument Name','Laboratory name','Test category','Network drive address','Domain', 'User name', 'Password']
        local_settings = {'lab_name' : settings_input[0],
                          'lab_attributes':{
                                            'machine_id' : settings_input[2],
                                            'creation date' : str(datetime.datetime.today()),
                                            'creation user' : settings_input[5],
                                            'services' :[
                                                         {
                                                         'test_category': settings_input[1],
                                                          'directories':{
                                                                         'local_paths' : [],
                                                                         'destination_server' :{
                                                                                                'serv_path' : settings_input[3], 
                                                                                                'domain' : settings_input[4]
                                                                                                }
                                                                          }
                                                           }
                                                         ]
                                             }
                                            
                          } 
        
         
        return local_settings
    
    def remote_set_generator(self, server,domain, local_settings):  
        config_remote = os.path.join(server, 'TECHNICAL','lc_clinial_config.json') 
        if os.path.isfile(config_remote):
            #PULL LOCAL SETTINGS TO VARIABLE
            with open(config_remote, 'r+') as set_json:
                settings_json = set_json.read()
            remote_settings = json.loads(settings_json) 
            remote_settings.append(local_settings) 
        else:
            remote_settings = []
            remote_settings.append(local_settings)
        json_remote_settings = json.dumps(remote_settings, encoding="latin-1",indent = 6)
        os.open(config_remote, os.O_RDWR | os.O_CREAT)
        with open(config_remote, 'wb') as out:
            out.write(json_remote_settings)
        
    def case_log(self, lab_name, instrument_id, place):
        create_clinical_log = ('CREATE TABLE case_log_' + lab_name + '('
        'id INTEGER PRIMARY KEY,'
        'lab_service TEXT,'
        'accession_number TEXT,'
        'patient_name TEXT,'
        'matrix TEXT, '
        'panel TEXT, '
        'lab_tech TEXT,'
        'date_sent_to_pathology DATETIME,'
        'training_pathologist TEXT,'
        'pathologist TEXT,'
        'date_reviewed_pathologist DATETIME)')
        
        create_machine_log = ('CREATE TABLE tech_log_' + lab_name + '_' + instrument_id + '('
        'id INTEGER PRIMARY KEY,'
        'date_run DATETIME,'
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
        
        db_clin_name = str(os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep +'clinical_cases_' + place + '.db')
        db_tech_name = str(os.path.dirname(__file__) + os.sep + 'labcuro_bin' + os.sep +'tech_runs_' + place + '.db')
        
        database_handler.create(create_clinical_log, db_clin_name)
        database_handler.create(create_machine_log, db_tech_name)
        
class setup_labcuro(common_settings):
    def setup_main(self, local_settings, admin_config, place, networkdriveletter, domain):

        title = 'LabCuro v3.0 Setup'
        msg =('Setup options')
        options = ['Add laboratory test or instrument', 'Edit path settings','Change network path','Add path to backup', 'Eliminate path from backup', 'Eliminate laboratory test']
        choice_setup = choicebox(msg, title, options)
        if choice_setup == 'Add laboratory test':
            self.new_test(local_settings, admin_config, place, networkdriveletter, domain)
        print choice_setup

    def new_test(self, local_settings, admin_config, place, networkdriveletter, domain):
        title = 'LabCuro v3.0 Setup'
        msg =('Enter new service')
        fieldNames = ['New test category', 'Instrument ID']
        new_test = multenterbox(title, msg)
        test_category = new_test[0]
        instrument_id = new_test[1]
        local_settings  = self.local_set_generator(local_settings, test_category)
        labname = local_settings['lab_name']
        admin_config
        self.set_filesystem(labname, test_category, instrument_id, local_settings, networkdriveletter, admin_config, place, None)
        print  local_settings
    

#Remove for deployment
#settings_path = os.path.dirname(__file__) + os.sep + 'local_settings.json'
#install_main(settings_path)