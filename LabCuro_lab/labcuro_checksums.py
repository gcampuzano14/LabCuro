import hashlib
import os
import traceback

class checksums():
    
    def check_files(self, files): 
        hashes = []
        for f in files: 
            hasher = hashlib.md5(f)
            with open(f, 'rb') as file_to_hash:
                file_bin = file_to_hash.read()
                file_hash = hasher.update(file_bin)
                #hasher.hexdigest()
                hashes.append(file_hash)
        if hashes[0] == hashes[1]:
            return True
        else:
            return False
    
    def check_dirs(self, directories):
        hashes = []
        for d in directories: 
            hasher = hashlib.md5()
            try:
                for root, dirs, files in os.walk(d):
                    for name in files:
                        filepath = os.path.join(root,name)
                        try:
                            file_to_hash = open(filepath, 'rb')
                        except:
                            # You can't open the file for some reason
                            file_to_hash.close()
                            continue
                        while 1:
                            file_bin = file_to_hash.read()
                            #print buf
                            if not file_bin : break
                            hasher.update(hashlib.md5(file_bin).hexdigest())
                        file_to_hash.close()
            except:
                traceback.print_exc()
                return -2
            print d
            print hasher.hexdigest()
            file_hash =  hasher.hexdigest()
            hashes.append(file_hash)
            #print d
            #print hasher.hexdigest()
        print hashes
        if hashes[0] == hashes[1]:
            print  True
        else:
            print False
        #return hasher.hexdigest()
    
    def check_dirs(self, directories):
        hashes = []
        for d in directories: 
            print d
            althasher = None
            hasher = None

            althasher = hashlib.md5()
            hasher = hashlib.md5()
            try:
                for root, dirs, files in os.walk(d):
                    #print files
                    for name in files:
                        #print name
                       # print root
                       # print dirs
                        filepath = os.path.join(root,name)
                       # print filepath
                        try:
                            file_to_hash = open(filepath, 'rb')
                        except:
                            # file won't open arrrhgg!!!
                            file_to_hash.close()
                            print 'no'
                            continue
    
                        while 1:
                            file_bin = file_to_hash.read()
                            rr = re.match(r'.+00008322\s2013-01-28\s1148\s001\.LMD\.PDF',filepath)
                            if rr:
                                althasher = None
                                althasher = hashlib.md5()
                                althasher.update(file_bin)
                                print althasher.hexdigest()
                            
                            if not file_bin: 
                                #print 'fgdsgdf'
                                break
                            hasher.update(file_bin)

                        file_to_hash.close()
            except:
                traceback.print_exc()
                return -2
            #print d
            #print hasher.hexdigest()
            file_hash =  hasher.hexdigest()
            hashes.append(file_hash)
        if hashes[0] == hashes[1]:
            return  True
        else:
            return False
    def check_dirsC(self, directories):
        lhasher = hashlib.md5()
        fhasher = hashlib.md5()
        mydict = {directories[0] : lhasher, directories[1] : fhasher}
        hashes = []
        for k in mydict: 
            cnt = 0
            print mydict[k].hexdigest()
            print k
            try:
                for root, dirs, files in os.walk(k):
                    print root
                    for name in files:
                        filepath = os.path.join(root,name)
                        try:
                            file_to_hash = open(filepath, 'rb')
                        except:
                            file_to_hash.close()
                            print 'no'
                            continue
                        while 1:
                            file_bin = file_to_hash.read()
                            cnt += 1
                            if not file_bin: 
                                #print 'fgdsgdf'
                                break
                            mydict[k].update(file_bin)

                        file_to_hash.close()
            except:
                traceback.print_exc()
                return -2
            print "kkkkk"
            print mydict[k].hexdigest()
            print k
            file_hash =  mydict[k].hexdigest()
            hashes.append(file_hash)
            print hashes
            print "ciount: ", str(cnt)
        if hashes[0] == hashes[1]:
            return  True
        else:
            return False


def check_dirs(dirs): 
    cs = checksums()
    mydict = {dirs[0] : {}, dirs[1] : {}}
    lists = []
    cnt = 0
    for k in mydict:
        for root, dirs, files in os.walk(k):
            for name in files:
                filepath = os.path.join(root,name)
                if name in mydict[k]:
                    mydict[k][name].append(root)
                else:
                    mydict[k][name] = [root]
        r = sorted(mydict[k])
        cnt += 1
        lists.append(mydict[k])
    cnt = 0
    print lists[1]
    if len(lists[0]) == len(lists[1]):
        for k in lists[0]:
            root_len = len(lists[0][k])
            for i in range(0,root_len):
                file_ori = os.path.join(lists[0][k][i],k)
                file_dst = os.path.join(lists[1][k][i],k)
                files = [file_ori, file_dst]
                print files
                print cs.check_files(files)


   

#cs = checksums()
dir1 = os.path.join('C:','flwr')
dir2 = os.path.join('A:','flwr')
#shutil.copytree(dir1, dir2, symlinks=False, ignore=None)
dirs = [dir1,dir2]

#print cs.check_dirsC(dirs)
check_dirs(dirs)



directory_ori = os.path.join(os.path.dirname(__file__),'LABCURO_SENT_home')
directory_dst =os.path.join(os.path.dirname(__file__),'LABCURO_SENT_home')
checker = checksums()
checker.check_dirs([directory_ori, directory_dst])

#print GetHashofDirs('My Documents', 1)

#file_ori = 'local_settings_home.json'        
#file_dst = 'local_settings_home.json'      
                
#files = (file_ori, file_dst)     

#check_files(files)