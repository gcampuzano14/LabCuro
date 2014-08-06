#CONFIG FILE
import json
import os

def config(localconfig_dir):
    regex_json = {
                  'file_types' :{
                                 "RESEARCH" : {'add_to_clin_database': None,
                                               'in_processed_folder':'(.*RXH.*).pdf',
                                               'in_raw_folder':'(.*RXH.*).pdf',
                                               'to_merge':'{{{_FILE_TO_MERGE_}}}(.*RXH.*).\.pdf'},
                                 "QC" : {'add_to_clin_database': None,
                                         'in_processed_folder' : "(.*QCF.*).pdf",
                                         'in_raw_folder' : "(.*QCF.*).pdf",
                                         'to_merge' : "{{{_FILE_TO_MERGE_}}}(.*QCF.*).\.pdf"},
                                 "COPATH" : {'add_to_clin_database': {'BONE MARROW | PERIPHERAL BLOOD':'(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB))\s+(\w+\d*)\s.+?(?=\.pdf)',
                                                                      'TISSUE | FLUIDS | OTHER':'(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:TS)|(?:FL))\s+(\w+\d*)\s.+?(?=\.pdf)'},
                                             'in_processed_folder' : "(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s+(\w+\d*)\s.+?(?=\.pdf)",
                                             'in_raw_folder' : "(\D{1,2}\d{2}-{1}\d+\w{0,})\s+(\w+-{0,1}\w+)\s.*?",
                                             'to_merge': "({{{_FILE_TO_MERGE_}}})(\D{1,2}\d{2}-{1}\d+\w{0,}\s+\w+-{0,1}\w+\s+(?:(?:BM)|(?:PB)|(?:TS)|(?:FL))\s+\w+\d*)(.+)(?=\.pdf)"},
                                 "SUNQUEST" : {'add_to_clin_database': {'BONE MARROW | PERIPHERAL BLOOD':'([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB))\s(\w+\d*)\s.+?(?=\.pdf)',
                                                                      'TISSUE | FLUIDS | OTHER':'([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:TS)|(?:FL))\s(\w+\d*)\s.+?(?=\.pdf)'},
                                               'in_processed_folder': "([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s+((?:BM)|(?:PB)|(?:TS)|(?:FL))\s(\w+\d*)\s.+?(?=\.pdf)",
                                               'in_raw_folder': "([MTXWFHS]\d+\w{0,})\s+(\w+-{0,1}\w+)\s.*?",
                                               'to_merge': "({{{_FILE_TO_MERGE_}}})([MTXWFHS]\d+\w{0,}\s+\w+-{0,1}\w+\s+(?:(?:BM)|(?:PB)|(?:TS)|(?:FL))\s\w+\d*)(.+)(?=\.pdf)"}
                                 },
                  'master_users':['gcampuzano', 'gcampuzanozuluaga', 'arangel', 'eimmunop', 'msharief', 'gsodeman']
                  }
    
    if not os.path.isdir(localconfig_dir):
        os.mkdir(localconfig_dir)
    config_path = os.path.join(localconfig_dir, 'config.json')
    json_config = json.dumps(regex_json, encoding="latin-1",indent = 6)
    os.open(config_path, os.O_RDWR | os.O_CREAT)
    with open(config_path, 'wb') as out:
        out.write(json_config)
        
def pull_config():
    with open(os.path.join(os.path.dirname(__file__), str('config.json')), 'r+') as set_json:
        config_json = set_json.read()
    local_config = json.loads(config_json)
    #PRINT REGEX
    #for e in   local_config['file_types']:
    #    print e
     #   for a in local_config['file_types'][e]:
      #      print str(a), str(local_config['file_types'][e][a])

    
    
 
    
