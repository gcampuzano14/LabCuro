from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import re

def pdfmerger(clinical_path, file_item, merge_regex, temp_path):
    #for file_item in os.listdir(clinical_path):
    file_path = os.path.join(clinical_path,file_item)
    files_to_kill = []
    if os.path.isfile(file_path):
        matchname = re.match(merge_regex, file_item, re.IGNORECASE)
        #matchname = re.match('({{{_FILE_TO_MERGE_}}})(\D{1,2}\d{2}-{1}\d+)(.+)(?=.PDF)', file_item)
        if matchname:
            #merge(matchname, clinical_path, file_item, temp_dir)
            merge_flag = matchname.group(1)
            fin_name = matchname.group(2)
            tail_file = matchname.group(3)
            extension = file_item[-4:]
            head_match =    merge_flag + fin_name
            reaschpattern = head_match + '.+(' + extension +')'
            merger = PdfFileMerger()
            for target in os.listdir(clinical_path):
                file_path = os.path.join(clinical_path, target)
                if os.path.isfile(file_path):
                        y = re.match(reaschpattern, target)
                        if y:
                            file_open = file(file_path, 'rb')
                            merger.append(PdfFileReader(file_open))
                            file_open.close()
                            files_to_kill.append(file_path)
                            
            file_name = fin_name+' '+ tail_file + extension
            file_name = re.sub(r'\s{2,}', ' ', file_name)
            
            #file_name = fin_name+'\s'+ tail_file + extension
            temp_dir = os.path.join(temp_path, file_name)
            doc = temp_dir
            merger.write(str(doc))
            merger.close()
            #for file_kill in files_to_kill:
            #    os.remove(file_kill)  
                    
    if len(files_to_kill) > 0:
        return files_to_kill
    
    else: 
        return None

