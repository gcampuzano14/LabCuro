#import shutil
import os
import sys
import subprocess
import hashlib

#OPEN FILE BY OS
def openFolder(path):
    if sys.platform == 'darwin':   
        subprocess.call(['open', path])
    elif sys.platform == 'linux2':
        subprocess.call(['gnome-open', '--', path])
    elif sys.platform == 'win32':
        subprocess.call(['explorer', path])
    return sys.platform

#GENERATYE DATE SERIAL FOR DUPLICATED FILES
def date_serial(year, month, day, hour, minute, second):
    date_items = [str(year), str(month), str(day), str(hour), str(minute), str(second)]
    for i in range(0,len(date_items)):
        if len(date_items[i]) == 1:
            date_items[i] = '0' + date_items[i]
    date_serial =  "".join(date_items)
    return date_serial

#CHECKSUMS FOR TRANSFERED FILES 
class checksums():
    
    def check_files(self, files): 
        hashes = []
        for f in files: 
            hasher = hashlib.md5(f)
            with open(f, 'rb') as file_to_hash:
                file_bin = file_to_hash.read()
                file_hash = hasher.update(file_bin)
                hashes.append(file_hash)
        if hashes[0] == hashes[1]:
            return True
        else:
            return False

    def check_dirs(self, dirs): 
        cs = checksums()
        mydict = {dirs[0] : {}, dirs[1] : {}}
        lists = []
        for k in mydict:
            for root, dirs, files in os.walk(k):
                for name in files:
                    if name in mydict[k]:
                        mydict[k][name].append(root)
                    else:
                        mydict[k][name] = [root]
            lists.append(mydict[k])
        if len(lists[0]) == len(lists[1]):
            for k in lists[0]:
                root_len = len(lists[0][k])
                for i in range(0,root_len):
                    file_ori = os.path.join(lists[0][k][i],k)
                    file_dst = os.path.join(lists[1][k][i],k)
                    files = [file_ori, file_dst]
                    return cs.check_files(files)



